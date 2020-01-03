FROM python:3-alpine

WORKDIR /opt/home_io_faas/

RUN pip3 install requests

COPY home_io_sdk ./home_io_sdk
COPY script.py .

CMD ["python3", "script.py"]
