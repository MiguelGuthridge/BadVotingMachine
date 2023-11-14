FROM python:3.10

WORKDIR /app

COPY requirements.txt /app
RUN pip install --extra-index-url http://localhost:8000 -r requirements.txt

COPY . /app

EXPOSE 8000

CMD ["gunicorn", "-c", "python:pyquocca.gunicorn", "app:app"]