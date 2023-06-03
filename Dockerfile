FROM python:3.10.10

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

ENV PYTHONUNBUFFERED=1

# CMD ["python", "-u", "main.py"]

CMD ["uvicorn", "--host", "192.168.1.2", "--port", "5000", "wsgi:app"]