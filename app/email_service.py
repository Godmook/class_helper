import aiosmtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from typing import List, Optional
from app.config import settings
import os


class EmailService:
    @staticmethod
    async def send_notification_email(
        to_email: str,
        courses: List[dict],
        screenshots: Optional[List[str]] = None
    ):
        """
        자리가 생긴 수업에 대한 알림 이메일 전송
        courses: [{'course_number': '535', 'registered': '49/50', 'course_name': '...'}]
        screenshots: 스크린샷 파일 경로 리스트
        """
        msg = MIMEMultipart('related')
        msg['From'] = settings.from_email
        msg['To'] = to_email
        msg['Subject'] = f"🎉 USC 수업 자리 알림: {len(courses)}개 수업에 자리가 생겼습니다!"
        
        # HTML 본문 작성
        html_body = f"""
        <html>
        <body>
            <h2>USC 수업 자리 알림</h2>
            <p>다음 수업들에 자리가 생겼습니다:</p>
            <ul>
        """
        
        for course in courses:
            html_body += f"""
            <li>
                <strong>{course.get('course_name', course.get('course_number'))}</strong> 
                - 등록인원: {course.get('registered', 'N/A')}
            </li>
            """
        
        html_body += """
            </ul>
            <p>아래 이미지를 확인하세요.</p>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(html_body, 'html', 'utf-8'))
        
        # 스크린샷 첨부
        if screenshots:
            for i, screenshot_path in enumerate(screenshots):
                if os.path.exists(screenshot_path):
                    with open(screenshot_path, 'rb') as f:
                        img = MIMEImage(f.read())
                        img.add_header('Content-Disposition', 'attachment', 
                                     filename=f"course_{courses[i].get('course_number', i)}.png")
                        msg.attach(img)
        
        # 이메일 전송
        await aiosmtplib.send(
            msg,
            hostname=settings.smtp_host,
            port=settings.smtp_port,
            username=settings.smtp_user,
            password=settings.smtp_password,
            use_tls=True,
        )
    
    @staticmethod
    async def send_status_email(to_email: str, courses: List[dict]):
        """
        5분마다 크롤링 상태 확인 메일 전송
        """
        msg = MIMEMultipart()
        msg['From'] = settings.from_email
        msg['To'] = to_email
        msg['Subject'] = "✅ USC 수업 크롤러 상태 확인"
        
        html_body = f"""
        <html>
        <body>
            <h2>크롤러 상태 확인</h2>
            <p>크롤러가 정상적으로 작동 중입니다.</p>
            <p>현재 모니터링 중인 수업:</p>
            <ul>
        """
        
        for course in courses:
            status = "✅ 자리 있음" if course.get('is_available') else "❌ 만석"
            html_body += f"""
            <li>
                <strong>{course.get('course_name', course.get('course_number'))}</strong> 
                - 등록인원: {course.get('registered', 'N/A')} ({status})
            </li>
            """
        
        html_body += """
            </ul>
            <p>크롤러는 15초마다 확인 중입니다.</p>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(html_body, 'html', 'utf-8'))
        
        await aiosmtplib.send(
            msg,
            hostname=settings.smtp_host,
            port=settings.smtp_port,
            username=settings.smtp_user,
            password=settings.smtp_password,
            use_tls=True,
        )
