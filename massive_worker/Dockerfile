FROM --platform=linux/amd64 python:3.10.7
RUN mkdir /backend
WORKDIR /backend
ADD requirements.txt /backend/
RUN pip install -r requirements.txt
ADD . /backend/
ENV PYTHONUNBUFFERED=1

CMD ["python", "init_bd.py", "&&", "python", "process.py"]