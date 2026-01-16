#!/bin/bash
set -e

echo "🚀 Starting USC Class Helper..."

# 프론트엔드 빌드
echo "📦 Building frontend..."
cd frontend
npm install
npm run build
cd ..

# 백엔드 실행 (프론트엔드 빌드 파일 포함)
echo "🐍 Starting backend..."
cd backend
playwright install chromium
uvicorn app.main:app --host 0.0.0.0 --port $PORT
