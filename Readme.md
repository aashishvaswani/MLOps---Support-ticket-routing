# 🧠 IT Support Ticket Classifier – Full MLOps Pipeline

A complete, production-ready **MLOps system** to classify IT service tickets into categories like Hardware, HR, and Access.

Designed as a final project for **CSE 816: Software Production Engineering**, this implementation showcases end-to-end DevOps and ML lifecycle automation, including observability, live patching, autoscaling, feedback-driven retraining, and secure CI/CD.

---

## 🚀 Key Features

- 🔁 **Live Feedback Loop + Auto-Retraining**
- 🐳 **Dockerized Microservices**: Frontend, Backend, ML Service, Retrainer
- ☸️ **Kubernetes Deployment with HPA**
- 🔐 **Secret Management with Vault (Optional)**
- 🔎 **Real-time Logging with ELK Stack**
- ⚙️ **Modular Ansible Roles for IaC**
- 🔄 **CI/CD with Jenkins + GitHub Webhooks**
- 📦 **Dynamic Model Hot Reloading**

---

## 🧰 Tech Stack Overview

| Category              | Tools/Tech Used                                                         |
|-----------------------|-------------------------------------------------------------------------|
| Version Control       | Git + GitHub                                                            |
| CI/CD Pipeline        | Jenkins + GitHub Webhook + Docker + Ansible + (Vault optional)          |
| Containerization      | Docker                                                                  |
| Orchestration         | Kubernetes + HPA + Ingress                                              |
| Configuration Mgmt    | Ansible (with roles)                                                    |
| Monitoring & Logging  | ELK Stack (Elasticsearch + Logstash + Kibana)                           |
| Secrets Management    | Vault (Optional)                                                        |
| Frontend              | React.js + NGINX                                                        |
| Backend               | Flask API with Logging + Feedback                                       |
| ML Service            | Scikit-learn + TF-IDF + LabelEncoder + Retraining                      |

---

## 📁 Folder Structure (Simplified)

```bash
.
├── backend/                  # Flask app: /predict + /feedback
├── frontend/                 # React UI + feedback form
├── ml_service/              # Inference + retraining + watcher
├── elk/logstash/            # logstash.conf config
├── k8s/                     # All deployment YAMLs + HPA + Ingress
├── ansible/                 # Infrastructure automation
├── Jenkinsfile              # CI/CD pipeline definition
├── docker-compose.yml       # Local dev setup (pre-K8s)
└── deploy-to-k8s.sh         # One-click K8s bootstrap script
```

---

## ⚙️ How to Deploy (K8s)

### Step 1: Start Minikube
```bash
minikube start
eval $(minikube docker-env)
```

### Step 2: Build Docker Images
```bash
docker build -t finalproject-backend ./backend
docker build -t finalproject-frontend ./frontend
docker build -t finalproject-ml-service ./ml_service
docker build -t finalproject-ml-service-retrain -f ml_service/Dockerfile.retrainer ./ml_service
```

### Step 3: Apply Kubernetes Manifests
```bash
kubectl apply -f k8s/elk/
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/mlservice-deployment.yaml
kubectl apply -f k8s/retrainer-deployment.yaml
kubectl apply -f k8s/backend-hpa.yaml
kubectl apply -f k8s/mlservice-hpa.yaml
kubectl apply -f k8s/ingress.yaml
```

### Step 4: Add Hostnames (for Ingress)
```bash
sudo vim /etc/hosts
# Add:
# 127.0.0.1 spe-frontend.com spe-backend.com spe-kibana.com
```

### Step 5: Access Services
| Service      | URL                             |
|--------------|----------------------------------|
| Frontend     | http://spe-frontend.com          |
| Backend      | http://spe-backend.com           |
| ML Service   | internal (K8s svc)               |
| Kibana       | http://spe-kibana.com            |

---

## 🔁 Feedback & Auto-Retraining

- Users provide corrections via the UI
- Entries stored in `feedback.jsonl`
- When count ≥ 10, `retrainer`:
  - Merges + deduplicates feedback with dataset
  - Triggers model retraining
  - Saves updated model in `/shared-model/`
- `ml-service` detects change and reloads new model (zero downtime)

---

## 🔎 Observability with ELK

- `python-json-logger` used in Flask
- Logstash reads logs via volume mount (`/tmp/shared-logs`)
- Kibana visualizes:
  - API hits
  - Errors
  - Feedback events
  - Retrain triggers

---

## 🔐 Jenkins CI/CD Pipeline

1. GitHub push triggers Jenkins build
2. Builds & tags Docker images
3. Runs unit tests in isolated Docker network
4. Pushes images to Docker Hub
5. Deploys via Ansible with optional Vault-secured credentials
6. Sends email on success/failure

---

## 🛠 Ansible Automation

- Role: `deploy_k8s` automates:
  - Minikube init
  - Docker image builds (via injected Docker env)
  - Enabling addons (metrics-server, ingress)
  - Applying all manifests
  - Waiting for readiness

---

🎉 **Deployed. Monitored. Retrained. Scaled.** All in one MLOps pipeline.

---

## 📌 Motivation and Problem Statement

In large IT organizations, support teams receive thousands of service tickets each day. Manually classifying and routing these tickets to the correct departments (HR, Access, Hardware, etc.) causes delays and increases resolution time. Misrouted tickets create additional backlogs and inefficiencies.

This project solves that with an **ML-powered, full-stack automated ticket classification system** that supports:

- 🔍 Real-time classification via ML API
- 💬 Interactive frontend for user interaction and feedback
- 🔁 Automated retraining pipeline based on user corrections
- 🧠 Scalable, production-ready deployment using Kubernetes and CI/CD

The entire system is **cloud-native**, observable, and capable of adapting to incoming feedback, improving over time.

---

## 🧪 Testing Strategy

- **Backend**: Unit tests using `pytest` for `/predict` and `/feedback` endpoints
- **Jenkins**: Runs test suite in a Docker container after every build
- **Frontend**: Basic rendering and form input testing using `App.test.js`
- **Load & Scaling**: Handled via Kubernetes HPA based on CPU utilization (auto-scales from 1 to 5 replicas for backend and ML service)
- **Log Validation**: Via structured JSON output parsed into Kibana dashboards

---

## 🧠 Machine Learning Model Details

- **Algorithm**: Logistic Regression (for interpretable linear classification)
- **Text Preprocessing**: Lowercasing, punctuation removal, whitespace trimming
- **Vectorization**: TF-IDF with top 500 features
- **Label Encoding**: Maps human-readable labels to numerical classes and back
- **Evaluation Metrics**: Accuracy, Classification Report, Support per Class
- **Retraining**:
  - Triggered when 10+ feedback samples are available
  - Deduplicates old + new data
  - Stores updated model in `/shared-model/` volume

---

## 📦 Docker Image Structure

| Service      | Base Image       | Purpose                             |
|--------------|------------------|-------------------------------------|
| Backend      | python:3.10-slim | Flask + Feedback API + Logger       |
| Frontend     | node:18 → nginx  | Build + Serve React App             |
| ML Service   | python:3.10-slim | Model Inference API                 |
| Retrainer    | python:3.10-slim | Watcher + Batch Retraining Pipeline |

All images are tagged and optionally pushed to DockerHub via Jenkins.

---

## 📊 Kibana Dashboards (Sample Insights)

- 📈 **Latency Tracking**: Time taken per prediction request
- 🚨 **Error Heatmaps**: Visualize failure hotspots
- 💬 **Feedback Logs**: Monitor frequency of corrections
- 📊 **Class Distribution**: Track which departments get most tickets
- 🔄 **Retrain Triggers**: When and how often retraining occurs

---

## 🧪 Performance Optimization

- Minimal memory footprints for ELK stack via container limits
- Model reloading via `watch_model()` runs on background thread
- React uses controlled form components with conditional rendering
- Docker images use `--no-cache-dir` and `alpine/slim` bases to reduce size
- Ansible ensures reproducibility with pre-checks and readiness waits

---