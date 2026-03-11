# Stage 1: Build (The "Kitchen")
FROM python:3.10-slim as builder
WORKDIR /app

# Install build tools and CLEAN UP immediately
RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install packages without saving temporary files
RUN pip install --user --no-cache-dir \
    fastapi uvicorn transformers python-dotenv anyio

# Install CPU-torch (This is the big one, we save GBs here)
RUN pip install --user --no-cache-dir \
    torch --extra-index-url https://download.pytorch.org/whl/cpu

# Stage 2: Final Production (The "Clean Table")
FROM python:3.10-slim
WORKDIR /app

# Copy only the final "cooked" packages
COPY --from=builder /root/.local /root/.local
COPY ./app ./app

# Set PATH
ENV PATH=/root/.local/bin:$PATH
# Ensure Python doesn't write .pyc files (saves a tiny bit more space)
ENV PYTHONDONTWRITEBYTECODE=1

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]