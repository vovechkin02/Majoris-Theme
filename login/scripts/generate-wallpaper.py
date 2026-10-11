#!/usr/bin/env python3
"""Precompose the prototype's gradients/ellipses/veil/diagonals once, not per frame."""
import json
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
W, H = 1920, 1080
Y, X = np.mgrid[0:H, 0:W].astype(float)


def rgb(text):
    return tuple(int(text.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))


for variant, t in json.loads((ROOT / 'theme/tokens.json').read_text()).items():
    base = np.empty((H, W, 3), dtype=float)
    base[:] = rgb(t['wall-base'])
    for cx, cy, color, opacity in [(0.19, .82, (100, 101, 244), .36 * .68), (.78, .22, (118, 124, 236), .26 * .68)]:
        distance = np.sqrt(((X / W - cx) / .65) ** 2 + ((Y / H - cy) / .65) ** 2)
        alpha = np.clip(1 - distance / .7, 0, 1)[..., None] * opacity
        base = base * (1 - alpha) + np.array(color) * alpha
    image = Image.fromarray(np.uint8(base)).convert('RGBA')
    for bounds, token, opacity in [
        ((-.16 * W, .65 * H, .42 * W, 1.41 * H), 'orb-a', .7),
        ((.62 * W, -.35 * H, 1.2 * W, .35 * H), 'orb-b', .73),
        ((.45 * W, .87 * H, .8 * W, 1.39 * H), 'orb-c', .65),
    ]:
        layer = Image.new('RGBA', (W, H))
        ImageDraw.Draw(layer).ellipse(bounds, fill=(*rgb(t[token]), round(255 * opacity)))
        image = Image.alpha_composite(image, layer.filter(ImageFilter.GaussianBlur(44)))
    veil = np.clip(1 - np.abs((X / W * .64 + Y / H * .36) - .48) / .5, 0, 1)
    color, opacity = ((240, 245, 255), .24) if variant == 'light' else ((6, 12, 35), .27)
    layer = np.empty((H, W, 4), dtype=np.uint8)
    layer[:, :, :3] = color
    layer[:, :, 3] = np.uint8(veil * opacity * 255)
    image = Image.alpha_composite(image, Image.fromarray(layer))
    lines = Image.new('RGBA', (W, H))
    draw = ImageDraw.Draw(lines)
    color = (255, 255, 255, 45) if variant == 'light' else (216, 225, 255, 6)
    for position in [.43, .49, .55]:
        x = W * position
        draw.line((x - H * .58, H, x + H * .58, 0), fill=color, width=2)
    image = Image.alpha_composite(image, lines).convert('RGB')
    image.resize((3840, 2160), Image.Resampling.LANCZOS).save(ROOT / f'assets/wallpapers/{variant}.png', optimize=True)
