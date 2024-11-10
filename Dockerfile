# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install necessary packages for Ollama installation and Python dependencies
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Run the installation command for Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Copy the requirements file into the container at /app
COPY requirements.txt ./

# Install Python dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . .

# Expose any necessary ports (optional)
# EXPOSE 8000

# Set the default command to run when the container starts
#CMD ollama pull llama3.2:1b && bash run_models.sh