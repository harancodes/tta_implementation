
# Lookit – E-Commerce Website (Two-Tier Architecture on AWS EKS)

This project is based on a **Git clone of the original Lookit E-Commerce repository developed by Abhinav Ashok**.

The purpose of cloning this project is **not to replicate the original deployment**, but to **use the application as a base to implement and demonstrate a production-style cloud architecture**.

In this implementation, the application is redesigned and deployed using a **Two-Tier Architecture on AWS Elastic Kubernetes Service (EKS)** to explore scalable DevOps practices.

---

## Project Purpose

The original repository provides a **full-stack Django e-commerce application**.
This cloned version is used as a **reference application to implement infrastructure architecture and DevOps workflows**.

Key goals of this implementation:

* Deploy the application using **containerized workloads**
* Implement **Two-Tier Architecture**
* Run the system on **AWS EKS (Kubernetes)**
* Demonstrate **cloud-native deployment practices**

---

## Architecture Overview

This implementation follows a **Two-Tier Architecture**:

### 1️⃣ Application Tier

Handles application logic and user requests.

Components:

* Django Application
* Gunicorn Application Server
* Nginx (reverse proxy)
* Docker containers
* Kubernetes Pods running on AWS EKS

Responsibilities:

* Process user requests
* Handle authentication
* Manage product catalog, cart, orders, and coupons
* Serve frontend templates

---

### 2️⃣ Data Tier

Handles persistent storage and database operations.

Components:

* PostgreSQL Database
* Persistent storage
* Kubernetes service for database access

Responsibilities:

* Store product data
* Manage user accounts
* Handle orders and transactions
* Maintain application state

---

## Technology Stack

### Frontend

* HTML
* CSS
* JavaScript
* Django Templates

### Backend

* Python
* Django
* Gunicorn

### Database

* PostgreSQL

### Containerization

* Docker

### Container Orchestration

* Kubernetes
* AWS EKS

### Infrastructure & Deployment

* AWS EKS
* Nginx (Reverse Proxy)
* Kubernetes Services & Deployments
* SSL via Certbot (Let's Encrypt)

---

## Key DevOps Concepts Implemented

* Containerized application using **Docker**
* Kubernetes deployments and services
* Two-tier application architecture
* Scalable infrastructure using **AWS EKS**
* Reverse proxy using **Nginx**
* Secure HTTPS deployment
* Infrastructure-ready project structure

