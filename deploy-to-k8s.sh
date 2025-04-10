#!/bin/bash

echo "▶ Switching Docker to Minikube context..."
eval $(minikube docker-env)

echo "Building Docker images inside Minikube..."
docker build -t finalproject-backend ./backend
docker build -t finalproject-frontend ./frontend
docker build -t finalproject-ml-service ./ml_service

echo "Applying ELK Stack (Elasticsearch, Kibana, Logstash)..."
kubectl apply -f k8s/elk/logstash-configmap.yaml
kubectl apply -f k8s/elk/elasticsearch-deployment.yaml
kubectl apply -f k8s/elk/kibana-deployment.yaml
kubectl apply -f k8s/elk/logstash-deployment.yaml

echo "Deploying Core App Services..."
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/mlservice-deployment.yaml
kubectl apply -f k8s/frontend-deployment.yaml

echo "Applying HPA Policies..."
kubectl apply -f k8s/backend-hpa.yaml
kubectl apply -f k8s/mlservice-hpa.yaml

echo "Deployment to Kubernetes completed successfully!"
