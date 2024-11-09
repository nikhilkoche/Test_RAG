#!/bin/bash

# Define the list of query texts for each step
QUERY_TEXTS=(
    "What are some of the recommended first aid steps to treat someone experiencing heat exhaustion?"
    "What are the characteristics that distinguish a platform ladder from other types of ladders used in construction?"
    "What are the key considerations for planning stormwater management in alignment with sewage and water services, as outlined in the Provincial Planning Statement, 2024?"
    "What was the federal government's target date for eliminating long-term drinking water advisories in First Nations communities, and was this target achieved by February 2023?"
)

# Define the list of models
MODELS=(
    "llama3.1"
    #"qwen2.5"
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
    local query_text="$1"  # Use the provided query text for this step

    # Reset the database before running models
    echo "Resetting the database..."
    python populate_database.py --reset
    
    # Run models sequentially
    for MODEL in "${MODELS[@]}"; do
        echo "Running model: $MODEL"
        python newtest.py "$query_text" "$MODEL"
        
        # Optional delay between runs to stabilize system usage
        echo "Pausing for 10 seconds to stabilize system usage..."
        sleep 10
    done
    echo "All models have been processed."
}

# Step 1: Copy the first file, use the first query text, reset database, run models, then clear destination directory
echo "Copying the first file..."
cp "$SOURCE_DIR/$(ls "$SOURCE_DIR" | head -n 1)" "$TARGET_DIR"
run_models "${QUERY_TEXTS[0]}"
echo "Clearing destination directory..."
rm -rf "$TARGET_DIR"/*

# Step 2: Copy the first 4 files, use the second query text, reset database, run models, then clear destination directory
echo "Copying the first 4 files..."
ls "$SOURCE_DIR" | head -n 4 | xargs -I {} cp "$SOURCE_DIR/{}" "$TARGET_DIR"
run_models "${QUERY_TEXTS[1]}"
echo "Clearing destination directory..."
rm -rf "$TARGET_DIR"/*

# Step 3: Copy the fifth file, use the third query text, reset database, run models, then clear destination directory
echo "Copying the fifth file..."
ls "$SOURCE_DIR" | head -n 5 | tail -n 1 | xargs -I {} cp "$SOURCE_DIR/{}" "$TARGET_DIR"
run_models "${QUERY_TEXTS[2]}"
echo "Clearing destination directory..."
rm -rf "$TARGET_DIR"/*

# Step 4: Copy all files starting from the fifth file, use the fourth query text, reset database, run models, then clear destination directory
echo "Copying all files starting from the fifth file..."
ls "$SOURCE_DIR" | tail -n +5 | xargs -I {} cp "$SOURCE_DIR/{}" "$TARGET_DIR"
run_models "${QUERY_TEXTS[3]}"
echo "Clearing destination directory..."
rm -rf "$TARGET_DIR"/*
