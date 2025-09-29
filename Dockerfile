FROM python:3.12-slim

WORKDIR /weatherapp


# no .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
# see logs instantly
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# use docker logs to see logs

CMD ["gunicorn","--workers=4","--bind=0.0.0.0:5000","--access-logfile","-","--error-logfile", "-","app:create_app"]
