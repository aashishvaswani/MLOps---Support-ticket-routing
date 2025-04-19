# IT Service Ticket Classifier – Full MLOps Pipeline

This project implements a production-grade **MLOps pipeline** for classifying IT support tickets into categories like Hardware, HR, and Access. It combines a Flask backend (serving a machine learning model), a React frontend, and a full DevOps lifecycle with real-time observability, feedback-driven retraining, and automated CI/CD. The system is designed with containerization, secure secret management, scalable orchestration, and modular infrastructure automation.
---

## Project Highlights

- **CI/CD with Jenkins**, Docker, and Kubernetes
- **Model Feedback Loop + Auto-Retraining**
- **Microservice Architecture**: Frontend, Backend, Model API, Retrainer
- **ELK Stack** for real-time logs from Flask
- **Secrets Managed with Vault**
- **Kubernetes HPA for Scalability**
- **Ansible Roles** for modular deployment

---

## Tech Stack

| Category              | Tools/Tech Used                                                         |
|-----------------------|-------------------------------------------------------------------------|
| Version Control       | Git + GitHub                                                            |
| CI/CD Pipeline        | Jenkins + GitHub Webhook + Docker + Ansible                             |
| Containerization      | Docker                                                                  |
| Orchestration         | Kubernetes + HPA                                                        |
| Configuration Mgmt    | Ansible (with roles)                                                    |
| Monitoring & Logging  | ELK Stack (Elasticsearch + Logstash + Kibana)                           |
| Secrets Management    | Vault                                                                   |
| Frontend              | React.js + NGINX                                                        |
| Backend               | Flask + Logging + Feedback API                                          |
| ML Service            | Scikit-learn + TF-IDF + LabelEncoder                                    |

---

## Folder Structure

```bash
.
├── .vscode/                         # Editor configs
├── ansible/                         # Configuration management with roles
│   ├── inventory.ini
│   ├── playbook.yaml
│   └── roles/
│       ├── deploy_compose/
│       └── deploy_k8s/
├── backend/                         # Flask backend
│   ├── logs/                        # JSON logs for ELK
│   │   ├── app.log
│   │   ├── app.log.1
│   │   └── completed.log
│   ├── tests/
│   ├── venv/
│   ├── app.py
│   ├── logger_config.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .dockerignore
├── elk/                             # Local ELK setup
│   ├── kibana/kibana.yml
│   └── logstash/logstash.conf
├── frontend/                        # React app served via NGINX
│   ├── build/
│   ├── public/
│   ├── src/
│   │   ├── App.js
│   │   ├── App.test.js
│   │   ├── index.js
│   │   └── ...
│   ├── Dockerfile
│   ├── .env
│   └── package.json
├── k8s/                             # All Kubernetes manifests
│   ├── elk/
│   │   ├── elasticsearch-deployment.yaml
│   │   ├── kibana-deployment.yaml
│   │   ├── logstash-configmap.yaml
│   │   └── logstash-deployment.yaml
│   ├── backend-deployment.yaml
│   ├── backend-hpa.yaml
│   ├── frontend-deployment.yaml
│   ├── retrainer-deployment.yaml
│   ├── mlservice-deployment.yaml
│   └── mlservice-hpa.yaml
├── ml_service/                      # Model inference and retraining
│   ├── logs/feedback.jsonl
│   ├── all_tickets_processed_improved_v3.csv
│   ├── app.py
│   ├── model_script.py
│   ├── retrain.py
│   ├── tfidf_vectorizer.pkl
│   ├── ticket_classification_model.pkl
│   ├── Dockerfile
│   └── Dockerfile.retrainer
├── Jenkinsfile                      # CI/CD pipeline
├── docker-compose.yml               # Local setup for ELK/Dev testing
├── deploy-to-k8s.sh                 # One-click deployment script
├── .gitignore
└── README.md

```

## How to Run

### 1. Start Minikube
```bash
minikube start
eval $(minikube docker-env)
```

### 2. Build All Docker Images
```bash
docker build -t finalproject-backend ./backend
docker build -t finalproject-frontend ./frontend
docker build -t finalproject-ml-service ./ml_service
docker build -t finalproject-ml-service-retrain -f ml_service/Dockerfile.retrainer ./ml_service
```

### 3. Deploy Services to Kubernetes
```bash
kubectl apply -f k8s/elk/
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/mlservice-deployment.yaml
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/retrainer-deployment.yaml
```

### 4. Apply Autoscaling (HPA)
```bash
kubectl apply -f k8s/backend-hpa.yaml
kubectl apply -f k8s/mlservice-hpa.yaml
```

### 5. Port Forwarding
```bash
kubectl port-forward svc/frontend-service 3000:80 &
kubectl port-forward svc/backend-service 5000:5000 &
kubectl port-forward svc/ml-service 6000:6000 &
kubectl port-forward svc/kibana-service 5601:5601 &
```

---

## Access Points

| Service      | URL                      |
|--------------|---------------------------|
| Frontend     | [http://localhost:3000](http://localhost:3000) |
| Backend      | [http://localhost:5000](http://localhost:5000) |
| ML Service   | [http://localhost:6000](http://localhost:6000) |
| Kibana       | [http://localhost:5601](http://localhost:5601) |

---

## Feedback Loop and Retraining

- User submits feedback for incorrect classifications.
- Feedback is stored in `ml_service/logs/feedback.jsonl`.
- Once 10+ entries are collected:
  - A retrainer pod is triggered.
  - The model is retrained using both existing and new data.
  - The updated model replaces the previous one in production.

---

## Observability with Kibana

- Flask backend logs are streamed via Logstash into Elasticsearch.
- Kibana dashboard visualizes:
  - Incoming API requests
  - Error rates
  - Feedback entries
  - Retrain trigger events

Access Kibana at: [http://localhost:5601](http://localhost:5601)

---

## Live Patching (Zero Downtime)

To reflect frontend changes (e.g., after editing `App.js`):

```bash
docker build -t finalproject-frontend ./frontend
kubectl rollout restart deployment frontend