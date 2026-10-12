from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from api.auth import get_current_user
from models.user import User

router = APIRouter()

# Structured roadmap templates for key canonical skills & fallback generator for any skill
SKILL_ROADMAP_DATABASE = {
    "docker": {
        "skill": "Docker",
        "overview": "Master containerization from fundamentals to multi-container production deployments using Docker and Docker Compose.",
        "prerequisites": ["Linux CLI Basics", "Basic Networking Concepts", "HTTP Protocol"],
        "stages": [
            {
                "level": "Basic",
                "topics": ["What is Docker?", "Containers vs Virtual Machines", "Images vs Containers", "Docker Architecture & CLI"],
                "tasks": ["Install Docker Engine & Desktop", "Run `docker run hello-world`", "Inspect container status with `docker ps`"],
                "project": "Run Nginx container locally and map port 8080"
            },
            {
                "level": "Intermediate",
                "topics": ["Dockerfile Directives (FROM, WORKDIR, COPY, RUN, EXPOSE, CMD)", "Layer Caching & Multi-stage Builds", "Port Mapping & Environment Variables", "Docker Volumes & Persistent Storage"],
                "tasks": ["Write a Dockerfile for a FastAPI/Node application", "Build image using `docker build -t app:v1 .`", "Mount host directory as volume for live reload"],
                "project": "Containerize Career Compass AI FastAPI Backend"
            },
            {
                "level": "Advanced",
                "topics": ["Docker Compose Configuration", "Multi-container Applications (Frontend + Backend + DB)", "Custom Bridge Networks & DNS", "Image Security Scanning & Non-root Users", "CI/CD Deployment Pipelines"],
                "tasks": ["Define docker-compose.yml with React frontend, FastAPI backend, and PostgreSQL DB", "Run `docker-compose up --build`", "Optimize Docker image size under 150MB"],
                "project": "Full-Stack Microservices Dockerization with Automated Health Checks"
            }
        ],
        "handsOnProjects": [
            "Mini Project: Single-container Web App Package",
            "Capstone Project: Multi-container Production Stack with Docker Compose"
        ],
        "assessment": {"mcqs": 10, "passingScore": 80},
        "reassessment": {"intervalDays": 7, "recommendedAction": "Take 30-MCQ Mock Assessment for Docker"}
    },
    "microservices": {
        "skill": "Microservices",
        "overview": "Learn how to decompose monolithic applications into independent, scalable, and resilient microservice architectures.",
        "prerequisites": ["REST API Architecture", "Database Fundamentals", "Async Programming"],
        "stages": [
            {
                "level": "Basic",
                "topics": ["Monolithic vs Microservices Architecture", "Domain-Driven Design (DDD) & Bounded Contexts", "Service Boundaries & Independent Deployment"],
                "tasks": ["Decompose a sample E-commerce monolith conceptually into User, Catalog, and Order services", "Define API contracts between services"],
                "project": "Design Microservices Domain Blueprint"
            },
            {
                "level": "Intermediate",
                "topics": ["Inter-Service Communication (Synchronous REST/gRPC vs Asynchronous Messaging)", "API Gateway Pattern & Rate Limiting", "Database per Service Pattern", "Service Discovery & Registration"],
                "tasks": ["Build two independent FastAPI services that communicate via HTTP REST", "Implement centralized API Gateway routing"],
                "project": "Build Two-Service Architecture with Central Gateway"
            },
            {
                "level": "Advanced",
                "topics": ["Event-Driven Microservices with RabbitMQ/Kafka", "Resilience & Fault Tolerance (Circuit Breaker, Bulkhead)", "Distributed Tracing & Centralized Logging (OpenTelemetry, Prometheus)", "Saga Pattern for Distributed Transactions"],
                "tasks": ["Implement Circuit Breaker pattern for remote service calls", "Configure distributed tracing across request lifecycles"],
                "project": "Event-Driven Microservice Ecosystem with Distributed Tracing"
            }
        ],
        "handsOnProjects": [
            "Mini Project: REST API Gateway & User Service",
            "Capstone Project: Distributed Order Processing Ecosystem with Message Queue"
        ],
        "assessment": {"mcqs": 10, "passingScore": 80},
        "reassessment": {"intervalDays": 7, "recommendedAction": "Take Microservices Technical Re-assessment"}
    },
    "aws": {
        "skill": "AWS",
        "overview": "Build, deploy, and scale cloud applications using Amazon Web Services core compute, storage, and serverless infrastructure.",
        "prerequisites": ["Cloud Fundamentals", "Networking Concepts (VPC, CIDR)", "Linux CLI"],
        "stages": [
            {
                "level": "Basic",
                "topics": ["AWS Global Infrastructure (Regions & Availability Zones)", "IAM (Users, Roles, Policies, MFA)", "Amazon EC2 (Virtual Servers) & Security Groups", "Amazon S3 (Object Storage)"],
                "tasks": ["Launch an EC2 Ubuntu instance and connect via SSH", "Create an S3 bucket and upload public/private assets"],
                "project": "Deploy Static Web App on Amazon S3 with CloudFront CDN"
            },
            {
                "level": "Intermediate",
                "topics": ["Amazon RDS (Managed Relational Databases)", "AWS Lambda & Serverless Compute", "Amazon API Gateway", "Auto Scaling Groups & Elastic Load Balancing (ALB)"],
                "tasks": ["Connect FastAPI backend on EC2 to Amazon RDS PostgreSQL", "Create a serverless Lambda function triggered by S3 uploads"],
                "project": "Serverless Document Processing Pipeline with AWS Lambda & S3"
            },
            {
                "level": "Advanced",
                "topics": ["AWS CloudFormation & Terraform (Infrastructure as Code)", "Amazon ECS/EKS Container Orchestration", "CloudWatch Monitoring, Alarm, & CloudTrail Audit", "AWS Well-Architected Framework"],
                "tasks": ["Deploy Dockerized app to AWS ECS Fargate", "Set up CloudWatch alarm for CPU utilization spikes"],
                "project": "Production-Grade Highly Available AWS Infrastructure with ECS & ALB"
            }
        ],
        "handsOnProjects": [
            "Mini Project: Serverless Image Resizer with AWS Lambda",
            "Capstone Project: Highly Available Cloud Architecture for Career Compass AI"
        ],
        "assessment": {"mcqs": 10, "passingScore": 80},
        "reassessment": {"intervalDays": 7, "recommendedAction": "Take AWS Cloud Architecture Re-assessment"}
    }
}

def generate_dynamic_skill_roadmap(skill_name: str) -> dict:
    canonical = skill_name.strip()
    return {
        "skill": canonical,
        "overview": f"Complete step-by-step learning roadmap to master {canonical} from core fundamentals to advanced real-world applications.",
        "prerequisites": [f"Basic Programming Concepts", f"Software Engineering Fundamentals"],
        "stages": [
            {
                "level": "Basic",
                "topics": [f"Core Principles of {canonical}", f"Syntax & Environment Setup", f"Basic Data Structures & Utilities"],
                "tasks": [f"Install & configure {canonical} workspace", f"Write baseline Hello World program in {canonical}", f"Solve 5 introductory exercises"],
                "project": f"Basic CLI / Scripting utility using {canonical}"
            },
            {
                "level": "Intermediate",
                "topics": [f"Core Architecture & Best Practices in {canonical}", f"API Design & Modularization", f"Error Handling & Unit Testing"],
                "tasks": [f"Implement modular design patterns in {canonical}", f"Write automated unit tests", f"Integrate external data sources"],
                "project": f"Intermediate Application Module utilizing {canonical}"
            },
            {
                "level": "Advanced",
                "topics": [f"Performance Optimization & Benchmarking", f"Concurrency & Memory Efficiency", f"Production Deployment & Monitoring"],
                "tasks": [f"Profile and optimize execution bottlenecks", f"Configure CI/CD automated pipeline for {canonical}", f"Deploy to cloud environment"],
                "project": f"Production Capstone Application featuring {canonical}"
            }
        ],
        "handsOnProjects": [
            f"Mini Project: Interactive {canonical} Utility Tool",
            f"Capstone Project: Full-Stack Production Integration with {canonical}"
        ],
        "assessment": {"mcqs": 10, "passingScore": 80},
        "reassessment": {"intervalDays": 7, "recommendedAction": f"Take 30-MCQ Mock Assessment focusing on {canonical}"}
    }

@router.get("/skill/{skill_name}")
def get_skill_roadmap(skill_name: str, current_user: User = Depends(get_current_user)):
    key = skill_name.strip().lower()
    if key in SKILL_ROADMAP_DATABASE:
        return SKILL_ROADMAP_DATABASE[key]
    return generate_dynamic_skill_roadmap(skill_name)
