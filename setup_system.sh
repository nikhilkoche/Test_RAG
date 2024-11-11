#!/bin/bash

# Update and upgrade system packages
sudo apt-get update -y
sudo apt-get upgrade -y

# Install Python and required dependencies
sudo apt-get install -y python3 python3-pip python3-venv git curl
sudo curl -fsSL https://ollama.com/install.sh | sh
#
ollama pull nomic-embed-text
ollama pull qwen2.5
ollama pull qwen2.5:3b
ollama pull llama3.1
ollama pull llama3.2
ollama pull llama3.2:1b
ollama run mistral


# Clone the repository (replace with your repository URL)
REPO_URL="https://github.com/nikhilkoche/Test_RAG.git"
REPO_DIR="Test_RAG"

# Check if the repository is already cloned; if not, clone it
if [ ! -d "$REPO_DIR" ]; then
    git clone -b automate $REPO_URL
fi

# Change to the repository directory
cd "$REPO_DIR"
mkdir data
# Set up a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install required Python packages
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

# Deactivate the virtual environment
deactivate

echo "Setup complete. The environment is ready. Activate it using 'source venv/bin/activate'."
