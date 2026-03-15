FROM maven:3.9-eclipse-temurin-21-noble AS jars

LABEL org.opencontainers.image.source=https://github.com/kimiroo/apt4989-api

RUN apt-get update && apt-get install -y \
    python3-dev \
    build-essential \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy dependency data
COPY src/pom.xml ./
COPY src/requirements.txt ./

# Create venv
RUN python3 -m venv venv
ENV PATH="/app/venv/bin:$PATH"

# Install dependencies
RUN mvn dependency:copy-dependencies -DoutputDirectory=./lib
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src .

# Set encoding
ENV PYTHONIOENCODING=utf-8
ENV JAVA_TOOL_OPTIONS="-Dfile.encoding=UTF8"

CMD ["gunicorn", "main:app", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "--timeout", "60", "--access-logfile", "-", "--error-logfile", "-"]