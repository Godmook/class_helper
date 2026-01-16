# Railway 배포 가이드 (멀티 서비스)

## 문제 해결: Nixpacks Build Failed

Railway가 프로젝트 루트를 보면서 어떤 언어/프레임워크를 사용할지 알 수 없어 발생하는 문제입니다.

## 올바른 배포 방법

Railway에서 **각 서비스를 별도로** 배포해야 합니다. 각 서비스는 **Root Directory**를 지정해서 배포합니다.

---

## 1단계: PostgreSQL 데이터베이스 추가

1. Railway 프로젝트 → **"+ New"**
2. **"Database"** → **"Add PostgreSQL"** 선택
3. ✅ `DATABASE_URL` 자동 설정됨

---

## 2단계: 백엔드 서비스 배포

### 방법 A: GitHub Repo로 추가

1. Railway 프로젝트 → **"+ New"**
2. **"GitHub Repo"** 선택
3. `Godmook/class_helper` 저장소 선택
4. ⚠️ **중요**: **"Root Directory"**를 `backend`로 설정
5. Railway가 자동으로 Python 프로젝트 인식

### 방법 B: 기존 서비스 수정

1. 기존 서비스 → **Settings** 탭
2. **"Root Directory"** 섹션에서 `backend` 입력
3. 저장

### 환경 변수 설정 (백엔드 서비스)

백엔드 서비스의 **Variables** 탭에서:

```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=cryptoboardtest@gmail.com
SMTP_PASSWORD=!Qwer1234!
FROM_EMAIL=cryptoboardtest@gmail.com
TERM_URL=https://classes.usc.edu/term/20261/catalogue/program/CSCI/school/ENGV
```

> 💡 `DATABASE_URL`은 PostgreSQL 추가 시 자동으로 설정됩니다.

---

## 3단계: 프론트엔드 서비스 배포

1. Railway 프로젝트 → **"+ New"**
2. **"GitHub Repo"** 선택
3. `Godmook/class_helper` 저장소 선택
4. ⚠️ **중요**: **"Root Directory"**를 `frontend`로 설정
5. Railway가 자동으로 Node.js 프로젝트 인식

### 환경 변수 설정 (프론트엔드 서비스 - 선택사항)

프론트엔드 서비스의 **Variables** 탭에서:

```
VITE_API_URL=https://your-backend-service.railway.app
```

> 백엔드 서비스의 도메인을 확인해서 설정하세요.

---

## 4단계: 확인

각 서비스가 정상적으로 배포되었는지 확인:

- ✅ 백엔드: `/api/health` 엔드포인트 확인
- ✅ 프론트엔드: 메인 페이지 확인
- ✅ PostgreSQL: 데이터베이스 연결 확인

---

## 중요한 설정

### Root Directory 설정

Railway에서 각 서비스를 추가할 때 반드시 **Root Directory**를 지정해야 합니다:

- **백엔드 서비스**: `backend`
- **프론트엔드 서비스**: `frontend`

이렇게 하면 Railway가 각 디렉토리의 `railway.json`, `requirements.txt`, `package.json` 등을 올바르게 인식합니다.

---

## 문제 해결

### "Nixpacks build failed" 에러

- ❌ 루트에 `railway.json`이 있거나 Root Directory가 설정되지 않음
- ✅ 각 서비스의 Root Directory를 `backend` 또는 `frontend`로 설정

### "No build plan" 에러

- Root Directory가 올바르게 설정되었는지 확인
- `backend/` 디렉토리에 `requirements.txt` 확인
- `frontend/` 디렉토리에 `package.json` 확인

### 환경 변수 에러

- 백엔드 서비스의 Variables 탭에서 모든 필수 환경 변수 확인
- PostgreSQL이 추가되었는지 확인 (DATABASE_URL 자동 생성)
