FROM python:3.14-slim@sha256:81ada6cb56bcbe3909644b4cb76ebe5354c65eaaad788a437bc1340a7638d49d

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py ./

EXPOSE 5000

CMD ["python", "app.py"]
