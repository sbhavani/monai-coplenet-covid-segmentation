FROM pytorch/pytorch
#python:3.8-slim

RUN apt update
#RUN apt install build-essential -y
RUN apt install libgdcm-tools git emacs -y

COPY requirements.txt /

RUN pip install --no-cache-dir -r /requirements.txt

COPY *.py /app/

WORKDIR /app

RUN mkdir {model,images,output,patients}
