#!/bin/bash
cd /mnt/c/Repos/Open-Sora

echo "==================================="
echo "Open-Sora Video Generation Status"
echo "==================================="
echo ""

# Check if inference is running
if ps aux | grep -i "inference.py" | grep -v grep > /dev/null; then
    echo "✓ Generation is RUNNING"
    echo ""
    echo "Process info:"
    ps aux | grep -i "inference.py" | grep -v grep | head -3
else
    echo "✗ No generation process found"
fi

echo ""
echo "-----------------------------------"
echo "Generated Videos:"
echo "-----------------------------------"

if [ -d "samples" ]; then
    ls -lh samples/ | grep -E "\.(mp4|avi|gif)$" || echo "No videos yet..."
else
    echo "samples/ directory not created yet"
fi

echo ""
echo "==================================="

