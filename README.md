# 🏦 Intelligent Banking Support System (BankingAI)

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![PyTorch](https://img.shields.io/badge/PyTorch-2.2%2B-red.svg)
![Django](https://img.shields.io/badge/Django-REST_Framework-092E20.svg)
![AWS](https://img.shields.io/badge/AWS-Cloud_Native-FF9900.svg)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED.svg)
![React](https://img.shields.io/badge/React-Frontend-61DAFB.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

> **A Cloud-Native, Serverless AI solution that classifies customer support tickets with 78% accuracy across 77 distinct banking intents.**

---

## 📖 Table of Contents
- [Architecture](#-architecture)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Installation & Local Setup](#-installation--local-setup)
- [AWS Deployment Architecture](#-aws-deployment-architecture)
- [API Documentation](#-api-documentation)
- [Future Roadmap](#-future-roadmap)

---

## 🏗 Architecture

This project implements a **Microservices Architecture** to decouple the web application from the heavy AI inference logic, ensuring scalability and cost-efficiency.

```mermaid
graph LR
    User[User / Frontend] -- HTTPS --> LB[Nginx (Port 80)]
    LB --> Backend[Django Backend (EC2)]
    Backend -- SQL --> DB[(PostgreSQL RDS)]
    Backend -- JSON Payload --> Lambda[AWS Lambda (AI Brain)]
    Lambda -- Load Model --> ECR[Docker Container (ECR)]
    Lambda --> Backend