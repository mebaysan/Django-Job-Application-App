FROM python:3.9

WORKDIR /app

COPY . .

RUN make install