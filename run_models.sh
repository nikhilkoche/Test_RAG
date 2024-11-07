#!/bin/bash

# Define the query text
QUERY_TEXT="What is the text about?"

# Define the list of models
MODELS=(
    "llama3.1"
    "llama3.2"
    "llama3.2:1b"
    "llama3.2:1b-instruct-q2_K"
    # Add more models as needed
)

# Run the Python script for each model
for MODEL in "${MODELS[@]}"; do
    echo "Running model: $MODEL"
    python newtest.py "$QUERY_TEXT" "$MODEL"
    
    # Optional delay between runs to stabilize system usage
    echo "Pausing for  seconds to stabilize system usage..."
    sleep 10
done

echo "All models have been processed."
