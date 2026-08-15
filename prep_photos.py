"""Auto-crop product shots to their content bbox and export web-ready JPEGs."""
import sys
from pathlib import Path
from PIL import Image, ImageChops

SRC = Path(r"C:\Users\Yarik\Desktop\Проекты\Инфографика\ИНФОГРАФИКА_\Масло 8шт кр_фото")
OUT = Path(r"C:\Users\Yarik\Desktop\GlowAroma\assets\img")
OUT.mkdir(parents=True, exist_ok=True)


def content_bbox(im, threshold=195):
    g = im.convert("L").point(lambda p: 255 if p < threshold else 0)
    return g.getbbox()


def export(src_path, out_name, pad=0.10, ratio=1.0, width=1400):
    im = Image.open(src_path).convert("RGB")
    box = content_bbox(im)
    if not box:
        print("no content:", src_path.name)
        return
    l, t, r, b = box
    w, h = r - l, b - t
    cx, cy = l + w / 2, t + h / 2
    side_w = w * (1 + pad * 2)
    side_h = h * (1 + pad * 2)
    if side_w / side_h < ratio:
        side_w = side_h * ratio
    else:
        side_h = side_w / ratio
    l = max(0, int(cx - side_w / 2))
    t = max(0, int(cy - side_h / 2))
    r = min(im.width, int(cx + side_w / 2))
    b = min(im.height, int(cy + side_h / 2))
    crop = im.crop((l, t, r, b))
    crop = crop.resize((width, int(width * crop.height / crop.width)), Image.LANCZOS)
    out = OUT / out_name
    crop.save(out, "JPEG", quality=86, optimize=True, progressive=True)
    print(f"{out_name}: {crop.width}x{crop.height} {out.stat().st_size // 1024} KB")


if __name__ == "__main__":
    export(SRC / "IMG_20250210_200307.jpg", "set8-box-front.jpg", ratio=0.82)
    export(SRC / "IMG_20250210_201107.jpg", "set8-open.jpg", ratio=1.15)
    export(SRC / "IMG_20250210_201242.jpg", "set8-open-angle.jpg", ratio=1.3)
    export(SRC / "IMG_20250210_200613.jpg", "set8-alt-a.jpg", ratio=1.0)
    export(SRC / "IMG_20250210_201334.jpg", "set8-alt-b.jpg", ratio=1.0)
