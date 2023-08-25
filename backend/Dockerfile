FROM python:3.9

# set the working directory
WORKDIR /backend

COPY ./requirements.txt /backend/requirements.txt

RUN pip install -r /backend/requirements.txt

COPY ./app /backend/app


