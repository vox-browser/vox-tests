"""Locate the implementation separately from the versioned parity suite."""
import os
from pathlib import Path


def vox_root():
    value = os.environ.get('VOX_SOURCE_DIR')
    if not value:
        raise RuntimeError('Set VOX_SOURCE_DIR to the canonical Vox checkout')
    root = Path(value).resolve()
    if not (root / 'cpuraster').is_dir():
        raise RuntimeError('VOX_SOURCE_DIR does not contain cpuraster: ' + str(root))
    return root
