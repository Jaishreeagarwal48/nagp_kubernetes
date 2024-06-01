FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

# EXPOSE 2000

CMD ["python", "app.py"]