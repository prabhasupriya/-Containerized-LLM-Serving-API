
## 🚀 LLM Microservice: Production-Ready GPT-2 Deployment
This project implements a secure, containerized RESTful API for serving a Large Language Model (LLM) using FastAPI and Docker. It is engineered with MLOps best practices to ensure scalability, security, and resource efficiency.
###  Project Structure
**app/main.py:** Core FastAPI logic featuring the Singleton Model Class and asynchronous endpoints.
**.env:** Stores sensitive configuration like the API_KEY and MODEL_NAME.
**Dockerfile:** Implements a multi-stage build to separate the build environment from the lean production image.
**docker-compose.yml:** Orchestrates the service, mapping ports and injecting environment variables.**test_api.py:** A dedicated Python script to validate security and concurrency requirements.
###  Key Features & MLOps Principles
**Secure API Design:** All generation requests are protected via X-API-KEY header validation to prevent unauthorized usage
**Lazy Model Loading:** The GPT-2 model follows a Singleton Pattern, initializing only upon the first request to ensure the container starts instantly.
**Advanced Concurrency:** Uses anyio.to_thread to handle multiple inference requests simultaneously without blocking the main event loop.
Optimized Footprint: Uses a python:3.10-slim base and torch-cpu to maintain an optimized image size (~1.5GB).### 🛠️ Setup & Execution Commands1. Build and Launch:Run the service in detached mode to keep your terminal free.Bashdocker-compose up --build -d
**Optimized Footprint:** Uses a python:3.10-slim base and torch-cpu to maintain an optimized image size (~1.5GB).
### Setup & Execution Commands
**1. Build and Launch:**
```bash
-compose up --build -d
```
**2.Verify Image Optimization** :
```bash
docker images
```
**3. Run Automated Validation Suite:**Executes tests for Health, Security (403 Rejection), and Concurrency
```bash
python test_api.py
```
**4. Shutdown & Cleanup:**Stops the container and removes the internal network
```bash
docker-compose down
```
### API Documentation
Endpoints Overview
Endpoint,Method,Auth Required,Description
/health,GET,No,Returns a 200 OK status and a JSON message confirming the service is operational.
/generate,POST,Yes (API Key),Accepts a JSON payload with a prompt and returns the LLM-generated text response.
**Sample Request (Windows CMD)**
```bash
 -X POST http://localhost:8000/generate ^
-H "X-API-KEY: YOUR_KEY_FROM_ENV" ^
-H "Content-Type: application/json" ^
-d "{\"prompt\": \"The future of AI is\", \"max_new_tokens\": 20}"
```