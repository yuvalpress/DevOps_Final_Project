FROM python:3.7-alpine

ADD . /code
WORKDIR /code

RUN pip install flask
RUN pip install pymysql
RUN pip install pypika

RUN chmod 644 rest_app.py

CMD ["python", "rest_app.py"]
