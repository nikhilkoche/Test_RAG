# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install curl (required for running the install command)
RUN apt-get update 

# Run the installation command for Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Copy the requirements file into the container at /app
COPY requirements.txt ./

# Install any dependencies specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . .

# Expose any necessary ports (optional)
# EXPOSE 8000

# Set the default command to run when the container starts
#CMD ["bash", "run_models.sh"]
