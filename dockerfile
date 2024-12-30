FROM python:3.12-alpine

RUN apk add --no-cache gcc musl-dev nmap

WORKDIR /app

COPY requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]

