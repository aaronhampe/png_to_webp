<h1>png2webp – Produktbilder einheitlich</h1>
Kleines Python-Tool, das alle .png im aktuellen Ordner in .webp konvertiert und anschließend jedes .webp auf ein exaktes Quadrat (Standard: 1200×1200 px) bringt – ideal für konsistente Produktbilder im Shop.

<h2>Features</h2>
Batch-Konvertierung: .png → .webp (verlustfrei oder lossy).

Optionales Downsizing vor dem Speichern: --max-width / --max-height.

Einheitliches Seitenverhältnis: Zentriert auf weißem 1200×1200-Canvas (Padding, keine Verzerrung).

Transparenz smart gehandhabt:

In der Konvertierung: Opaque → RGB, mit Alpha → RGBA (WebP mit Transparenz).

Beim Quadratisieren: Bild wird auf Weiß flach zusammengesetzt (keine Transparenz im Endbild).

<h2>Voraussetzungen</h2>
Python 3.8+

Pillow (PIL):

<i>
pip install Pillow</i> <br> <br>
<h2>Installation & Ausführung</h2>
Datei png2webp.py in den Zielordner legen (dort, wo die Bilder liegen).

Terminal/PowerShell in diesem Ordner öffnen.

Ausführen, z. B.:


<i>
python png2webp.py --lossy -q 80 --max-width 1200</i> <br> <br>

<h2>Empfohlene Presets</h2>
Produkt-Hauptbilder:

<i>
python png2webp.py --lossy -q 80 --max-width 1200</i> <br> <br>

Kategorieseiten/Thumbnails (kleiner & schneller):


<i>
python png2webp.py --lossy -q 75 --max-width 600 --square-size 600</i> <br> <br>

Richtwerte: Für schnelle LCP peile ~100–150 KB fürs Hauptbild an. Thumbnails eher 20–60 KB.

<h2>CLI-Optionen</h2>

-o, --overwrite     Überschreibt vorhandene .webp in der KONVERTIERUNG.
--lossy             Verlustbehaftete WebP-Kodierung (sonst lossless).
-q, --quality N     Qualität 0–100 (nur mit --lossy relevant).
--max-width N       Max. Breite vor dem Speichern (Seitenverhältnis bleibt).
--max-height N      Max. Höhe vor dem Speichern.
--square-size N     Zielgröße des quadratischen Canvas (Default: 1200).
<h3>Wichtiges Verhalten</h3>
Zwei Schritte in einem Lauf:

.png → .webp

Alle .webp im Ordner → quadratisch (weißes Padding).

Der Quadrat-Schritt überschreibt immer die .webp-Dateien mit der quadratischen Version.

Liegen im Ordner bereits .webp (z. B. Logos/Icons), werden auch diese auf Quadrat gebracht. Ggf. vorher auslagern.

<h2>Beispiele (Windows, macOS, Linux)</h2>
Verlustfrei (größer, aber ohne Verluste):

<i>
python png2webp.py --max-width 1200</i> <br> <br>

Stärker komprimiert:

<i>
python png2webp.py --lossy -q 75 --max-width 1200</i> <br> <br>

Exaktes Quadrat 1600×1600:

<i>
python png2webp.py --lossy -q 80 --square-size 1600</i> <br> <br>

<h3>Output prüfen (optional)</h3>
Liste Größe & Modus aller .webp:

<i>
python - << "PY"
from pathlib import Path
from PIL import Image
for f in Path(".").glob("*.webp"):
    with Image.open(f) as im:
        print(f"{f.name:40}  {im.size}  {im.mode}")
PY</i> <br> <br>

<h3>Tipps für kleine Dateien</h3>
Qualität anpassen: -q 80 ist oft visuell „verlustfrei genug“.
Bei Bedarf in 5er-Schritten testen: 85 → 80 → 75.

Vorab skalieren: Downsizing auf 1200 px (oder 1000 px) bringt meist mehr als noch mehr Kompressionsdruck.

Transparenz vermeiden: Wenn nicht nötig, werden Bilder automatisch als RGB gespeichert – spart Bytes.

Lazy Loading & srcset: Im Shop loading="lazy" und responsive Größen ausspielen.

<h2>Troubleshooting </h2>
ImportError: Pillow
→ pip install Pillow

Lanczos/Resampling-Warnung
Bei sehr neuen/alten Pillow-Versionen kann Image.LANCZOS eine Warnung ausgeben.
Lösung: Pillow aktualisieren (pip install -U Pillow) oder im Code Image.Resampling.LANCZOS verwenden.

Ungewollt weiße Ränder
Das ist beabsichtigt: Das Tool zentriert und füllt auf Weiß, um ein exaktes Quadrat zu garantieren.
Wenn du die Transparenz behalten willst, müsstest du den Quadrat-Schritt anpassen/überspringen.

