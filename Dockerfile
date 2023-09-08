FROM --platform=linux/x86_64 python:3.9

ENV PYTHONUNBUFFERED 1

COPY . /app/
WORKDIR /app

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
