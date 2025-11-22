resolution = "240p"  # Lower resolution for RTX 2080 Super
aspect_ratio = "16:9"  # Standard widescreen
num_frames = 51  # ~2 seconds at 24fps
fps = 24
frame_interval = 1
save_fps = 24

save_dir = "./samples/"
seed = 42
batch_size = 1
multi_resolution = "STDiT2"
dtype = "bf16"
condition_frame_length = 5
align = 5

model = dict(
    type="STDiT3-XL/2",
    from_pretrained="hpcai-tech/OpenSora-STDiT-v3",  # Will auto-download
    qk_norm=True,
    enable_flash_attn=True,
    enable_layernorm_kernel=True,
)
vae = dict(
    type="OpenSoraVAE_V1_2",
    from_pretrained="hpcai-tech/OpenSora-VAE-v1.2",  # Will auto-download
    micro_frame_size=17,
    micro_batch_size=4,
)
text_encoder = dict(
    type="t5",
    from_pretrained="./ckpts/google/t5-v1_1-xxl",  # Use already downloaded
    model_max_length=300,
)
scheduler = dict(
    type="rflow",
    use_timestep_transform=True,
    num_sampling_steps=30,
    cfg_scale=7.0,
)

aes = 6.5
flow = None

