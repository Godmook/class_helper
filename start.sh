#!/bin/bash

echo "========================================="
echo "🚀 USC Class Helper - Starting..."
echo "========================================="
echo "Current dir: $(pwd)"
echo "PORT: ${PORT:-8000}"
echo ""

# 프론트엔드 확인
if [ -d "frontend/dist" ]; then
    echo "✅ Frontend built"
else
    echo "⚠️ Frontend not built, skipping..."
fi

# 백엔드 디렉토리로 이동
cd backend || { echo "❌ Backend directory not found!"; exit 1; }
echo "✅ Changed to backend directory"

# 가상환경 확인 및 활성화
if [ -f "/app/venv/bin/activate" ]; then
    source /app/venv/bin/activate
    echo "✅ Virtual environment activated"
    PYTHON_CMD="python3"
    UVICORN_CMD="/app/venv/bin/uvicorn"
else
    echo "⚠️ Virtual env not found, using system Python"
    PYTHON_CMD="python3"
    UVICORN_CMD="python3 -m uvicorn"
fi

# uvicorn 경로 확인
if command -v uvicorn >/dev/null 2>&1; then
    echo "✅ uvicorn found: $(which uvicorn)"
    UVICORN_CMD="uvicorn"
elif [ -f "/app/venv/bin/uvicorn" ]; then
    echo "✅ uvicorn found: /app/venv/bin/uvicorn"
    UVICORN_CMD="/app/venv/bin/uvicorn"
else
    echo "⚠️ uvicorn not in PATH, using python3 -m"
    UVICORN_CMD="python3 -m uvicorn"
fi

echo ""
echo "Starting server..."
echo "Command: $UVICORN_CMD app.main:app --host 0.0.0.0 --port ${PORT:-8000}"
echo ""

# 서버 시작
$UVICORN_CMD app.main:app --host 0.0.0.0 --port "${PORT:-8000}" --log-level info
