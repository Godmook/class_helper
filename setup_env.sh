#!/bin/bash

# Railway 환경 변수 자동 설정 스크립트
# 이 스크립트는 제공된 Gmail 정보로 환경 변수를 설정합니다.

echo "Railway 환경 변수 설정 중..."
echo ""

# 제공된 Gmail 정보
SMTP_USER="cryptoboardtest@gmail.com"
SMTP_PASSWORD="!Qwer1234!"
FROM_EMAIL="cryptoboardtest@gmail.com"

# Railway CLI 확인
if ! command -v railway &> /dev/null; then
    echo "Railway CLI가 설치되지 않았습니다."
    echo "설치 중..."
    npm install -g @railway/cli
fi

# Railway 로그인 확인
if ! railway whoami &>/dev/null; then
    echo "Railway에 로그인이 필요합니다."
    echo "브라우저에서 로그인을 진행해주세요."
    railway login
fi

# 프로젝트 연결 확인
if [ ! -f ".railway/project.json" ]; then
    echo "Railway 프로젝트를 연결해주세요."
    railway link
fi

echo "환경 변수를 설정하는 중..."
echo ""

# Railway에 환경 변수 설정
railway variables set SMTP_HOST="smtp.gmail.com"
railway variables set SMTP_PORT="587"
railway variables set SMTP_USER="$SMTP_USER"
railway variables set SMTP_PASSWORD="$SMTP_PASSWORD"
railway variables set FROM_EMAIL="$FROM_EMAIL"
railway variables set TERM_URL="https://classes.usc.edu/term/20261/catalogue/program/CSCI/school/ENGV"

echo ""
echo "✅ 환경 변수 설정 완료!"
echo ""
echo "설정된 값:"
echo "  SMTP_USER: $SMTP_USER"
echo "  FROM_EMAIL: $FROM_EMAIL"
echo "  SMTP_PASSWORD: ********"
echo ""
echo "⚠️  참고:"
echo "  1. DATABASE_URL은 PostgreSQL 플러그인 추가 시 자동 설정됩니다."
echo "  2. Gmail 2단계 인증을 사용 중이라면 앱 비밀번호가 필요할 수 있습니다."
echo "     https://myaccount.google.com/apppasswords 에서 생성하세요."
echo "  3. 환경 변수는 Railway 대시보드에서도 확인/수정 가능합니다."
