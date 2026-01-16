import asyncio
import os
from datetime import datetime
from typing import List
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User, Course, CrawlerLog
from app.crawler import USCCrawler
from app.email_service import EmailService


class CrawlerScheduler:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.crawler = USCCrawler()
        self.email_service = EmailService()
        self.last_status_email = {}  # {user_id: last_sent_time}
        
    async def init_crawler(self):
        """크롤러 초기화"""
        await self.crawler.start()
        
    async def cleanup(self):
        """크롤러 종료"""
        await self.crawler.close()
        
    async def crawl_all_courses(self):
        """모든 등록된 수업들을 크롤링"""
        db: Session = SessionLocal()
        try:
            # 모든 활성 수업 가져오기
            courses = db.query(Course).all()
            
            if not courses:
                return
            
            # 사용자별로 그룹화
            user_courses = {}
            for course in courses:
                if course.user_id not in user_courses:
                    user_courses[course.user_id] = []
                user_courses[course.user_id].append(course)
            
            # 각 사용자별로 처리
            for user_id, user_course_list in user_courses.items():
                user = db.query(User).filter(User.id == user_id).first()
                if not user:
                    continue
                
                available_courses = []
                status_courses = []
                
                for course in user_course_list:
                    # 크롤링 실행
                    result = await self.crawler.find_course(course.course_number)
                    
                    if result:
                        # 로그 저장
                        screenshot_dir = "screenshots"
                        os.makedirs(screenshot_dir, exist_ok=True)
                        screenshot_path = os.path.join(
                            screenshot_dir, 
                            f"{course.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                        )
                        
                        screenshot_taken = await self.crawler.take_course_screenshot(
                            course.course_number, 
                            screenshot_path
                        )
                        
                        log = CrawlerLog(
                            course_id=course.id,
                            registered_info=result.get('registered'),
                            is_available=result.get('is_available', False),
                            screenshot_path=screenshot_path if screenshot_taken else None
                        )
                        db.add(log)
                        
                        # 수업 정보 업데이트
                        course.current_registered = result.get('registered')
                        course.course_name = result.get('course_name', course.course_name)
                        
                        # 자리가 생겼는지 확인 (이전에는 만석이었는데 이제 자리가 있음)
                        if result.get('is_available', False):
                            if not course.is_available:  # 이전에는 만석이었음
                                available_courses.append({
                                    'course_number': course.course_number,
                                    'course_name': result.get('course_name', f"CSCI {course.course_number}"),
                                    'registered': result.get('registered', ''),
                                    'is_available': True
                                })
                            course.is_available = True
                            status_courses.append({
                                'course_number': course.course_number,
                                'course_name': result.get('course_name', f"CSCI {course.course_number}"),
                                'registered': result.get('registered', ''),
                                'is_available': True
                            })
                        else:
                            course.is_available = False
                            status_courses.append({
                                'course_number': course.course_number,
                                'course_name': result.get('course_name', f"CSCI {course.course_number}"),
                                'registered': result.get('registered', ''),
                                'is_available': False
                            })
                
                db.commit()
                
                # 자리가 생긴 수업이 있으면 알림 이메일 전송
                if available_courses:
                    screenshot_paths = []
                    for course_obj in available_courses:
                        # 해당 course_number로 Course 찾기
                        target_course = next((c for c in user_course_list if c.course_number == course_obj['course_number']), None)
                        if target_course:
                            log = db.query(CrawlerLog)\
                                .filter(CrawlerLog.course_id == target_course.id)\
                                .order_by(CrawlerLog.crawled_at.desc())\
                                .first()
                            if log and log.screenshot_path:
                                screenshot_paths.append(log.screenshot_path)
                    
                    try:
                        await self.email_service.send_notification_email(
                            user.email,
                            available_courses,
                            screenshot_paths
                        )
                    except Exception as e:
                        print(f"이메일 전송 에러: {e}")
                
                # 상태 확인 (5분마다)
                now = datetime.now()
                last_sent = self.last_status_email.get(user_id)
                
                if not last_sent or (now - last_sent).total_seconds() >= 300:  # 5분 = 300초
                    try:
                        await self.email_service.send_status_email(user.email, status_courses)
                        self.last_status_email[user_id] = now
                    except Exception as e:
                        print(f"상태 이메일 전송 에러: {e}")
                        
        except Exception as e:
            print(f"크롤링 작업 에러: {e}")
            db.rollback()
        finally:
            db.close()
    
    def start(self):
        """스케줄러 시작"""
        # 15초마다 크롤링
        self.scheduler.add_job(
            self.crawl_all_courses,
            'interval',
            seconds=15,
            id='crawl_job'
        )
        self.scheduler.start()
        print("스케줄러가 시작되었습니다. 15초마다 크롤링합니다.")
