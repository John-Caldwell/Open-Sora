import torch
import os
from transformers import T5EncoderModel, T5Config
from accelerate import init_empty_weights
from safetensors.torch import save_file

# Paths
input_dir = "./ckpts/google/t5-v1_1-xxl"
output_dir = "./ckpts/google/t5-v1_1-xxl-sharded"
os.makedirs(output_dir, exist_ok=True)

print(f"Loading config from {input_dir}...")
config = T5Config.from_pretrained(input_dir)

print("Defining model structure (empty weights)...")
with init_empty_weights():
    model = T5EncoderModel(config)

# We need to load the state dict from the big bin file safely
# Since mmap fails, we might need to use a different approach.
# However, let's try to use the 'map_location' to CPU and verify if we can load it.
# If direct load fails, we are in a bind without more RAM.
# But usually 'torch.load' allows loading if we have enough SWAP.
# Ensure you have a pagefile/swap enabled in Windows/WSL!

checkpoint_path = os.path.join(input_dir, "pytorch_model.bin")
print(f"Loading massive checkpoint from {checkpoint_path}...")

# Try loading with mmap=True explicitly? No, the error said mmap failed.
# We'll try standard load. If this crashes, we need to increase Swap space.
try:
    state_dict = torch.load(checkpoint_path, map_location="cpu")
except Exception as e:
    print(f"Failed to load checkpoint: {e}")
    print("Tip: Ensure you have enough Swap space (Pagefile) in Windows.")
    exit(1)

print("Checkpoint loaded. Saving as sharded safetensors...")

# Split into chunks (e.g., 5GB)
shard_size = 5 * 1024 * 1024 * 1024 # 5GB
current_shard = {}
current_size = 0
shard_index = 0

def save_shard(shard, index):
    filename = f"model-{index:05d}-of-{total_shards:05d}.safetensors"
    save_path = os.path.join(output_dir, filename)
    print(f"Saving shard {index} to {filename}...")
    save_file(shard, save_path)

# This is a simplified sharding. A proper one needs to calculate total size first to know total_shards.
# For now, let's just save sequentially and handle the index map later or simply use 
# 'save_pretrained' from transformers which handles sharding automatically if we can load it!

print("Using transformers save_pretrained to handle sharding automatically...")
# We load the state_dict into the model? No, that duplicates memory.
# We can use 'save_pretrained' with the state_dict directly if we wrap it?
# Actually, 'model.save_pretrained(..., state_dict=state_dict)' works in recent versions.

# Load state dict into the empty model?
# model.load_state_dict(state_dict) -> This works if we use 'accelerate' to load into devices.
# But we are on CPU.

# Let's try the most robust way: Transformers 'save_pretrained' with max_shard_size
# We create a model with the state_dict.
model = T5EncoderModel.from_pretrained(input_dir, state_dict=state_dict, torch_dtype=torch.float16)
# Converting to float16 saves 50% RAM! 44GB -> 22GB. This might fit!

print("Saving sharded model...")
model.save_pretrained(output_dir, max_shard_size="5GB", safe_serialization=True)
config.save_pretrained(output_dir)

print(f"Done! Sharded model saved to {output_dir}")



