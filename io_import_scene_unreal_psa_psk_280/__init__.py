# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

"""
Version': '2.0' ported by Darknet

Unreal Tournament PSK file to Blender mesh converter V1.0
Author: D.M. Sturgeon (camg188 at the elYsium forum), ported by Darknet
Imports a *psk file to a new mesh

-No UV Texutre
-No Weight
-No Armature Bones
-No Material ID
-Export Text Log From Current Location File (Bool )
"""

"""
Version': '2.7.*' edited by befzz
Github: https://github.com/Befzz/blender3d_import_psk_psa
- Pskx support
- Animation import updated (bone orientation now works)
- Skeleton import: auto-size, auto-orient bones
- UVmap, mesh, weights, etc. import revised
- Extra UVs import

- No Scale support. (no test material)
- No smoothing groups (not exported by umodel)
"""

"""
Version': '2.8.0' edited by floxay
- Vertex normals import (VTXNORMS chunk)
        (requires custom UEViewer build /at the moment/)
"""

"""
Edited by matyalatte
- Rename objects
- Apply smooth shading
- Set false to Down Scale as default
- Change unit scale to 0.01
- Add an UI panel to combine psk skeleton and gltf mesh
- Split files
"""

# https://github.com/gildor2/UModel/blob/master/Exporters/Psk.h

import bpy
from . import io_import_scene_unreal_psa_psk_280
from . import combine_psk_and_gltf, export_as_fbx

if "bpy" in locals():
    import importlib
    if "io_import_scene_unreal_psa_psk_280" in locals():
        importlib.reload(io_import_scene_unreal_psa_psk_280)
    if "combine_psk_and_gltf" in locals():
        importlib.reload(combine_psk_and_gltf)
    if "export_as_fbx" in locals():
        importlib.reload(export_as_fbx)
bl_info = {
    "name": "Import Unreal Skeleton Mesh (.psk)/Animation Set (.psa) (280)",
    "author": "Darknet, flufy3d, camg188, befzz, matyalatte",
    "version": (2, 8, 0),
    "blender": (2, 80, 0),
    "location": "File > Import > Skeleton Mesh (.psk)/Animation Set (.psa) OR View3D > Tool Shelf (key T) > Misc. tab",
    "description": "Import Skeleton Mesh / Animation Data",
    "warning": "",
    "wiki_url": "https://github.com/Befzz/blender3d_import_psk_psa",
    "category": "Import-Export",
    "tracker_url": "https://github.com/Befzz/blender3d_import_psk_psa/issues"
}

def register():
    io_import_scene_unreal_psa_psk_280.register()
    combine_psk_and_gltf.register()
    export_as_fbx.register()

def unregister():
    io_import_scene_unreal_psa_psk_280.unregister()
    combine_psk_and_gltf.unregister()
    export_as_fbx.unregister()