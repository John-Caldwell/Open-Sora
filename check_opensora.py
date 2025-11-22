#!/usr/bin/env python3
"""Check if Open-Sora is properly installed."""

print("Checking Open-Sora installation...")
print()

try:
    import opensora
    print("✓ opensora module imported")
except ImportError as e:
    print(f"✗ Failed to import opensora: {e}")
    exit(1)

try:
    import colossalai
    print("✓ colossalai imported")
except ImportError as e:
    print(f"✗ Failed to import colossalai: {e}")
    exit(1)

try:
    from opensora.models.mmdit import Flux
    print("✓ Flux model imported")
except ImportError as e:
    print(f"✗ Failed to import Flux: {e}")
    exit(1)

try:
    from opensora.utils.inference import prepare_model
    print("✓ inference utils imported")
except ImportError as e:
    print(f"✗ Failed to import inference utils: {e}")
    exit(1)

print()
print("=" * 50)
print("All checks passed! Open-Sora is ready to use! 🚀")
print("=" * 50)

