FROM --platform=linux/amd64 python:3.10.7-slim

RUN mkdir .config_app
COPY credentials.json /.config_app/credentials.json
RUN export GOOGLE_APPLICATION_CREDENTIALS="/.config_app/credentials.json"
ENV GOOGLE_APPLICATION_CREDENTIALS="/.config_app/credentials.json"

RUN mkdir /backend
WORKDIR /backend
ADD requirements.txt /backend/
RUN pip install -r requirements.txt
ADD . /backend/
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/backend

CMD ["sh", "-c", "PYTHONPATH=/backend/.. python -m backend.init_bd && PYTHONPATH=/backend/.. python -m backend.process"]