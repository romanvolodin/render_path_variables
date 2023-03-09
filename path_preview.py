import textwrap
from os.path import abspath, basename, splitext

import bpy


def create_multiline_label(context, text, parent):
    pixels_per_char = 7
    chars_per_line = int(context.region.width / pixels_per_char)
    wrapper = textwrap.TextWrapper(width=chars_per_line)
    text_lines = wrapper.wrap(text=text)
    for text_line in text_lines:
        parent.label(text=text_line)


def format_render_output_path(scene):
    path = abspath(bpy.path.abspath(scene.render.filepath))
    blendname, _ = splitext(basename(bpy.data.filepath))
    return path.format(blendname=blendname).replace("/", " / ")


class RenderPathPreviewPanel(bpy.types.Panel):
    """Panel shows formatted render path"""

    bl_label = "Render Path Preview"
    bl_idname = "RENDER_PT_render_path_preview"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "output"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Absolute render path:")

        try:
            text = format_render_output_path(context.scene)
        except ValueError as err:
            text = f"Error: {err}"
            layout.alert = True

        layout.scale_y = 0.5
        create_multiline_label(context, text, layout)
