FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /server
COPY requirements.txt /server/
RUN pip3 install -r requirements.txt
RUN apt-get update
RUN mkdir /var/log/tplanet_backend
COPY . /server/
