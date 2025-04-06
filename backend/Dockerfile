FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && \
    apt-get install -y tzdata && \
    ln -fs /usr/share/zoneinfo/Asia/Kolkata /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p logs

COPY . .

COPY ticket_classification_model.pkl .
COPY tfidf_vectorizer.pkl .

# Expose the Flask port
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
