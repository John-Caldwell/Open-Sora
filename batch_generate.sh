#!/bin/bash
# Batch generation from CSV for Open-Sora (WSL/Linux)
# Usage: ./batch_generate.sh prompts.csv [config] [save_dir]

set -e

CSV_PATH="$1"
CONFIG="${2:-configs/diffusion/inference/t2i2v_256px.py}"
SAVE_DIR="${3:-samples}"

if [ -z "$CSV_PATH" ]; then
    echo "Usage: $0 <csv_path> [config] [save_dir]"
    echo ""
    echo "CSV format:"
    echo "  text,reference"
    echo "  \"ocean waves at sunset\","
    echo "  \"a cat playing with yarn\","
    echo ""
    echo "Example:"
    echo "  $0 prompts.csv"
    echo "  $0 prompts.csv configs/diffusion/inference/256px.py samples"
    exit 1
fi

if [ ! -f "$CSV_PATH" ]; then
    echo "Error: CSV file not found: $CSV_PATH"
    exit 1
fi

echo "================================"
echo "Open-Sora Batch Generation"
echo "================================"
echo ""
echo "CSV Path: $CSV_PATH"
echo "Config: $CONFIG"
echo "Save Directory: $SAVE_DIR"
echo ""

CMD="torchrun --nproc_per_node 1 --standalone scripts/diffusion/inference.py $CONFIG --save-dir $SAVE_DIR --dataset.data-path $CSV_PATH"

echo "Running: $CMD"
echo ""

eval $CMD


