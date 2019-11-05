FROM python:3.7

ENV PYTHONUNBUFFERED 13

COPY ./requirements.txt /requirements.txt

RUN pip3 install -r requirements.txt --no-input
RUN mkdir /app mkdir /timestamps_dir

# VOLUME ../timestamps_dir ../timestamps_dir

WORKDIR /app

COPY ./src /app