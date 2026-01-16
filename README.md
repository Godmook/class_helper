# USC 수업 크롤러

USC 수업의 등록 가능 여부를 모니터링하고 이메일 알림을 보내주는 서비스입니다.

## 주요 기능

- ✅ 수업 번호로 자동 모니터링 등록
- ✅ 15초마다 자동 크롤링
- ✅ 자리가 생기면 즉시 이메일 알림
- ✅ 알림과 함께 스크린샷 이미지 제공
- ✅ 5분마다 크롤러 상태 확인 메일
- ✅ 크롤링 이력 저장 및 조회

## 설치 방법

1. 저장소 클론 및 이동
```bash
cd usc_class_helper
```

2. 가상환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. 의존성 설치
```bash
pip install -r requirements.txt
playwright install chromium
```

4. 환경 변수 설정
```bash
cp .env.example .env
# .env 파일을 열어서 필요한 정보를 입력하세요
```

## 환경 변수 설정

`.env` 파일에 다음 정보를 입력하세요:

- `DATABASE_URL`: PostgreSQL 데이터베이스 URL
- `SMTP_HOST`: SMTP 서버 주소 (기본값: smtp.gmail.com)
- `SMTP_PORT`: SMTP 포트 (기본값: 587)
- `SMTP_USER`: 이메일 계정
- `SMTP_PASSWORD`: 이메일 앱 비밀번호 (Gmail의 경우)
- `FROM_EMAIL`: 발신자 이메일 주소
- `TERM_URL`: 크롤링할 USC 수업 페이지 URL

### Gmail 설정

Gmail을 사용하는 경우:
1. Google 계정 설정 → 보안
2. 2단계 인증 활성화
3. 앱 비밀번호 생성
4. 생성된 비밀번호를 `SMTP_PASSWORD`에 입력

## 로컬 실행

1. PostgreSQL 데이터베이스 실행
2. 환경 변수 설정
3. 서버 실행:
```bash
uvicorn app.main:app --reload
```

4. 브라우저에서 `http://localhost:8000` 접속

## Railway 배포

1. Railway 프로젝트 생성
2. GitHub 저장소 연결
3. PostgreSQL 플러그인 추가
4. 환경 변수 설정 (Railway 대시보드에서)
5. 배포 자동 시작

## 사용 방법

1. 웹사이트에서 수업 번호와 이메일 입력
2. 수업 등록 완료
3. 15초마다 자동으로 크롤링 시작
4. 자리가 생기면 이메일 알림 수신
5. 5분마다 상태 확인 메일 수신

## 라이센스

MIT
