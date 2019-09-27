FROM python:3-alpine

WORKDIR /opt/home_io_backend

# install deps
ARG REQUIREMENTS
COPY ${REQUIREMENTS} .
RUN pip3 install -r ${REQUIREMENTS}

# copy files
COPY env.py .
COPY config/config.py ./home_io_backend/config.py