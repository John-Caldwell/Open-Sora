#!/usr/bin/env python3
"""Download all Open-Sora v2 model components."""

import os
from huggingface_hub import snapshot_download, hf_hub_download

print("=" * 60)
print("Downloading Open-Sora v2 Model Components")
print("=" * 60)
print()

# Rename the existing model if it's in the wrong place
if os.path.exists("./ckpts/model.safetensors") and not os.path.exists("./ckpts/Open_Sora_v2.safetensors"):
    print("Renaming model.safetensors to Open_Sora_v2.safetensors...")
    os.rename("./ckpts/model.safetensors", "./ckpts/Open_Sora_v2.safetensors")
    print("✓ Renamed")
    print()

# Download VAE
print("1. Downloading HunyuanVideo VAE...")
try:
    hf_hub_download(
        repo_id="tencent/HunyuanVideo",
        filename="hunyuan-video-t2v-720p/vae/pytorch_model.pt",
        local_dir="./ckpts",
        local_dir_use_symlinks=False,
    )
    # Try to rename if needed
    vae_path = "./ckpts/hunyuan-video-t2v-720p/vae/pytorch_model.pt"
    if os.path.exists(vae_path):
        os.makedirs("./ckpts", exist_ok=True)
        import shutil
        shutil.copy(vae_path, "./ckpts/hunyuan_vae.pt")
        print("✓ Downloaded VAE")
except Exception as e:
    print(f"Note: {e}")
    print("Will try alternative...")
    try:
        hf_hub_download(
            repo_id="hpcai-tech/Open-Sora",
            filename="vae.safetensors",
            local_dir="./ckpts",
            local_dir_use_symlinks=False,
        )
        if os.path.exists("./ckpts/vae.safetensors"):
            os.rename("./ckpts/vae.safetensors", "./ckpts/hunyuan_vae.safetensors")
        print("✓ Downloaded VAE (alternative)")
    except Exception as e2:
        print(f"✗ Could not download VAE: {e2}")
print()

# Download T5
print("2. Downloading T5-XXL text encoder (~20GB)...")
try:
    snapshot_download(
        repo_id="google/t5-v1_1-xxl",
        local_dir="./ckpts/google/t5-v1_1-xxl",
        local_dir_use_symlinks=False,
    )
    print("✓ Downloaded T5")
except Exception as e:
    print(f"✗ Error: {e}")
print()

# Download CLIP
print("3. Downloading CLIP text encoder (~1.7GB)...")
try:
    snapshot_download(
        repo_id="openai/clip-vit-large-patch14",
        local_dir="./ckpts/openai/clip-vit-large-patch14",
        local_dir_use_symlinks=False,
    )
    print("✓ Downloaded CLIP")
except Exception as e:
    print(f"✗ Error: {e}")
print()

print("=" * 60)
print("Download Summary")
print("=" * 60)
import subprocess
result = subprocess.run(["du", "-sh", "./ckpts"], capture_output=True, text=True)
print(result.stdout)
print()
print("Files:")
result = subprocess.run(["find", "./ckpts", "-name", "*.safetensors", "-o", "-name", "*.pt", "-o", "-name", "*.bin"], 
                       capture_output=True, text=True)
print(result.stdout[:500])


