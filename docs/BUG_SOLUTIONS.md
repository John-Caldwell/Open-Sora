# Bug Solutions and Known Issues

## Windows Native Execution Issues

### Problem
Open-Sora cannot run natively on Windows due to the following dependencies that do not support Windows:

1. **ColossalAI** - Core dependency for distributed training/inference
   - Error: `RuntimeError: Windows is not supported yet. Please try again within the Windows Subsystem for Linux (WSL).`
   - Required for: Model parallelism, distributed operations
   
2. **Triton** - Required by liger-kernel for optimized kernels
   - Error: `ERROR: No matching distribution found for triton>=2.3.1`
   - Required for: Performance optimizations

3. **torchrun** - PyTorch distributed launcher has libuv issues on Windows
   - Error: `RuntimeError: use_libuv was requested but PyTorch was build without libuv support`
   - Required for: Multi-GPU inference

### Solution
Use **Windows Subsystem for Linux (WSL 2)** to run Open-Sora:

#### Setup WSL 2 (Recommended)

1. **Install WSL 2:**
   ```powershell
   wsl --install
   ```

2. **Install Ubuntu in WSL:**
   ```powershell
   wsl --install -d Ubuntu-24.04
   ```

3. **Setup CUDA in WSL:**
   - Install NVIDIA drivers on Windows (already done - RTX 5060 detected)
   - WSL will automatically access the GPU through the Windows driver
   - No need to install CUDA separately in WSL

4. **Install dependencies in WSL:**
   ```bash
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install Python and pip
   sudo apt install python3.11 python3-pip git -y
   
   # Clone repo (or access Windows files at /mnt/c/Repos/Open-Sora)
   cd /mnt/c/Repos/Open-Sora
   
   # Install PyTorch with CUDA
   pip3 install torch==2.4.0 torchvision==0.19.0 --index-url https://download.pytorch.org/whl/cu121
   
   # Install requirements
   pip3 install -r requirements.txt
   
   # Install Open-Sora
   pip3 install -e .
   ```

5. **Run inference:**
   ```bash
   torchrun --nproc_per_node 1 --standalone scripts/diffusion/inference.py \
     configs/diffusion/inference/256px.py \
     --save-dir samples \
     --prompt "ocean waves crashing on a beach at sunset"
   ```

#### Alternative: Docker

Use the official Docker image (requires Docker Desktop with WSL 2 backend):

```bash
docker pull hpcaitech/open-sora:latest
docker run --gpus all -v C:\Repos\Open-Sora:/workspace hpcaitech/open-sora:latest
```

### Status
- ✅ PyTorch with CUDA 12.4 installed on Windows
- ✅ Models downloaded (~50GB)
- ✅ All compatible dependencies installed
- ❌ Cannot run inference natively on Windows
- ✅ WSL 2 is the recommended solution

### Verification
To verify GPU is accessible in WSL:
```bash
python3 -c "import torch; print('CUDA available:', torch.cuda.is_available())"
```

Expected output: `CUDA available: True`

---

## RTX 5060 / Blackwell (sm_120) Compatibility Issue

### Problem
NVIDIA GeForce RTX 5060 Laptop GPU uses the Blackwell architecture with compute capability **sm_120**, which is too new for current PyTorch releases (as of November 2024). When running Open-Sora, you may encounter:

```
RuntimeError: CUDA error: no kernel image is available for execution on the device
```

This occurs because:
1. PyTorch 2.6.0 only supports up to sm_90 (Hopper architecture)
2. NCCL (distributed communications library) tries to use CUDA kernels
3. The kernels aren't compiled for sm_120

### Workaround: Disable NCCL

Force PyTorch to use Gloo backend instead of NCCL for single-GPU inference:

```bash
export CUDA_VISIBLE_DEVICES=0
export NCCL_P2P_DISABLE=1
export NCCL_IB_DISABLE=1

# Run with Gloo backend
torchrun --nproc_per_node 1 --standalone \
  scripts/diffusion/inference.py \
  configs/diffusion/inference/t2i2v_256px.py \
  --save-dir samples \
  --prompt "A cat playing with a ball of yarn"
```

Or modify the script to use Gloo explicitly:
```python
# In scripts/diffusion/inference.py, around line 60
dist.init_process_group(backend="gloo")  # Change from "nccl" to "gloo"
```

### Alternative: Build PyTorch from Source

For native sm_120 support, PyTorch must be built from source with CUDA 13.0:

**Status**: CUDA libraries successfully compiled with sm_120 support, but Python bindings have linking issues (see `PYTORCH_SM120_SUMMARY.md`).

**Timeline**: Official PyTorch support for Blackwell expected in Q1-Q2 2025.

### Temporary Solution

Use CPU-only mode for testing (slow but works):
```bash
CUDA_VISIBLE_DEVICES="" python3 scripts/diffusion/inference.py ...
```

Or wait for PyTorch 2.7+ which should include Blackwell support.

---


