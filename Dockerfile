FROM python:3.13.0

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .



EXPOSE 8080

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8080", "main:app"]
