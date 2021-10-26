FROM python:3-alpine
LABEL org.opencontainers.image.authors="tom+docker@tswartz.net"
LABEL description="Docker container to run a Slack bot which posts daily \
updates on the Advent of Code leaderboard."


COPY leaderboard.py .
COPY requirements.txt .
COPY crontab .
RUN pip install --no-cache-dir -r requirements.txt

RUN crontab crontab

CMD [ "crond", "-f" ]
