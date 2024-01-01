FROM apache/airflow:2.6.1
USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
        vim \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
USER "${AIRFLOW_UID:-50000}:0"



# pamermill 에 쓰일 커널 설정
RUN pip install --upgrade pip ipython ipykernel
RUN ipython kernel install --name "python3" --user


# requirements.txt 복사
COPY requirements.txt .



# 필요한 Python 패키지 설치
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# 나머지 도커 파일 내용 추가...

