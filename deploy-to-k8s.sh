#!/bin/bash

echo "Switching Docker to Minikube context..."
eval $(minikube docker-env)

echo "Starting Minikube (if not already running)..."
minikube status >/dev/null 2>&1 || minikube start

echo "Building Docker images inside Minikube..."
docker build -t finalproject-backend ./backend
docker build -t finalproject-frontend ./frontend
docker build -t finalproject-ml-service ./ml_service
docker build -t finalproject-ml-service-retrain -f ml_service/Dockerfile.retrainer ./ml_service

echo "Applying ELK Stack (Elasticsearch, Kibana, Logstash)..."
kubectl apply -f k8s/elk/logstash-configmap.yaml
kubectl apply -f k8s/elk/elasticsearch-deployment.yaml
kubectl apply -f k8s/elk/kibana-deployment.yaml
kubectl apply -f k8s/elk/logstash-deployment.yaml

echo "Deploying Core App Services..."
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/mlservice-deployment.yaml
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/retrainer-deployment.yaml
kubectl apply -f k8s/ingress.yaml

echo "Applying HPA Policies..."
kubectl apply -f k8s/backend-hpa.yaml
kubectl apply -f k8s/mlservice-hpa.yaml

echo "Waiting for all pods to be ready..."
kubectl wait --for=condition=Ready pods --all --timeout=300s

# echo "Starting port-forwarding..."
# pkill -f "kubectl port-forward" >/dev/null 2>&1

sleep 5
# kubectl port-forward svc/backend-service 5000:5000 &
# kubectl port-forward svc/frontend-service 3000:3000 &
# kubectl port-forward svc/ml-service 6000:6000 &
# kubectl wait --for=condition=ready pod -l app=kibana --timeout=60s
# kubectl port-forward svc/kibana-service 5601:5601 &

echo "Deployment to Kubernetes completed successfully!"
# echo "Services available at:"
# echo "   ▪ Backend:     http://localhost:5000"
# echo "   ▪ Frontend:    http://localhost:3000"
# echo "   ▪ ML Service:  http://localhost:6000"
# echo "   ▪ Kibana:      http://localhost:5601"
