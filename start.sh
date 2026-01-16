#!/bin/bash
set -e

echo "🚀 Starting USC Class Helper..."
echo "Current directory: $(pwd)"
echo "PORT: $PORT"

# 프론트엔드가 이미 빌드되었는지 확인
if [ ! -d "frontend/dist" ]; then
    echo "📦 Building frontend..."
    npm install --prefix frontend
    npm run build --prefix frontend
else
    echo "✅ Frontend already built"
fi

# 백엔드 실행 (프론트엔드 빌드 파일 포함)
echo "🐍 Starting backend..."
cd backend
echo "Backend directory: $(pwd)"

# 가상환경 활성화
if [ -f "/app/venv/bin/activate" ]; then
    echo "Activating virtual environment..."
    source /app/venv/bin/activate
else
    echo "⚠️ Warning: Virtual environment not found at /app/venv"
fi

# Python 경로 확인
echo "Python: $(which python3)"
echo "Uvicorn: $(which uvicorn || echo 'not found')"

# 환경 변수 확인 (민감한 정보는 출력하지 않음)
echo "DATABASE_URL: ${DATABASE_URL:0:20}..."
echo "SMTP_USER: ${SMTP_USER}"

echo "Starting uvicorn on port $PORT..."

# 에러가 발생해도 로그를 확인할 수 있도록
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} --log-level info 2>&1
