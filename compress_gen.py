"""Compress KIE output PNGs into web-ready JPEGs."""
from pathlib import Path
from PIL import Image

GEN = Path(__file__).parent / "assets" / "gen"
TARGETS = {
    "hero-atmosphere": 2200,
    "scene-kitchen": 1100,
    "scene-evening": 1100,
    "scene-guests": 1100,
    "scene-gift": 1100,
}

for stem, width in TARGETS.items():
    src = GEN / f"{stem}.png"
    if not src.exists():
        print("missing:", src.name)
        continue
    im = Image.open(src).convert("RGB")
    if im.width > width:
        im = im.resize((width, round(width * im.height / im.width)), Image.LANCZOS)
    out = GEN / f"{stem}.jpg"
    im.save(out, "JPEG", quality=84, optimize=True, progressive=True)
    print(f"{out.name}: {im.width}x{im.height} {out.stat().st_size // 1024} KB")
    src.unlink()
