FROM python:alpine
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
RUN apk update && apk add --no-cache \
    gcc \
    musl-dev \
    postgresql-dev

COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . /app/
EXPOSE 8000
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "moonbase_backend.asgi:application"]
