FROM python:3.6
ADD . /demo
WORKDIR /demo
RUN pip install -r requirements.txt