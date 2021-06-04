FROM python:3.8

WORKDIR /app

COPY . .

# RUN apk update && apk add gcc

RUN pip install -r requirements.txt

CMD ["python", "app.py"]