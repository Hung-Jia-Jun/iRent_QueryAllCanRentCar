FROM ubuntu:latest
WORKDIR /app
ADD . /app
RUN apt-get update -y && apt-get install -y python3-pip python3 build-essential libpq-dev
RUN bash install.sh
EXPOSE 8000
CMD python3 app.py
