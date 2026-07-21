FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_PROJECT_ENVIRONMENT=/opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /workspace

# asyncmy 같은 패키지를 컴파일하기 위한 도구 설치
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential curl \
    && rm -rf /var/lib/apt/lists/*

# Python 패키지 관리 도구 uv 설치
RUN pip install --no-cache-dir uv

# 패키지 설정 파일 복사
COPY pyproject.toml uv.lock README.md ./

# 프로젝트에 필요한 Python 패키지 설치
RUN uv sync --frozen --no-dev --no-install-project

# FastAPI 코드 복사
COPY app /app

WORKDIR /

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]