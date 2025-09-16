# Cloud-Native URL Shortener: A DevOps & Kubernetes Showcase

This project is a fully containerized, two-tier URL shortener application designed to be deployed on Kubernetes. It consists of a Python Flask API and a Redis database.

---

## ## Vision & Purpose

The primary goal of this project is not to build the world's best URL shortener, but to serve as a practical, hands-on learning exercise for mastering the full cloud-native software lifecycle.

It is a portfolio piece designed to demonstrate core competencies in **DevOps methodologies**, **Kubernetes orchestration**, **containerization**, and **observability**. The "greater vision" is to use this simple application as a foundation to build out a complete, production-grade ecosystem with robust automation and monitoring.

---

## ## Architecture Overview

The application follows a simple microservice pattern:

* **Frontend/API (`Python/Flask`):** A stateless web service that handles API requests for creating and redirecting URLs.
* **Database (`Redis`):** A stateful key-value store that persists the mapping between short codes and long URLs.

All communication happens over the internal Kubernetes network.



---

## ## Core Technologies Demonstrated

* **Containerization:** Docker & Dockerfile (multi-stage builds)
* **Orchestration:** Kubernetes
* **Application:** Python (Flask)
* **Database:** Redis
* **Version Control:** Git & GitHub
* **Observability:** Prometheus (for metrics) & Grafana (for dashboards)
* **CI/CD:** GitHub Actions (Future Goal)

---

## ## How to Run Locally

You can test the application on your local machine using Docker.

**Prerequisites:**
* Docker
* Python 3.9+
* An active terminal

**Steps:**
1.  **Clone the repository:**
    ```sh
    git clone <your-repo-url>
    cd <your-repo-name>
    ```
2.  **Start the Redis container:**
    ```sh
    docker run --name local-redis -d -p 6379:6379 redis
    ```
3.  **Install Python dependencies:**
    ```sh
    pip install -r requirements.txt
    ```
4.  **Run the application:**
    ```sh
    python app.py
    ```
    The API will be available at `http://127.0.0.1:5000`.

---

## ## Future Goals & Roadmap

This project is the foundation. The next steps are to build out a complete, automated ecosystem around it:

* [ ] **CI/CD Pipeline:** Implement a full GitHub Actions workflow that automatically builds, tests, and deploys the application to Kubernetes on every commit to the `main` branch.
* [ ] **Kubernetes Manifests:** Develop robust `Deployment`, `Service`, and `StatefulSet` manifests for the application and database.
* [ ] **Full Observability Stack:** Deploy the "PLG" (Prometheus, Loki, Grafana) stack to the cluster to visualize metrics and aggregate logs.
* [ ] **Infrastructure as Code (IaC):** Use Terraform to provision the underlying Kubernetes cluster itself.
* [ ] **Distributed Tracing:** Add tools like Jaeger or Tempo to trace requests as they move between the API and the database.
