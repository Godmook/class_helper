# Railway 배포 문제 해결

## 현재 문제

Railway가 프로젝트 루트를 스캔하고 있어서 빌드 실패가 발생합니다.

## 해결 방법

### ✅ 방법 1: Railway 서비스 Settings에서 Root Directory 설정 (권장)

1. Railway 프로젝트 → **백엔드 서비스** 선택
2. **Settings** 탭 클릭
3. **Root Directory** 섹션 찾기
4. `backend` 입력하고 저장
5. **프론트엔드 서비스**도 동일하게 `frontend`로 설정

### ✅ 방법 2: 서비스 재생성

기존 서비스를 삭제하고 다시 추가:

1. **백엔드 서비스 생성**
   - "+ New" → "GitHub Repo"
   - 저장소 선택
   - ⚠️ **Root Directory**: `backend` 입력
   
2. **프론트엔드 서비스 생성**
   - "+ New" → "GitHub Repo"
   - 저장소 선택
   - ⚠️ **Root Directory**: `frontend` 입력

### ✅ 방법 3: Railway CLI 사용

```bash
# 프로젝트 연결
railway link

# 백엔드 서비스 배포 (backend 디렉토리로)
cd backend
railway up

# 프론트엔드 서비스 배포 (별도 서비스로)
cd ../frontend
railway up
```

## 확인 방법

서비스가 올바르게 설정되었는지 확인:

1. Railway 대시보드 → 서비스 선택
2. Settings 탭 → **Root Directory** 확인
   - 백엔드: `backend` 또는 `/backend`
   - 프론트엔드: `frontend` 또는 `/frontend`

3. 서비스별로 다음 파일들이 보여야 합니다:
   - 백엔드: `app/`, `requirements.txt`, `railway.json`
   - 프론트엔드: `src/`, `package.json`, `railway.json`

## 추가 파일 설명

프로젝트에 추가된 파일들:

- `.railwayignore`: Railway가 무시할 파일 목록
- `railway.toml`: 루트 설정 (사용하지 않음)
- `backend/nixpacks.toml`: 백엔드 빌드 설정
- `frontend/nixpacks.toml`: 프론트엔드 빌드 설정

## 여전히 문제가 발생하는 경우

1. Railway 대시보드에서 서비스를 완전히 삭제
2. 다시 생성하되, Root Directory를 **반드시** 설정
3. 환경 변수는 서비스 생성 후 Variables 탭에서 설정
