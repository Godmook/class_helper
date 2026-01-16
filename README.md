# USC 수업 크롤러

USC 수업의 등록 가능 여부를 모니터링하고 이메일 알림을 보내주는 서비스입니다.

## 🎯 주요 기능

- ✅ **React 기반 모던한 웹 UI**
- ✅ **FastAPI 백엔드 API**
- ✅ 수업 번호로 자동 모니터링 등록
- ✅ 15초마다 자동 크롤링
- ✅ 자리가 생기면 즉시 이메일 알림
- ✅ 알림과 함께 스크린샷 이미지 제공
- ✅ 5분마다 크롤러 상태 확인 메일
- ✅ 크롤링 이력 저장 및 조회

## 📁 프로젝트 구조

```
usc_class_helper/
├── backend/          # FastAPI 백엔드
│   ├── app/
│   │   ├── main.py   # API 엔드포인트
│   │   ├── crawler.py
│   │   ├── scheduler.py
│   │   └── ...
│   └── requirements.txt
├── frontend/         # React 프론트엔드
│   ├── src/
│   │   ├── App.jsx
│   │   └── ...
│   └── package.json
└── README.md
```

## 🚀 Railway 배포

Railway에서 자동으로 백엔드, 프론트엔드, 데이터베이스를 배포합니다.

### 1. Railway 프로젝트 생성

1. [Railway](https://railway.app)에 로그인
2. "New Project" 클릭
3. "Deploy from GitHub repo" 선택
4. `Godmook/class_helper` 저장소 선택

### 2. PostgreSQL 데이터베이스 추가

1. Railway 프로젝트에서 **"+ New"** 클릭
2. **"Database"** → **"Add PostgreSQL"** 선택
3. PostgreSQL 추가 시 **DATABASE_URL이 자동으로 설정됩니다** ✨

### 3. 백엔드 서비스 추가

1. GitHub 저장소 → **backend/** 디렉토리 선택
2. 또는 Railway에서 **"+ New"** → **"GitHub Repo"** → `backend` 디렉토리 선택

### 4. 프론트엔드 서비스 추가

1. Railway에서 **"+ New"** → **"GitHub Repo"** → `frontend` 디렉토리 선택

### 5. 환경 변수 설정

**백엔드 서비스**의 Variables 탭에서:

```
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
FROM_EMAIL=your_email@gmail.com
```

> 💡 **DATABASE_URL**은 PostgreSQL 플러그인 추가 시 자동으로 설정됩니다!

### 6. 프론트엔드 환경 변수 (선택사항)

프론트엔드 서비스의 Variables 탭에서:

```
VITE_API_URL=https://your-backend-url.railway.app
```

> 백엔드 URL은 Railway에서 생성된 백엔드 서비스의 도메인을 사용하세요.

## 📧 Gmail 앱 비밀번호 생성

1. [Google 계정 설정](https://myaccount.google.com) 접속
2. **보안** → **2단계 인증** 활성화
3. **앱 비밀번호** 생성: https://myaccount.google.com/apppasswords
4. "메일" 선택, "USC Crawler" 입력
5. 생성된 16자리 비밀번호를 `SMTP_PASSWORD`에 입력

## 🛠️ 로컬 개발

### 백엔드 실행

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium

# .env 파일 생성 (DATABASE_URL, SMTP_USER 등 설정)
uvicorn app.main:app --reload
```

### 프론트엔드 실행

```bash
cd frontend
npm install
npm run dev
```

## 🎨 기술 스택

- **Frontend**: React 18, Vite, Axios
- **Backend**: FastAPI, Python 3.11
- **Database**: PostgreSQL
- **Crawling**: Playwright
- **Scheduling**: APScheduler
- **Email**: SMTP (Gmail)
- **Deployment**: Railway

## 📝 사용 방법

1. 웹사이트 접속
2. 수업 번호 (예: 535)와 이메일 입력
3. 수업 등록 완료
4. 15초마다 자동으로 크롤링 시작
5. 자리가 생기면 이메일 알림 수신 ✉️
6. 5분마다 상태 확인 메일 수신

## 📚 더 자세한 가이드

- [Railway 설정 가이드](RAILWAY_SETUP.md)

## 📄 라이센스

MIT
