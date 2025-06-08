FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.5.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    PATH="$POETRY_HOME/bin:$PATH"

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    libpoppler-cpp-dev \
    pkg-config \
    tesseract-ocr \
    tesseract-ocr-eng \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -


# Copy project files
WORKDIR /app
COPY pyproject.toml poetry.lock* ./

# Install Python dependencies
RUN poetry install --no-dev --no-root

# Copy the rest of the project
COPY . .

# Install the package in development mode
RUN poetry install --no-dev

# Create a non-root user
RUN adduser --disabled-password --gecos '' redocuser
USER redocuser

# Set the entrypoint
ENTRYPOINT ["redoc"]
CMD ["--help"]
