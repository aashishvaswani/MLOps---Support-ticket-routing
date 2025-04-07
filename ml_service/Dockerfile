FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ticket_classification_model.pkl .
COPY tfidf_vectorizer.pkl .
COPY app.py .

EXPOSE 6000

CMD ["python", "app.py"]
