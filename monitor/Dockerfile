FROM --platform=linux/amd64 python:3.10.16-slim

RUN mkdir .config_app
COPY credentials.json /.config_app/credentials.json
RUN export GOOGLE_APPLICATION_CREDENTIALS="/.config_app/credentials.json"
ENV GOOGLE_APPLICATION_CREDENTIALS="/.config_app/credentials.json"

COPY firebase-cred.json /.config_app/firebase-cred.json
ENV FIREBASE_PATH="/.config_app/firebase-cred.json"

WORKDIR app
COPY requirements.txt ./

RUN python --version
RUN pip install --upgrade --no-cache-dir pip==23.2.1
RUN pip --version
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 3025/tcp
ENV PYTHONUNBUFFERED=1
ENV TESTING=false

CMD [ "flask", "--app", ".", "run", "--host=0.0.0.0", "--port=3025" ]