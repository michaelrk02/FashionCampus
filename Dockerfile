FROM python:3.9-slim-buster

WORKDIR /app/FashionCampus

COPY requirements.txt .
RUN python -m pip install gunicorn
RUN python -m pip install -r requirements.txt

COPY . .

EXPOSE 8000

ENV PYTHONPATH="/app"

CMD [ "python", "-m", "gunicorn", "api:app"]
