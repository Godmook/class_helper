#!/bin/bash

echo "🚀 Starting USC Class Helper..."
echo "Current directory: $(pwd)"
echo "PORT: ${PORT:-8000}"

# 프론트엔드가 이미 빌드되었는지 확인
if [ ! -d "frontend/dist" ]; then
    echo "📦 Building frontend..."
    npm install --prefix frontend || true
    npm run build --prefix frontend || true
else
    echo "✅ Frontend already built"
fi

# 백엔드 실행 (프론트엔드 빌드 파일 포함)
echo "🐍 Starting backend..."
cd backend || exit 1
echo "Backend directory: $(pwd)"

# 가상환경 활성화
if [ -f "/app/venv/bin/activate" ]; then
    echo "✅ Activating virtual environment..."
    source /app/venv/bin/activate
    export PATH="/app/venv/bin:$PATH"
else
    echo "⚠️ Warning: Virtual environment not found at /app/venv"
fi

# Python 경로 확인
echo "Python: $(which python3 || which python)"
echo "Uvicorn: $(which uvicorn || echo 'not found')"

# 환경 변수 확인
echo "DATABASE_URL: ${DATABASE_URL:0:30}..."
echo "SMTP_USER: ${SMTP_USER:-not set}"

# 포트 설정
PORT="${PORT:-8000}"
echo "Starting uvicorn on port $PORT..."

# 서버 시작 (에러가 발생해도 로그 출력)
python3 -m uvicorn app.main:app --host 0.0.0.0 --port "$PORT" --log-level info || {
    echo "❌ Uvicorn failed, trying alternative..."
    /app/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port "$PORT" --log-level info || {
        echo "❌ All attempts failed"
        exit 1
    }
}
