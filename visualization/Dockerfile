FROM python:3.11-slim

WORKDIR /app

COPY uploader.py .

RUN pip install requests

CMD ["python", "uploader.py"]
