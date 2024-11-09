#!/bin/bash

# Define the query text
QUERY_TEXT="What is the text about?"

# Define the list of models
MODELS=(
    "llama3.1"
    "qwen2.5"
    "mistral"
    "llama3.2"
    "qwen2.5:3b" 
    "llama3.2:1b"
    # Add more models as needed
)

# Define source and target directories for file copying
SOURCE_DIR="data_1"
TARGET_DIR="data"

# Ensure the target directory exists
mkdir -p "$TARGET_DIR"

# Function to reset the database and then run all models on the copied files
run_models() {
    # Reset the database before running models
    echo "Resetting the database..."
    python populate_database.py --reset
    
    # Run models sequentially
    for MODEL in "${MODELS[@]}"; do
        echo "Running model: $MODEL"
        python newtest.py "$QUERY_TEXT" "$MODEL"
        
        # Optional delay between runs to stabilize system usage
        echo "Pausing for 10 seconds to stabilize system usage..."
        sleep 10
    done
    echo "All models have been processed."
}

# Step 1: Copy the first file, reset database, run models, then clear destination directory
echo "Copying the first file..."
cp "$SOURCE_DIR/$(ls "$SOURCE_DIR" | head -n 1)" "$TARGET_DIR"
run_models
echo "Clearing destination directory..."
rm -rf "$TARGET_DIR"/*

# Step 2: Copy the first 4 files, reset database, run models, then clear destination directory
echo "Copying the first 4 files..."
ls "$SOURCE_DIR" | head -n 4 | xargs -I {} cp "$SOURCE_DIR/{}" "$TARGET_DIR"
run_models
echo "Clearing destination directory..."
rm -rf "$TARGET_DIR"/*

# Step 3: Copy the fifth file, reset database, run models, then clear destination directory
echo "Copying the fifth file..."
ls "$SOURCE_DIR" | head -n 5 | tail -n 1 | xargs -I {} cp "$SOURCE_DIR/{}" "$TARGET_DIR"
run_models
echo "Clearing destination directory..."
rm -rf "$TARGET_DIR"/*

# Step 4: Copy all files starting from the fifth file, reset database, run models, then clear destination directory
echo "Copying all files starting from the fifth file..."
ls "$SOURCE_DIR" | tail -n +5 | xargs -I {} cp "$SOURCE_DIR/{}" "$TARGET_DIR"
run_models
echo "Clearing destination directory..."
rm -rf "$TARGET_DIR"/*
