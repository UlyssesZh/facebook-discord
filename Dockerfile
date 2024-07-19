FROM python:3-alpine

RUN apk add --no-cache git gcc supercronic musl-dev

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir /data
VOLUME [ "/data" ]

COPY main.py .

COPY crontab .
CMD [ "supercronic", "crontab" ]
