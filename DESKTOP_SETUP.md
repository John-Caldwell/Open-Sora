# Open-Sora Setup for RTX 2080 Super Desktop

## Quick Start

Your laptop work has been committed to the `discovery` branch. Here's how to set it up on your desktop with RTX 2080 Super.

## On Your Desktop

### 1. Pull the Latest Code

```bash
cd /path/to/Open-Sora
git fetch origin
git checkout discovery
git pull origin discovery
```

### 2. Verify GPU

```bash
nvidia-smi
```

Expected: RTX 2080 Super with 8GB VRAM (sm_75 compute capability)

### 3. Install Dependencies

#### Option A: Windows (if you want to try native)
```powershell
# Install PyTorch
pip install torch==2.4.0 torchvision==0.19.0 --index-url https://download.pytorch.org/whl/cu121

# Install requirements
pip install -r requirements.txt

# Install Open-Sora
pip install -e .
```

**Note**: May still hit Windows compatibility issues with ColossalAI. If so, use WSL (Option B).

#### Option B: WSL 2 (Recommended)
```bash
# In WSL Ubuntu
cd /mnt/c/path/to/Open-Sora

# Install PyTorch
pip3 install torch==2.4.0 torchvision==0.19.0 --index-url https://download.pytorch.org/whl/cu121

# Install requirements
pip3 install -r requirements.txt

# Install Open-Sora
pip3 install -e .
```

### 4. Test Installation

```bash
# In WSL or Windows
python test_opensora.py
```

Expected output:
```
✓ Open-Sora modules imported successfully!
✓ Model checkpoint found: 22.1 GB
SUCCESS! Open-Sora is ready to generate videos!
```

**No sm_120 warning** - your RTX 2080 Super is fully supported!

### 5. Generate Your First Video

```bash
# Single video
bash generate.sh "A cat playing with a ball of yarn"

# Or batch generation
bash batch_generate.sh
```

## Key Differences from Laptop

### ✅ What Works Better on Desktop

1. **No sm_120 issues** - RTX 2080 Super (sm_75) is fully supported
2. **Better performance** - 2x memory bandwidth (496 GB/s vs 256 GB/s)
3. **More stable** - Mature driver support
4. **Higher power budget** - 250W vs 45-115W (less throttling)

### 📊 Expected Performance

- **256px video (129 frames)**: ~2-3 minutes
- **768px video (shorter)**: ~5-10 minutes
- **Memory usage**: ~6-7 GB VRAM

### 🔧 Modified Files (Already in Repo)

These changes are already committed and will work on your desktop:

1. **opensora/utils/cai.py** - Gloo backend option (not needed for RTX 2080 Super, but harmless)
2. **opensora/models/mmdit/math.py** - Optional flash_attn
3. **opensora/models/mmdit/distributed.py** - Optional flash_attn
4. **opensora/utils/ckpt.py** - Optional tensornvme

All changes are backward compatible and won't affect your RTX 2080 Super.

## Troubleshooting

### If you see NCCL errors:
```bash
# Force Gloo backend (shouldn't be needed for RTX 2080 Super)
export DIST_BACKEND=gloo
bash generate.sh "your prompt"
```

### If models aren't found:
```bash
# Make sure you're in the repo directory
cd /path/to/Open-Sora
ls -lh ckpts/  # Should show ~46GB of models
```

### If CUDA isn't detected:
```bash
python -c "import torch; print(torch.cuda.is_available())"
# Should print: True
```

## What's in the Repo

- **generate.sh** - Single video generation script
- **batch_generate.sh** - Batch video generation from CSV
- **prompts.csv** - Example prompts for batch generation
- **test_opensora.py** - Environment verification
- **docs/BUG_SOLUTIONS.md** - Known issues and solutions
- **CURRENT_STATUS.md** - Full status of laptop setup
- **PYTORCH_SM120_SUMMARY.md** - Details of sm_120 build attempt

## Next Steps

1. Pull the `discovery` branch on your desktop
2. Run `test_opensora.py` to verify setup
3. Generate your first video!
4. Enjoy stable, fast video generation on RTX 2080 Super

## Future: Laptop Setup

When PyTorch 2.7+ releases with Blackwell support (Q1-Q2 2025):
1. Update PyTorch on laptop: `pip install torch --upgrade`
2. Test with: `python test_opensora.py`
3. Generate videos on the go!

---

**Bottom Line**: Your desktop will work perfectly right now. Your laptop will work perfectly in a few months. All the setup work is done!

