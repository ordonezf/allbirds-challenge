FROM python:3.8-slim-buster

ENV PIP_ROOT_USER_ACTION=ignore
ENV PYTHONUNBUFFERED=1

WORKDIR /opt/app

RUN apt update && apt upgrade -y \
    && apt install -y gcc libpq-dev \
    && apt clean -y \
    && apt-get autoremove -yqq  --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src/ .

ENTRYPOINT [ "python", "main.py" ]
