from os.path import basename, splitext

import bpy

from bpy.app.handlers import persistent


@persistent
def format_render_output_path(scene):
    path = scene.render.filepath
    blendname, _ = splitext(basename(bpy.data.filepath))
    scene["old_render_filepath"] = path
    scene.render.filepath = path.format(blendname=blendname)


@persistent
def revert_render_output_path(scene):
    scene.render.filepath = scene["old_render_filepath"]
    del scene["old_render_filepath"]