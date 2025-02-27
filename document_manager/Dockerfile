FROM python:3.10.16

WORKDIR app
COPY requirements.txt ./

RUN python --version
RUN pip install --upgrade --no-cache-dir pip==23.2.1
RUN pip --version
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 3003/tcp

CMD [ "flask", "--app", ".", "run", "--host=0.0.0.0", "--port=3003" ]