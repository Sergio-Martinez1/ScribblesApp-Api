FROM python:3.10.12-bullseye

WORKDIR /app

COPY prod.requirements.txt /app

RUN pip install --upgrade pip && pip install -r /app/prod.requirements.txt

EXPOSE 8080

COPY ./ /app

CMD ["python", "main.py"]
