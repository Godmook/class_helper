#!/bin/bash
set -e

echo "🚀 Starting USC Class Helper..."

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
uvicorn app.main:app --host 0.0.0.0 --port $PORT
