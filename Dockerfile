FROM python:3.11.0a6-alpine
LABEL org.opencontainers.image.source=https://github.com/tomswartz07/AdventOfCodeLeaderboard
LABEL org.opencontainers.image.authors="tom+docker@tswartz.net"
LABEL description="Docker container to run a Slack bot which posts daily \
updates on the Advent of Code leaderboard."


COPY crontab .
RUN crontab crontab
COPY leaderboard.py .
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "crond", "-f" ]
