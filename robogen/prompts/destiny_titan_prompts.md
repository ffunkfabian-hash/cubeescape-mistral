# Prompt-Sammlung: Destiny-2-ähnlicher Titan (Layer für Layer)

Sequenzielle Agenten-Prompts zum Aufbau einer `build_spec.yaml` für einen
Destiny-2-ähnlichen Titanen (Wächter-Klasse: massive Schulterplatten, schwere
Brustplatte, Helm mit Visier, klobige Panzerhandschuhe). Jeder Layer erweitert
die Spec im vorhandenen Schema (`robogen/build_spec.yaml`) um genau einen
Bauteil-Layer. Layer strikt in Reihenfolge ausführen; nach jedem Layer
`blender -b -P generate.py -- <spec>` laufen lassen, damit die Spec valide bleibt.

Charakteristische Merkmale (Zielbild):
- Gesamthöhe ca. 2.10 m, sehr breite Schultern (ca. 0.95 m inkl. Pauldrons)
- Kompakter, tiefer Schwerpunkt; Brustkorb massiv und kantig
- Große, überhängende Schulterplatten (Pauldrons) — das dominanteste Merkmal
- Helm mit schmalem, leuchtendem Visier
- Klobige Gauntlets, gepanzerte Stiefel, Gürtel mit Klassen-Symbol (Mark)

---

## Layer 0 — Meta & Proportionen

**Ziel:** Grundgerüst der Spec: Meta-Block, Proportionen als Bruchteile der Gesamthöhe.

**Prompt:**
> Erzeuge den Kopf einer `build_spec.yaml` im vorhandenen Schema von `robogen/build_spec.yaml` für einen Destiny-2-ähnlichen Titanen. Fülle nur `meta` (name: `titan`, unit: meters, origin/forward/up/right wie im hexbot-Beispiel, total_height: 2.10) und `proportions`. Proportionen: head_height 0.22, shoulder_width (inkl. Pauldrons) 0.95, torso_height 0.62, leg_length 0.95, upper_arm 0.34, forearm 0.30. Gib ausschließlich valides YAML aus — kein Freitext.

**Erwartete Ausgabe:** `meta:` + `proportions:` Block.

**Prüfkriterium:** YAML parst fehlerfrei; Summe der Höhenanteile konsistent mit total_height.

---

## Layer 1 — Torso / Brustkorb

**Ziel:** Massiver, kantiger Brustkorb mit Brustplatte und Bauchsegment.

**Prompt:**
> Erweitere die Titanen-Spec um das Part `torso` (parent: none, material: armor_steel). Baue es aus Cubes mit Bevel: Hauptbrustkorb als breiter, flacher Kasten (size ca. [0.62, 0.36, 0.55], center z ca. 1.45), darüber eine kantige Brustplatte (size ca. [0.50, 0.06, 0.35], vorne versetzt, leicht überstehend), darunter ein schmalerer Bauchblock (size ca. [0.44, 0.30, 0.35], center z ca. 1.02). Füge einen zentralen "Reactor"-Akzent als flachen Cylinder (vertices: 6, radius 0.10, vorne auf der Brust, material: glow_core). Gib nur den YAML-Block für `parts: [- id: torso ...]` aus.

**Erwartete Ausgabe:** Part `torso` mit 4 Primitiven.

**Prüfkriterium:** `generate.py` läuft fehlerfrei; Brustkorb in Frontalansicht breiter als hoch.

---

## Layer 2 — Helm mit Visier

**Ziel:** Kompakter Helm mit schmalem, leuchtendem Visier-Schlitz.

**Prompt:**
> Erweitere die Titanen-Spec um das Part `head` (parent: torso, material: armor_steel). Helm als Cube (size ca. [0.34, 0.34, 0.26], center z ca. 1.92, bevel 0.05), darüber ein Kamm/Helmgrat als schmaler Cube (size ca. [0.10, 0.30, 0.10], oben mittig). Visier als flaches, längliches Element vorne: Cube (size ca. [0.24, 0.02, 0.05], loc y ca. -0.18, z ca. 1.93, material: visor_glow). Optional: zwei kleine "Hörner"/Flügel als Cubes seitlich am Helm. Gib nur den YAML-Block für das Part `head` aus.

**Erwartete Ausgabe:** Part `head` mit Helm, Kamm, Visier.

**Prüfkriterium:** Visier sitzt in der Frontalansicht mittig auf Gesichtshöhe; `generate.py` OK.

---

## Layer 3 — Schulterplatten (Pauldrons)

**Ziel:** Die dominanten, großen, überhängenden Schulterplatten — das Markenzeichen des Titans.

**Prompt:**
> Erweitere die Titanen-Spec um die Parts `pauldron_L` und `pauldron_R` (parent: torso, material: armor_steel). Jede Pauldron besteht aus: einer großen, klobigen Hauptplatte (Cube, size ca. [0.30, 0.30, 0.22], loc x ca. ±0.46, z ca. 1.62, bevel 0.06) und einer überstehenden Kappe oben (Cube, size ca. [0.34, 0.34, 0.10], loc x ca. ±0.46, z ca. 1.78, bevel 0.04), die seitlich überhängt. Optional ein kleiner Spike als Kegel/Cylinder vorne oben (material: glow_core als Akzent). Spiegele L/R exakt über die X-Achse. Gib nur die YAML-Blöcke für beide Parts aus.

**Erwartete Ausgabe:** Parts `pauldron_L`, `pauldron_R` mit je 2–3 Primitiven.

**Prüfkriterium:** In der Frontal-Silhouette deutlich breiter als der Torso; `generate.py` OK.

---

## Layer 4 — Arme & Gauntlets

**Ziel:** Dicke Oberarme, breite Unterarme und klobige Panzerhandschuhe.

**Prompt:**
> Erweitere die Titanen-Spec um die Parts `arm_L` und `arm_R` (parent: torso, material: armor_steel). Pro Arm: Oberarm als Cube (size ca. [0.16, 0.16, 0.34], loc x ca. ±0.42, z ca. 1.42), Unterarm als breiterer Cube (size ca. [0.18, 0.18, 0.30], loc x ca. ±0.42, z ca. 1.05, bevel 0.03) und Gauntlet/Hand als klobiger Block (size ca. [0.20, 0.18, 0.16], loc x ca. ±0.42, z ca. 0.82, material: armor_dark). Spiegele L/R exakt. Gib nur die YAML-Blöcke für beide Parts aus.

**Erwartete Ausgabe:** Parts `arm_L`, `arm_R` mit je 3 Primitiven.

**Prüfkriterium:** Gauntlets enden auf Höhe der Oberschenkelmitte; `generate.py` OK.

---

## Layer 5 — Beine, Gürtel & Stiefel

**Ziel:** Dicke Oberschenkel, Kniepanzer, schwere Stiefel sowie Gürtel mit Mark (Klassen-Symbol).

**Prompt:**
> Erweitere die Titanen-Spec um die Parts `leg_L`, `leg_R` und `belt` (parent: torso). Pro Bein: Oberschenkel als Cube (size ca. [0.20, 0.20, 0.48], loc x ca. ±0.15, z ca. 0.72), Unterschenkel als Cube (size ca. [0.17, 0.17, 0.45], loc x ca. ±0.15, z ca. 0.26), Knie als kleiner Block vorne (size ca. [0.16, 0.10, 0.12], z ca. 0.50, vorne versetzt), Stiefel als langer, breiter Schuh (size ca. [0.22, 0.34, 0.10], loc x ca. ±0.15, y ca. -0.05, z ca. 0.05, material: armor_dark). Gürtel: flacher breiter Ring als Cube (size ca. [0.48, 0.34, 0.10], z ca. 1.28, material: armor_dark) plus Mark (Klassen-Symbol) als kleiner Zylinder (vertices: 3, radius 0.09, depth 0.03, vorne am Gürtel, material: glow_core). Gib nur die YAML-Blöcke aus.

**Erwartete Ausgabe:** Parts `leg_L`, `leg_R`, `belt`.

**Prüfkriterium:** Stiefel stehen stabil auf z=0; Gesamthöhe bleibt ca. 2.10 m; `generate.py` OK.

---

## Layer 6 — Materialien

**Ziel:** Material-Palette im Destiny-Stil: matte Panzerung, dunkle Gelenke, leuchtende Akzente.

**Prompt:**
> Erweitere die Titanen-Spec um den Block `materials`. Definiere: `armor_steel` (base_color ca. [0.55, 0.58, 0.62], metallic 0.6, roughness 0.35), `armor_dark` (base_color ca. [0.12, 0.12, 0.14], metallic 0.4, roughness 0.5), `glow_core` (base_color dunkel, emission z. B. [0.2, 0.6, 1.0], emission_strength 6.0), `visor_glow` (emission z. B. [1.0, 0.6, 0.1], emission_strength 8.0). Gib nur den YAML-Block `materials:` aus.

**Erwartete Ausgabe:** 4 Material-Definitionen im vorhandenen Schema.

**Prüfkriterium:** Alle in Primitiven referenzierten Materialnamen existieren; `generate.py` OK.

---

## Layer 7 — Build-Order & Verifikation

**Ziel:** `build_order` setzen und den Verify-Loop gegen Referenz-Silhouetten fahren.

**Prompt:**
> Vervollständige die Titanen-Spec um `build_order` (Reihenfolge: torso, belt, head, pauldron_L, pauldron_R, arm_L, arm_R, leg_L, leg_R) und den Block `verification` (render_views front/back/side wie im hexbot-Beispiel, target_iou: 0.8). Gib nur diese YAML-Blöcke aus.

**Verifikation (manuell/agent):**
1. `blender -b -P generate.py -- titan_spec.yaml` → `BUILD OK`
2. `blender -b scene.blend -P verify.py -- refs/front.png refs/back.png refs/side.png` → IoU mean > 0,8
3. Bei IoU < 0,8: fehlende Layer-Linie identifizieren (meist Pauldron-Breite oder Helm-Höhe), entsprechenden Layer-Prompt mit Korrekturhinweis erneut ausführen.
