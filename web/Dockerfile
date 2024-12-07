FROM python:3.13
LABEL authors="d1ffic00lt"

WORKDIR /web

COPY . .

RUN pip install -r requirements.txt
RUN chmod +x ./entrypoint.sh

ENTRYPOINT ./entrypoint.sh
