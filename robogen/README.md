# robogen – maschinenlesbare Bauanleitungen für Roboter in Blender

KI-Agenten erzeugen hier keine Prosa-Anleitungen, sondern eine strukturierte
`build_spec.yaml`, aus der ein deterministisches Blender-Python-Skript das Modell
baut. Ein Verifikationsschritt rendert Ortho-Ansichten und vergleicht die
Silhouetten per IoU mit den Referenzbildern (Ziel: > 0,8).

## Dateien

| Datei | Zweck |
|---|---|
| `build_spec.yaml` | Spezifikation „hexbot": Proportionen (als Bruchteile der Gesamthöhe), Teile-Hierarchie, Primitive mit Maßen, Materialien |
| `generate.py` | Baut das Modell in Blender: `blender -b -P generate.py -- build_spec.yaml` |
| `verify.py` | Rendert Front/Rück/Seite als Ortho-Silhouetten und gibt IoU gegen Referenzen aus |

## Ablauf

1. **Analyse:** Agent liest 4 Referenzansichten (front/back/side) und erzeugt die Spec.
2. **Build:** `generate.py` erzeugt Teile aus Primitiven (Cube/Cylinder/UV-Sphere) + Bevel, symmetrisch gespiegelt.
3. **Verify:** `verify.py` rendert Ortho-Ansichten, IoU gegen Referenzen; bei < 0,8 Spec korrigieren und neu bauen.

## Voraussetzungen

- Blender 4.x (headless: `blender -b`)
- Python-Zusatzpakete nur für `verify.py`: `pip install pyyaml numpy pillow`

## Agenten-Prompt-Template (neue Figur aus Referenzbildern)

> Extrahiere aus den 4 Ortho-Ansichten Silhouette, Proportionen (Bruchteile der
> Gesamthöhe), Teile-Hierarchie und Materialien. Gib ausschließlich eine
> `build_spec.yaml` im vorhandenen Schema aus – kein Freitext.
