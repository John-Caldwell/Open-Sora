#!/bin/bash
# Quick video generation script for Open-Sora (WSL/Linux)
# Usage: ./generate.sh "your prompt here" [options]

set -e

# Default values
PROMPT=""
CONFIG="configs/diffusion/inference/t2i2v_256px.py"
SAVE_DIR="samples"
SEED=-1
MOTION_SCORE=4
ASPECT_RATIO="16:9"
NUM_FRAMES=129

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --config)
            CONFIG="$2"
            shift 2
            ;;
        --save-dir)
            SAVE_DIR="$2"
            shift 2
            ;;
        --seed)
            SEED="$2"
            shift 2
            ;;
        --motion-score)
            MOTION_SCORE="$2"
            shift 2
            ;;
        --aspect-ratio)
            ASPECT_RATIO="$2"
            shift 2
            ;;
        --num-frames)
            NUM_FRAMES="$2"
            shift 2
            ;;
        *)
            if [ -z "$PROMPT" ]; then
                PROMPT="$1"
            fi
            shift
            ;;
    esac
done

if [ -z "$PROMPT" ]; then
    echo "Usage: $0 \"your prompt here\" [options]"
    echo ""
    echo "Options:"
    echo "  --config PATH          Config file (default: t2i2v_256px.py)"
    echo "  --save-dir PATH        Save directory (default: samples)"
    echo "  --seed NUM             Random seed (default: -1)"
    echo "  --motion-score NUM     Motion score 1-7 (default: 4)"
    echo "  --aspect-ratio RATIO   Aspect ratio (default: 16:9)"
    echo "  --num-frames NUM       Number of frames (default: 129)"
    echo ""
    echo "Examples:"
    echo "  $0 \"ocean waves at sunset\""
    echo "  $0 \"a cat playing\" --seed 42 --motion-score 7"
    exit 1
fi

echo "================================"
echo "Open-Sora Video Generation"
echo "================================"
echo ""
echo "Prompt: $PROMPT"
echo "Config: $CONFIG"
echo "Save Directory: $SAVE_DIR"
echo ""

# Build command
CMD="torchrun --nproc_per_node 1 --standalone scripts/diffusion/inference.py $CONFIG --save-dir $SAVE_DIR --prompt \"$PROMPT\""

if [ $SEED -ge 0 ]; then
    CMD="$CMD --seed $SEED --sampling_option.seed $SEED"
fi

if [ $MOTION_SCORE -gt 0 ]; then
    CMD="$CMD --motion-score $MOTION_SCORE"
fi

if [ -n "$ASPECT_RATIO" ]; then
    CMD="$CMD --aspect_ratio $ASPECT_RATIO"
fi

if [ $NUM_FRAMES -gt 0 ]; then
    CMD="$CMD --num_frames $NUM_FRAMES"
fi

echo "Running: $CMD"
echo ""

eval $CMD


