FROM python:3-alpine

WORKDIR /opt/home_io_backend

# install deps
ARG REQUIREMENTS
COPY ${REQUIREMENTS} .
RUN pip3 install -r ${REQUIREMENTS}

# copy files
COPY home_io_backend ./home_io_backend