#!/usr/bin/env python3
"""Download Open-Sora v2 model checkpoints from Hugging Face."""

import os
from huggingface_hub import snapshot_download

print("=" * 60)
print("Downloading Open-Sora v2 Models (~22GB)")
print("=" * 60)
print()

# Create ckpts directory
os.makedirs("./ckpts", exist_ok=True)

# Download the main Open-Sora v2 model
print("Downloading Open-Sora v2 model files...")
try:
    snapshot_download(
        repo_id="hpcai-tech/OpenSora-STDiT-v3",
        local_dir="./ckpts",
        local_dir_use_symlinks=False,
    )
    print("✓ Downloaded successfully!")
except Exception as e:
    print(f"✗ Error: {e}")
    print()
    print("Trying alternative repository...")
    try:
        snapshot_download(
            repo_id="hpcai-tech/Open-Sora",
            local_dir="./ckpts",
            local_dir_use_symlinks=False,
        )
        print("✓ Downloaded successfully!")
    except Exception as e2:
        print(f"✗ Error: {e2}")

print()
print("=" * 60)
print("Download complete! Checking files...")
print("=" * 60)

# List downloaded files
import subprocess
result = subprocess.run(["du", "-sh", "./ckpts"], capture_output=True, text=True)
print(result.stdout)

result = subprocess.run(["ls", "-lh", "./ckpts"], capture_output=True, text=True)
print(result.stdout[:1000])

