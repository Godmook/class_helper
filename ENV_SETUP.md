# 환경 변수 설정 가이드

## 제공된 Gmail 계정 정보

```
SMTP_USER: cryptoboardtest@gmail.com
SMTP_PASSWORD: !Qwer1234!
FROM_EMAIL: cryptoboardtest@gmail.com
```

## Railway에서 환경 변수 설정하는 방법

### 방법 1: Railway 대시보드에서 수동 설정

1. Railway 프로젝트 대시보드로 이동
2. **백엔드 서비스** 선택 → **Variables** 탭 클릭
3. 다음 환경 변수들을 추가:

```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=cryptoboardtest@gmail.com
SMTP_PASSWORD=!Qwer1234!
FROM_EMAIL=cryptoboardtest@gmail.com
TERM_URL=https://classes.usc.edu/term/20261/catalogue/program/CSCI/school/ENGV
```

### 방법 2: Railway CLI로 자동 설정

```bash
./setup_env.sh
```

또는 직접 명령어로:

```bash
railway variables set SMTP_USER="cryptoboardtest@gmail.com"
railway variables set SMTP_PASSWORD="!Qwer1234!"
railway variables set FROM_EMAIL="cryptoboardtest@gmail.com"
railway variables set SMTP_HOST="smtp.gmail.com"
railway variables set SMTP_PORT="587"
railway variables set TERM_URL="https://classes.usc.edu/term/20261/catalogue/program/CSCI/school/ENGV"
```

## 중요 사항

### ⚠️ Gmail 2단계 인증 사용 시

Gmail에서 2단계 인증을 활성화한 경우, 일반 비밀번호 대신 **앱 비밀번호**를 사용해야 합니다.

1. [앱 비밀번호 생성](https://myaccount.google.com/apppasswords)
2. "메일" 선택, "USC Crawler" 입력
3. 생성된 16자리 비밀번호를 `SMTP_PASSWORD`에 사용

### DATABASE_URL

PostgreSQL 플러그인을 Railway에서 추가하면 `DATABASE_URL`이 **자동으로 설정**됩니다.

1. Railway 프로젝트 → "+ New" → "Add PostgreSQL"
2. DATABASE_URL 자동 생성 ✅

## 환경 변수 확인

Railway 대시보드에서 Variables 탭을 통해 설정된 모든 환경 변수를 확인할 수 있습니다.
