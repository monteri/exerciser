FROM --platform=linux/x86_64 python:3.9

ENV PYTHONUNBUFFERED 1

COPY . /app/
WORKDIR /app

RUN apt-get update && apt-get install -y make \
    && make install

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
