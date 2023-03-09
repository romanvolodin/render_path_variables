import bpy

from .handlers import format_render_output_path, revert_render_output_path
from .preferences import (
    CUSTOM_VARIABLES_OT_actions,
    CUSTOM_VARIABLES_UL_name_value,
    CustomVariablePropertiesGroup,
    Preferences,
)


bl_info = {
    "name": "Render Path Variables",
    "author": "Roman Volodin",
    "version": (1, 0, 0),
    "blender": (2, 83, 0),
    "category": "Render",
}

classes = (
    CUSTOM_VARIABLES_UL_name_value,
    CustomVariablePropertiesGroup,
    CUSTOM_VARIABLES_OT_actions,
    Preferences,
)


def register():
    for class_ in classes:
        bpy.utils.register_class(class_)

    bpy.app.handlers.render_pre.append(format_render_output_path)
    bpy.app.handlers.render_post.append(revert_render_output_path)
    bpy.app.handlers.render_cancel.append(revert_render_output_path)


def unregister():
    for class_ in classes:
        bpy.utils.unregister_class(class_)

    bpy.app.handlers.render_pre.remove(format_render_output_path)
    bpy.app.handlers.render_post.remove(revert_render_output_path)
    bpy.app.handlers.render_cancel.remove(revert_render_output_path)


if __name__ == "__main__":
    register()
