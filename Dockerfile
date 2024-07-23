FROM python:3.11-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt clean && apt update && apt install curl netcat vim gettext -y

WORKDIR /my_code
COPY . /my_code/

RUN pip install -r requirements.txt

RUN #cp .env.example .env

COPY .deploy/entrypoint.sh /
RUN chmod +x /entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["sh", "/entrypoint.sh"]