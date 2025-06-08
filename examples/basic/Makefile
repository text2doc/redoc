.PHONY: install test run clean build-docker run-docker

# Variables
PYTHON = python3
PIP = pip3
DOCKER = docker

# Default target
all: install test

# Install dependencies
install:
	$(PIP) install -r requirements.txt

# Run tests
test:
	$(PYTHON) -m pytest test.py -v

# Run the example
run:
	$(PYTHON) main.py

# Build Docker image
build-docker:
	$(DOCKER) build -t redoc-basic-example .

# Run in Docker
run-docker: build-docker
	$(DOCKER) run --rm -v "$(PWD)/output:/app/output" redoc-basic-example

# Clean generated files
clean:
	rm -rf __pycache__ output/*.pdf
