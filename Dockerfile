# Stage 1: Builder stage
FROM python:3.11-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends     build-essential     curl     git     && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy only the files needed for installation
COPY gpt_engineer_enhanced_web/requirements.txt .
COPY pyproject.toml poetry.lock ./

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip &&     pip install --no-cache-dir -r requirements.txt

# Install poetry and gpt-engineer dependencies
RUN pip install --no-cache-dir poetry &&     poetry config virtualenvs.create false &&     poetry install --no-dev

# Stage 2: Final stage
FROM python:3.11-slim

WORKDIR /app

# Copy Python packages from builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy the application code
COPY . .

# Install Node.js and npm
RUN apt-get update && apt-get install -y ca-certificates curl gnupg &&     mkdir -p /etc/apt/keyrings &&     curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg &&     echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_18.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list &&     apt-get update && apt-get install -y nodejs &&     apt-get clean && rm -rf /var/lib/apt/lists/*

# Verify Node.js and npm installation
RUN node --version && npm --version

# Install frontend dependencies and build CSS
WORKDIR /app/gpt_engineer_enhanced_web
RUN npm install && npm run build

# Install gpt-engineer in editable mode
WORKDIR /app
RUN pip install -e .
WORKDIR /app/gpt_engineer_enhanced_web

# Set the command to run the application
CMD ["python", "-m", "uvicorn", "gpt_engineer_enhanced_web.asgi:application", "--host", "0.0.0.0", "--port", "8000",  "--reload"]
