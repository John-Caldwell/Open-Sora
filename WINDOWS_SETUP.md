# Open-Sora Setup Guide for Windows Users

## ⚠️ Important: WSL Required

**Open-Sora cannot run natively on Windows** due to dependencies (ColossalAI, Triton) that only support Linux. You must use **Windows Subsystem for Linux (WSL 2)** to run Open-Sora.

## Quick Start

### 1. Install WSL 2

Open PowerShell as Administrator and run:

```powershell
wsl --install
```

Restart your computer when prompted.

### 2. Install Ubuntu

```powershell
wsl --install -d Ubuntu-24.04
```

Follow the prompts to create a username and password.

### 3. Setup Open-Sora in WSL

Open Ubuntu from the Start menu, then run:

```bash
# Navigate to your Windows repository
cd /mnt/c/Repos/Open-Sora

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3.11 python3-pip git -y

# Install PyTorch with CUDA support
pip3 install torch==2.4.0 torchvision==0.19.0 --index-url https://download.pytorch.org/whl/cu121

# Install Open-Sora requirements
pip3 install -r requirements.txt

# Install Open-Sora package
pip3 install -e .
```

### 4. Verify GPU Access

```bash
python3 -c "import torch; print('CUDA available:', torch.cuda.is_available()); print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'N/A')"
```

Expected output:
```
CUDA available: True
GPU: NVIDIA GeForce RTX 5060 Laptop GPU
```

### 5. Generate Your First Video

```bash
# Simple text-to-video (fast, ~60 seconds)
torchrun --nproc_per_node 1 --standalone scripts/diffusion/inference.py \
  configs/diffusion/inference/256px.py \
  --save-dir samples \
  --prompt "ocean waves crashing on a beach at sunset"

# Text-to-image-to-video (better quality, ~90 seconds)
torchrun --nproc_per_node 1 --standalone scripts/diffusion/inference.py \
  configs/diffusion/inference/t2i2v_256px.py \
  --save-dir samples \
  --prompt "a cat playing with a ball of yarn"
```

## Helper Scripts

### Quick Generation

Use the provided bash script for easier generation:

```bash
chmod +x generate.sh
./generate.sh "your prompt here"
```

With options:

```bash
./generate.sh "sunset over mountains" --seed 42 --motion-score 7 --aspect-ratio 16:9
```

### Batch Generation

Create a CSV file with your prompts:

```csv
text,reference
"ocean waves at sunset",
"a cat playing with yarn",
"rain falling on city streets",
```

Run batch generation:

```bash
chmod +x batch_generate.sh
./batch_generate.sh prompts.csv
```

## Configuration Options

### Available Configs

**Direct Text-to-Video:**
- `configs/diffusion/inference/256px.py` - Fast, lower quality (~45 sec, 5GB VRAM)
- `configs/diffusion/inference/768px.py` - Slow, higher quality (~15 min, 8GB VRAM)

**Text-to-Image-to-Video (Recommended):**
- `configs/diffusion/inference/t2i2v_256px.py` - Best quality at 256px (~90 sec, 6GB VRAM)
- `configs/diffusion/inference/t2i2v_768px.py` - Highest quality (~20 min, 8GB VRAM)

### Command-Line Parameters

```bash
--prompt "your prompt"           # Text description
--save-dir samples               # Output directory
--seed 42                        # Random seed for reproducibility
--motion-score 4                 # Motion intensity (1-7)
--aspect_ratio "16:9"            # Video aspect ratio (16:9, 9:16, 1:1)
--num_frames 129                 # Number of frames (4k+1 format: 33, 65, 129)
--sampling_option.num_steps 50   # Quality (30-50)
--sampling_option.guidance 7.5   # Guidance scale (5.0-10.0)
--offload True                   # Offload to CPU to save VRAM
```

## Performance Expectations (RTX 5060 8GB)

| Config | Resolution | Time | VRAM | Quality |
|--------|-----------|------|------|---------|
| 256px.py | 256×256 | ~45s | ~5GB | Good |
| t2i2v_256px.py | 256×256 | ~90s | ~6GB | Better |
| 768px.py | 768×768 | ~15min | ~8GB | Best |
| t2i2v_768px.py | 768×768 | ~20min | ~8GB | Excellent |

## Troubleshooting

### CUDA Out of Memory

Add `--offload True` to move models between CPU/GPU:

```bash
torchrun --nproc_per_node 1 --standalone scripts/diffusion/inference.py \
  configs/diffusion/inference/t2i2v_256px.py \
  --save-dir samples \
  --prompt "test" \
  --offload True
```

Or reduce frames:

```bash
--num_frames 65  # or 33 for very low VRAM
```

### Slow First Run

The first generation will be slower (~2-3 minutes) as models are loaded and compiled. Subsequent runs will be faster.

### Model Not Found

Ensure models are downloaded:

```bash
huggingface-cli download hpcai-tech/Open-Sora-v2 --local-dir ./ckpts
```

### Import Errors

Reinstall dependencies:

```bash
pip3 install -r requirements.txt --force-reinstall
pip3 install -e .
```

## File Access Between Windows and WSL

### From Windows to WSL

WSL mounts your Windows drives at `/mnt/`:
- `C:\Repos\Open-Sora` → `/mnt/c/Repos/Open-Sora`

### From WSL to Windows

Access WSL files from Windows at:
- `\\wsl$\Ubuntu-24.04\home\<username>\`

Or in File Explorer, type: `\\wsl$`

## Generated Videos Location

Videos are saved in the `samples/` directory. Access them from:

**In WSL:**
```bash
ls samples/
```

**In Windows:**
```
C:\Repos\Open-Sora\samples\
```

Or: `\\wsl$\Ubuntu-24.04\mnt\c\Repos\Open-Sora\samples\`

## Content Restrictions

⚠️ **Important:** Open-Sora uses the Tencent HunyuanVideo license which includes:

1. **Prohibited Content:**
   - Illegal activities
   - Hate speech or discrimination
   - Violence or harm
   - Adult content
   - Misinformation
   - Privacy violations

2. **Geographic Restrictions:**
   - Cannot be used outside designated territories
   - Check LICENSE file for details

3. **Usage Restrictions:**
   - Cannot use outputs to train other AI models (except derivatives)
   - Must include use restrictions in any distribution

## Additional Resources

- **Main README:** See `README.md` for detailed documentation
- **Bug Solutions:** See `docs/BUG_SOLUTIONS.md` for known issues
- **Technical Reports:** See `docs/report_*.md` for model details
- **License:** See `LICENSE` for full terms

## Support

For issues specific to Windows/WSL setup:
1. Check `docs/BUG_SOLUTIONS.md`
2. Verify GPU access with `nvidia-smi` in WSL
3. Ensure CUDA drivers are updated on Windows
4. Check WSL version: `wsl --version` (should be WSL 2)

For general Open-Sora issues:
- GitHub: https://github.com/hpcaitech/Open-Sora
- Documentation: See `docs/` directory

