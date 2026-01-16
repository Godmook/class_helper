# Railway 배포 설정 가이드

## 1. PostgreSQL 데이터베이스 추가

1. Railway 프로젝트 대시보드에서 **"+ New"** 클릭
2. **"Database"** → **"Add PostgreSQL"** 선택
3. PostgreSQL이 추가되면 자동으로 `DATABASE_URL` 환경 변수가 설정됩니다.

## 2. 환경 변수 설정

Railway 프로젝트 대시보드에서 **"Variables"** 탭으로 이동하여 다음 환경 변수들을 추가하세요:

### 필수 환경 변수

```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
FROM_EMAIL=your_email@gmail.com
TERM_URL=https://classes.usc.edu/term/20261/catalogue/program/CSCI/school/ENGV
```

### Gmail 앱 비밀번호 생성 방법

1. Google 계정 설정 (https://myaccount.google.com) 접속
2. **보안** 메뉴로 이동
3. **2단계 인증** 활성화 (아직 안 했다면)
4. **앱 비밀번호** 생성
   - 검색창에서 "앱 비밀번호" 검색
   - 또는 직접: https://myaccount.google.com/apppasswords
5. "메일" 및 "기타(맞춤 이름)" 선택 후 "USC Crawler" 입력
6. 생성된 16자리 비밀번호를 복사하여 `SMTP_PASSWORD`에 입력

### 선택적 환경 변수

```
SECRET_KEY=your-random-secret-key-here (기본값: "change-me")
```

## 3. 배포 확인

환경 변수를 설정한 후, Railway가 자동으로 재배포합니다. 

**Deployments** 탭에서 배포 상태를 확인하세요.

## 4. 서비스 URL 확인

배포가 완료되면 **Settings** 탭에서 생성된 도메인 URL을 확인할 수 있습니다.

## 문제 해결

### 환경 변수 에러가 발생하는 경우
- Railway 대시보드 → Variables 탭에서 모든 필수 환경 변수가 설정되었는지 확인
- 변수 이름이 대문자인지 확인 (DATABASE_URL, SMTP_USER 등)
- PostgreSQL이 추가되었는지 확인 (DATABASE_URL이 자동 생성됨)

### 이메일 전송이 안 되는 경우
- SMTP_PASSWORD가 올바른 앱 비밀번호인지 확인
- Gmail에서 "보안 수준이 낮은 앱의 액세스"를 허용했는지 확인 (필요한 경우)
- SMTP_USER와 FROM_EMAIL이 같은 이메일인지 확인
