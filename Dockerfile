FROM python:3.9-slim-buster

WORKDIR /app/FashionCampus

RUN python -m pip install gunicorn

COPY requirements.torch.txt .
RUN python -m pip install -r requirements.torch.txt --extra-index-url https://download.pytorch.org/whl/cpu

COPY requirements.nn.txt .
RUN python -m pip install -r requirements.nn.txt

RUN apt update
RUN apt install -y libgl1
RUN apt install -y libglib2.0-0

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

COPY . .

EXPOSE 8000

ENV PYTHONPATH="/app"

CMD [ "python", "-m", "gunicorn", "api:app"]
