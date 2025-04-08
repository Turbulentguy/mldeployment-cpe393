FROM python:3.9-slim

WORKDIR /app

COPY app/ /app/

COPY app/model.pkl /app/model.pkl

COPY app/linear_model.pkl /app/linear_model.pkl

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 9000

CMD ["python", "app.py"]
