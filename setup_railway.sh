#!/bin/bash

# Railway 환경 변수 설정 스크립트
# 사용법: ./setup_railway.sh

echo "Railway 환경 변수 설정"
echo "======================"
echo ""

# Railway 로그인 확인
if ! railway whoami &>/dev/null; then
    echo "Railway에 로그인이 필요합니다."
    railway login
fi

# 프로젝트 연결 확인
if [ ! -f ".railway/project.json" ]; then
    echo "Railway 프로젝트를 연결해주세요."
    railway link
fi

# 환경 변수 값 입력받기
read -p "SMTP_USER (이메일 주소): " SMTP_USER
read -sp "SMTP_PASSWORD (앱 비밀번호): " SMTP_PASSWORD
echo ""
read -p "FROM_EMAIL (발신자 이메일): " FROM_EMAIL
read -p "TERM_URL [기본값: https://classes.usc.edu/term/20261/catalogue/program/CSCI/school/ENGV]: " TERM_URL
TERM_URL=${TERM_URL:-"https://classes.usc.edu/term/20261/catalogue/program/CSCI/school/ENGV"}

# Railway에 환경 변수 설정
echo ""
echo "환경 변수를 설정하는 중..."

railway variables set SMTP_HOST="smtp.gmail.com"
railway variables set SMTP_PORT="587"
railway variables set SMTP_USER="$SMTP_USER"
railway variables set SMTP_PASSWORD="$SMTP_PASSWORD"
railway variables set FROM_EMAIL="$FROM_EMAIL"
railway variables set TERM_URL="$TERM_URL"

echo ""
echo "✅ 환경 변수 설정 완료!"
echo ""
echo "참고: DATABASE_URL은 PostgreSQL 플러그인을 추가하면 자동으로 설정됩니다."
