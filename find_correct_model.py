#!/usr/bin/env python3
"""Find the correct Open-Sora v2 model."""

from huggingface_hub import list_models

print("Searching for Open-Sora v2 models...")
print()

# Search for hpcai-tech models
for model in list_models(author="hpcai-tech", search="open-sora"):
    print(f"- {model.modelId}")

print()
print("Looking for specific v2 models...")

# Common names to try
repos_to_check = [
    "hpcai-tech/Open-Sora-v2",
    "hpcai-tech/OpenSora-v2",
    "hpcai-tech/Open-Sora",
]

for repo in repos_to_check:
    try:
        from huggingface_hub import model_info
        info = model_info(repo)
        print(f"✓ Found: {repo}")
        print(f"  Last modified: {info.lastModified}")
        print(f"  Downloads: {info.downloads}")
        print()
    except:
        print(f"✗ Not found: {repo}")


