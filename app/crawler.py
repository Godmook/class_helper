import re
import os
from typing import Optional, Dict, List
from playwright.async_api import async_playwright, Page, Browser
from app.models import Course
from app.config import settings


class USCCrawler:
    def __init__(self):
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        
    async def start(self):
        """브라우저 시작"""
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=True)
        self.page = await self.browser.new_page()
        
    async def close(self):
        """브라우저 종료"""
        if self.browser:
            await self.browser.close()
            
    async def find_course(self, course_number: str) -> Optional[Dict]:
        """
        특정 수업 번호를 찾아서 정보를 반환
        Returns: {
            'course_number': '535',
            'course_name': 'Course Name',
            'registered': '49/50',
            'is_available': True/False,
            'element_selector': selector for screenshot
        }
        """
        try:
            await self.page.goto(settings.term_url, wait_until="networkidle", timeout=30000)
            
            # 페이지가 로드될 때까지 대기
            await self.page.wait_for_selector("table, .course, [class*='course']", timeout=10000)
            
            # 페이지에서 모든 텍스트 가져오기
            content = await self.page.content()
            
            # course_number를 포함하는 행 찾기
            # CSCI 535 또는 535 형식으로 찾기
            pattern = rf'(?:CSCI\s+)?{re.escape(course_number)}\b'
            
            # 페이지에서 해당 번호가 있는지 확인
            if not re.search(pattern, content, re.IGNORECASE):
                return None
            
            # JavaScript로 DOM에서 해당 수업 찾기
            # JavaScript에서 사용할 수 있도록 course_number 이스케이프
            course_num_js = course_number.replace('\\', '\\\\').replace('`', '\\`').replace('$', '\\$')
            course_info = await self.page.evaluate(f"""
                (courseNum) => {{
                    const text = document.body.innerText;
                    const regex = new RegExp('(?:CSCI\\\\s+)?' + courseNum.replace(/[.*+?^${{}}()|[\\]\\\\]/g, '\\\\$&') + '\\\\b', 'i');
                    if (!regex.test(text)) return null;
                    
                    // 테이블이나 리스트에서 해당 수업 찾기
                    const elements = Array.from(document.querySelectorAll('tr, div, li'));
                    for (let el of elements) {{
                        const text = el.innerText || '';
                        if (regex.test(text)) {{
                            // REGISTERED 정보 찾기
                            const registeredMatch = text.match(/(\\d+)\\s*\\/\\s*(\\d+)/);
                            const registered = registeredMatch ? registeredMatch[0] : null;
                            
                            // 수업명 추출 시도
                            const lines = text.split('\\n').map(l => l.trim()).filter(l => l);
                            let courseName = '';
                            for (let line of lines) {{
                                if (line.includes(courseNum) && line.length > 10) {{
                                    courseName = line;
                                    break;
                                }}
                            }}
                            
                            return {{
                                registered: registered,
                                elementIndex: elements.indexOf(el),
                                text: text.substring(0, 500)
                            }};
                        }}
                    }}
                    return null;
                }}
            """, course_num_js)
            
            if not course_info:
                return None
            
            # REGISTERED 정보 파싱
            registered = course_info.get('registered', '')
            is_available = False
            if registered:
                match = re.match(r'(\d+)\s*/\s*(\d+)', registered)
                if match:
                    current = int(match.group(1))
                    total = int(match.group(2))
                    is_available = current < total
            
            # 더 정확한 수업명 찾기
            course_name = await self.page.evaluate(f"""
                (courseNum) => {{
                    const elements = Array.from(document.querySelectorAll('*'));
                    for (let el of elements) {{
                        const text = el.innerText || '';
                        if (text.includes(courseNum) && text.length > 20 && text.length < 200) {{
                            const lines = text.split('\\n');
                            for (let line of lines) {{
                                if (line.includes(courseNum)) {{
                                    return line.trim();
                                }}
                            }}
                        }}
                    }}
                    return 'CSCI ' + courseNum;
                }}
            """, course_num_js)
            
            return {
                'course_number': course_number,
                'course_name': course_name or f"CSCI {course_number}",
                'registered': registered,
                'is_available': is_available,
                'full_text': course_info.get('text', '')
            }
            
        except Exception as e:
            print(f"크롤링 에러: {e}")
            return None
    
    async def take_course_screenshot(self, course_number: str, save_path: str) -> bool:
        """특정 수업 부분의 스크린샷을 찍어서 저장"""
        try:
            await self.page.goto(settings.term_url, wait_until="networkidle", timeout=30000)
            await self.page.wait_for_selector("table, .course, [class*='course']", timeout=10000)
            
            # 해당 수업이 있는 요소 찾기
            course_num_js = course_number.replace('\\', '\\\\').replace('`', '\\`').replace('$', '\\$')
            element = await self.page.evaluate_handle(f"""
                (courseNum) => {{
                    const elements = Array.from(document.querySelectorAll('tr, div, li, td'));
                    const regex = new RegExp(courseNum.replace(/[.*+?^${{}}()|[\\]\\\\]/g, '\\\\$&') + '\\\\b', 'i');
                    for (let el of elements) {{
                        const text = el.innerText || '';
                        if (regex.test(text)) {{
                            return el;
                        }}
                    }}
                    return null;
                }}
            """, course_num_js)
            
            if element and element.as_element():
                # 요소가 있으면 해당 요소만 스크린샷
                await element.as_element().screenshot(path=save_path)
            else:
                # 요소를 못 찾으면 전체 페이지 스크린샷
                await self.page.screenshot(path=save_path, full_page=True)
            
            return os.path.exists(save_path)
            
        except Exception as e:
            print(f"스크린샷 에러: {e}")
            # 에러가 나도 전체 페이지 스크린샷 시도
            try:
                await self.page.screenshot(path=save_path, full_page=True)
                return os.path.exists(save_path)
            except:
                return False
