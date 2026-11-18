#!/usr/bin/env python3
"""Create screenshot comparisons using Machado et al. 2009 dichromacy matrices.

Run with the project's Pillow and NumPy installations. This is an audit aid,
not a claim that simulation replaces testing with people with colour-vision
deficiency.
"""
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
MATRICES = {
    "Protanopia simulation": np.array([
        [0.152286, 1.052583, -0.204868],
        [0.114503, 0.786281, 0.099216],
        [-0.003882, -0.048116, 1.051998],
    ]),
    "Deuteranopia simulation": np.array([
        [0.367322, 0.860646, -0.227968],
        [0.280085, 0.672501, 0.047413],
        [-0.011820, 0.042940, 0.968881],
    ]),
}
SCREENSHOTS = {
    "overview": "review/animations/overview-viewport.png",
    "country": "review/animations/country-viewport.png",
    "company_size": "review/animations/company-size-viewport.png",
    "industry": "review/animations/industry-viewport.png",
    "barrier_ranking": "review/animations/barriers-after-viewport.png",
    "barrier_comparison": "review/animations/barriers-after-section-3.png",
    "conclusion": "review/animations/conclusion-viewport.png",
}


def simulate(image: Image.Image, matrix: np.ndarray) -> Image.Image:
    srgb = np.asarray(image.convert("RGB"), dtype=np.float64) / 255
    linear = np.where(srgb <= 0.04045, srgb / 12.92, ((srgb + 0.055) / 1.055) ** 2.4)
    transformed = np.clip(linear @ matrix.T, 0, 1)
    encoded = np.where(transformed <= 0.0031308, 12.92 * transformed,
                       1.055 * transformed ** (1 / 2.4) - 0.055)
    return Image.fromarray(np.uint8(np.rint(np.clip(encoded, 0, 1) * 255)))


def main() -> None:
    out_dir = ROOT / "review/accessibility"
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, source in SCREENSHOTS.items():
        original = Image.open(ROOT / source).convert("RGB")
        width, height = original.size
        label_height = 34
        sheet = Image.new("RGB", (width * 3, height + label_height), "white")
        draw = ImageDraw.Draw(sheet)
        font = ImageFont.load_default()
        for index, (label, image) in enumerate([
            ("Reference", original),
            ("Protanopia simulation", simulate(original, MATRICES["Protanopia simulation"])),
            ("Deuteranopia simulation", simulate(original, MATRICES["Deuteranopia simulation"])),
        ]):
            x = width * index
            draw.text((x + 10, 10), label, fill="#17324D", font=font)
            sheet.paste(image, (x, label_height))
        sheet.save(out_dir / f"{name}-cvd-review.jpg", quality=86, optimize=True)


if __name__ == "__main__":
    main()
