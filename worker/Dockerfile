FROM python:3.13-slim

# 빌드에 필요한 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    python3-dev \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

# llama-cpp-python 설치 (컴파일 시간이 다소 소요될 수 있습니다)
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python","-u","main.py"]