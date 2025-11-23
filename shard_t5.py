import torch
import os
import json
from transformers import T5EncoderModel

def shard_model():
    input_dir = "./ckpts/google/t5-v1_1-xxl"
    output_dir = "./ckpts/google/t5-v1_1-xxl-sharded"
    
    print(f"Loading model from {input_dir}...")
    # We use lazy loading via accelerate if available, or just state dict loading
    # But here we can just load the state dict directly without instantiating the model first to save RAM
    
    chkpt_path = os.path.join(input_dir, "pytorch_model.bin")
    print(f"Loading state dict from {chkpt_path} (this may take time)...")
    
    # Load on CPU
    state_dict = torch.load(chkpt_path, map_location="cpu")
    
    print("Sharding model...")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    # Copy config files
    os.system(f"cp {input_dir}/*.json {output_dir}/")
    os.system(f"cp {input_dir}/*.txt {output_dir}/")
    os.system(f"cp {input_dir}/*.model {output_dir}/")
    
    # Shard weights
    # We'll split into ~2GB chunks
    max_shard_size = 2 * 1024 * 1024 * 1024 # 2GB
    
    from transformers.modeling_utils import shard_checkpoint
    shards, index = shard_checkpoint(state_dict, max_shard_size=max_shard_size, weights_name="pytorch_model.bin")
    
    # Save shards
    for shard_file, shard in shards.items():
        print(f"Saving {shard_file}...")
        torch.save(shard, os.path.join(output_dir, shard_file))
        
    # Save index
    with open(os.path.join(output_dir, "pytorch_model.bin.index.json"), "w") as f:
        json.dump(index, f, indent=2)
        
    print(f"Model sharded successfully to {output_dir}")

if __name__ == "__main__":
    shard_model()

