FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

RUN mkdir -p model
COPY model/tfidf_vectorizer.pkl model/
COPY model/ticket_classification_model.pkl model/

EXPOSE 6000
CMD ["python", "app.py"]
