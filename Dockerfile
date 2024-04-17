FROM python:3.10-slim 

WORKDIR /code

RUN pip install --upgrade pip

COPY ./requirements.txt /code/

RUN pip install -r /code/requirements.txt

COPY . .
