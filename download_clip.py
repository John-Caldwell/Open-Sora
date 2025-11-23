#!/usr/bin/env python3
"""Download CLIP model."""

from huggingface_hub import snapshot_download

print("Downloading CLIP...")
snapshot_download(
    repo_id="openai/clip-vit-large-patch14",
    local_dir="./ckpts/openai/clip-vit-large-patch14",
    local_dir_use_symlinks=False,
)
print("✓ CLIP downloaded!")

import subprocess
result = subprocess.run(["du", "-sh", "./ckpts/openai/clip-vit-large-patch14"], capture_output=True, text=True)
print(result.stdout)


