#!/usr/bin/env python3
# Datei: png2webp.py
from pathlib import Path
import sys
from typing import Optional

try:
    from PIL import Image
except ImportError:
    print("Bitte zuerst Pillow installieren: pip install Pillow")
    sys.exit(1)


def convert_images_to_webp(directory: Path, overwrite: bool = False, quality: Optional[int] = None,
                         lossless: bool = True, max_width: Optional[int] = None, max_height: Optional[int] = None):
    image_files = [p for p in directory.iterdir() if p.is_file() and p.suffix.lower() in [".png", ".jpg", ".jpeg"]]
    if not image_files:
        print("Keine .png, .jpg oder .jpeg Dateien im aktuellen Ordner gefunden.")
        return

    converted = 0
    for image_path in image_files:
        webp_path = image_path.with_suffix(".webp")
        if webp_path.exists() and not overwrite:
            print(f"⚠️  Überspringe (bereits vorhanden): {webp_path.name}")
            continue

        try:
            with Image.open(image_path) as im:
                # ggf. verkleinern (schont stark die Dateigröße)
                if max_width or max_height:
                    im.thumbnail((max_width or im.width, max_height or im.height), Image.LANCZOS)

                if im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info):
                    im = im.convert("RGBA")
                else:
                    im = im.convert("RGB")
                save_kwargs = {"method": 6}
                if lossless:
                    save_kwargs.update(lossless=True)
                elif quality is not None:
                    save_kwargs.update(quality=quality)
                im.save(webp_path, "WEBP", **save_kwargs)

            print(f"✅ {image_path.name} → {webp_path.name}")
            converted += 1
        except Exception as e:
            print(f"❌ Fehler bei {image_path.name}: {e}")

    print(f"Fertig. {converted} Datei(en) konvertiert.")


def resize_webps_to_square(
    directory: Path,
    size: int = 1200,
    overwrite: bool = True,
    quality: Optional[int] = None,
    lossless: bool = True,
):
    """Resize all .webp images in directory to an exact size x size canvas.

    - Preserves aspect ratio by fitting within the square and padding.
    - Uses a solid white background (#ffffff) for padding (flattened, no alpha).
    - Re-encodes using provided lossless/quality settings.
    """
    webp_files = [p for p in directory.iterdir() if p.is_file() and p.suffix.lower() == ".webp"]
    if not webp_files:
        print("Keine .webp Dateien zum Anpassen gefunden.")
        return

    resized = 0
    for webp_path in webp_files:
        try:
            with Image.open(webp_path) as im:
                orig_w, orig_h = im.width, im.height

                # Skip if already the exact target size
                if orig_w == size and orig_h == size and not overwrite:
                    print(f"⚠️  Überspringe (bereits {size}x{size}): {webp_path.name}")
                    continue

                # Work in RGBA for correct compositing, then flatten to white RGB
                if im.mode != "RGBA":
                    im = im.convert("RGBA")

                # Fit within the square while preserving aspect ratio
                scale = min(size / im.width, size / im.height) if im.width and im.height else 1.0
                new_w = max(1, int(round(im.width * scale)))
                new_h = max(1, int(round(im.height * scale)))

                if new_w != im.width or new_h != im.height:
                    im = im.resize((new_w, new_h), Image.LANCZOS)

                # Create square canvas with solid white background
                canvas = Image.new("RGB", (size, size), (255, 255, 255))
                left = (size - im.width) // 2
                top = (size - im.height) // 2
                # Paste with mask to respect alpha, resulting image is flattened (no alpha)
                canvas.paste(im, (left, top), im)

                save_kwargs = {"method": 6}
                if lossless:
                    save_kwargs.update(lossless=True)
                elif quality is not None:
                    save_kwargs.update(quality=quality)

                canvas.save(webp_path, "WEBP", **save_kwargs)

            print(f"🔁 Größe angepasst: {webp_path.name} → {size}x{size}")
            resized += 1
        except Exception as e:
            print(f"❌ Fehler beim Anpassen von {webp_path.name}: {e}")

    print(f"Quadratisches Format fertig. {resized} Datei(en) angepasst.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Konvertiert alle .png, .jpg und .jpeg im aktuellen Ordner zu .webp.")
    parser.add_argument("-o", "--overwrite", action="store_true", help="Vorhandene .webp-Dateien überschreiben.")
    parser.add_argument("--lossy", action="store_true", help="Verlustbehaftet statt lossless speichern.")
    parser.add_argument("-q", "--quality", type=int, help="Qualität 0-100 (nur relevant mit --lossy).")
    parser.add_argument("--max-width", type=int, help="Maximale Breite vor dem Speichern.")
    parser.add_argument("--max-height", type=int, help="Maximale Höhe vor dem Speichern.")
    parser.add_argument("--square-size", type=int, default=1200, help="Zielgröße für quadratisches Canvas (Standard 1200).")
    args = parser.parse_args()

    convert_images_to_webp(
        Path("."),
        overwrite=args.overwrite,
        quality=args.quality if args.lossy else None,
        lossless=not args.lossy,
        max_width=args.max_width,
        max_height=args.max_height
    )

    # Zweiter Schritt: Alle .webp auf exaktes Quadrat bringen
    resize_webps_to_square(
        Path("."),
        size=args.square_size,
        overwrite=True,
        quality=args.quality if args.lossy else None,
        lossless=not args.lossy,
    )
