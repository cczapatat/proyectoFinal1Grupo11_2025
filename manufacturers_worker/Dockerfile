FROM --platform=linux/amd64 python:3.9-slim

RUN mkdir .config_app
COPY credentials.json /.config_app/credentials.json
RUN export GOOGLE_APPLICATION_CREDENTIALS="/.config_app/credentials.json"
ENV GOOGLE_APPLICATION_CREDENTIALS="/.config_app/credentials.json"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
ENV PYTHONUNBUFFERED=1

CMD ["python", "-m", "src.main"]