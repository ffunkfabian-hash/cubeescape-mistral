"""Build a robot in Blender from build_spec.yaml. Run: blender -b -P generate.py"""
import bpy
import yaml
import math
import sys
from mathutils import Vector

SPEC_PATH = sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv else "build_spec.yaml"


def load_spec(path):
    with open(path) as f:
        return yaml.safe_load(f)["build_spec"]


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for block in (bpy.data.meshes, bpy.data.curves, bpy.data.materials,
                  bpy.data.cameras, bpy.data.lights):
        for item in list(block):
            if item.users == 0:
                block.remove(item)


def make_material(name, cfg):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*cfg["base_color"], 1.0)
    bsdf.inputs["Roughness"].default_value = cfg.get("roughness", 0.5)
    bsdf.inputs["Metallic"].default_value = cfg.get("metallic", 0.0)
    if "emission" in cfg:
        bsdf.inputs["Emission Color"].default_value = (*cfg["emission"], 1.0)
        bsdf.inputs["Emission Strength"].default_value = cfg.get("emission_strength", 1.0)
    return mat


def add_primitive(prim, mats):
    ptype = prim["type"]
    if ptype == "cube":
        bpy.ops.mesh.primitive_cube_add(location=prim["loc"])
        obj = bpy.context.active_object
        obj.scale = [s / 2 for s in prim["scale"]]
    elif ptype == "uv_sphere":
        bpy.ops.mesh.primitive_uv_sphere_add(location=prim["loc"], segments=32, ring_count=16)
        obj = bpy.context.active_object
        obj.scale = prim.get("scale", [prim["radius"]] * 3)
    elif ptype == "cylinder":
        bpy.ops.mesh.primitive_cylinder_add(
            location=prim["loc"], vertices=prim.get("vertices", 32),
            radius=prim["radius"], depth=prim["depth"])
        obj = bpy.context.active_object
        rot = prim.get("rot", [0, 0, 0])
        obj.rotation_euler = [math.radians(a) for a in rot]
    else:
        raise ValueError(f"unknown primitive type: {ptype}")
    bpy.ops.object.transform_apply(scale=True, rotation=True)
    bevel = prim.get("bevel")
    if bevel:
        mod = obj.modifiers.new("bevel", "BEVEL")
        mod.width = bevel
        mod.segments = 2
    mat_name = prim.get("material")
    if mat_name and mat_name in mats:
        obj.data.materials.append(mats[mat_name])
    return obj


def build():
    spec = load_spec(SPEC_PATH)
    clear_scene()
    mats = {name: make_material(name, cfg) for name, cfg in spec["materials"].items()}
    root = bpy.data.objects.new("ROOT", None)
    bpy.context.collection.objects.link(root)
    parts = {}
    for part in spec["parts"]:
        holder = bpy.data.objects.new(part["id"], None)
        bpy.context.collection.objects.link(holder)
        holder.parent = root
        prims = [add_primitive(p, mats) for p in part["primitives"]]
        for p in prims:
            p.parent = holder
        parts[part["id"]] = holder
    for part in spec["parts"]:
        parent_id = part.get("parent")
        if parent_id and parent_id in parts:
            parts[part["id"]].parent = parts[parent_id]
    return spec, root


if __name__ == "__main__":
    spec, root = build()
    print(f"BUILD OK: {spec['meta']['name']} with {len(spec['parts'])} parts")
