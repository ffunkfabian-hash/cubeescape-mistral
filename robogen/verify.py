"""Render orthographic views and compare silhouettes against reference images (IoU).

Usage: blender -b scene.blend -P verify.py -- refs/front.png refs/back.png refs/side.png
Requires: numpy, pillow. pip install numpy pillow
"""
import bpy
import sys
import numpy as np
from PIL import Image

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []


def setup_ortho_camera():
    cam_data = bpy.data.cameras.new("ortho")
    cam_data.type = "ORTHO"
    cam_data.ortho_scale = 2.2
    cam = bpy.data.objects.new("ortho", cam_data)
    bpy.context.collection.objects.link(cam)
    bpy.context.scene.camera = cam
    return cam


def render_silhouette(cam, rot_euler, filepath, size=256):
    cam.rotation_euler = rot_euler
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE_NEXT" if hasattr(bpy.types, "EEVEE_NEXT") else "BLENDER_EEVEE"
    scene.render.resolution_x = size
    scene.render.resolution_y = size
    scene.render.filepath = filepath
    scene.render.film_transparent = True
    bpy.ops.render.render(write_still=True)
    img = np.array(Image.open(filepath).convert("RGBA"))
    return (img[..., 3] > 128)


def load_ref(path, size=256):
    img = np.array(Image.open(path).convert("RGBA").resize((size, size)))
    return (img[..., 3] > 128) if img.shape[-1] == 4 else (img.mean(axis=-1) < 200)


def iou(a, b):
    inter = np.logical_and(a, b).sum()
    union = np.logical_or(a, b).sum()
    return inter / union if union else 0.0


def main():
    cam = setup_ortho_camera()
    views = {"front": [1.5708, 0, 0], "back": [1.5708, 0, 3.1416], "side": [1.5708, 0, -1.5708]}
    results = {}
    for i, (name, rot) in enumerate(views.items()):
        out = f"/tmp/render_{name}.png"
        sil = render_silhouette(cam, rot, out)
        if i < len(argv):
            ref = load_ref(argv[i])
            results[name] = round(iou(sil, ref), 3)
        else:
            results[name] = "no ref"
    total = [v for v in results.values() if isinstance(v, float)]
    print("IOU_RESULTS", results, "MEAN", round(sum(total) / len(total), 3) if total else None)
    return results


if __name__ == "__main__":
    main()
