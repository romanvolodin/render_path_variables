import bpy


class CUSTOM_VARIABLES_UL_name_value(bpy.types.UIList):
    def draw_item(
        self, context, layout, data, item, icon, active_data, active_propname, index
    ):
        layout.prop(data=item, property="name", text="")
        layout.prop(data=item, property="value", text="")


class CustomVariablePropertiesGroup(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(
        name="Custom Variable Name",
        description="The name of the custom variable",
    )
    value: bpy.props.StringProperty(
        name="Custom Variable Value",
        description="The value of the custom variable",
    )


class CUSTOM_VARIABLES_OT_actions(bpy.types.Operator):
    """Move items up and down, add and remove"""

    bl_idname = "custom_render_path_variables.list_action"
    bl_label = "List Actions"
    bl_description = "Move items up and down, add and remove"
    bl_options = {"REGISTER"}

    action: bpy.props.EnumProperty(
        items=(
            ("UP", "Up", ""),
            ("DOWN", "Down", ""),
            ("REMOVE", "Remove", ""),
            ("ADD", "Add", ""),
        )
    )

    def invoke(self, context, event):
        preferences = context.preferences.addons[__package__].preferences
        active_variable_index = preferences.active_variable_index

        if self.action == "ADD":
            preferences.custom_variables.add()
            preferences.active_variable_index = len(preferences.custom_variables) - 1

        if self.action == "REMOVE":
            preferences.custom_variables.remove(active_variable_index)

        if self.action == "UP" and active_variable_index >= 1:
            preferences.custom_variables.move(
                active_variable_index, active_variable_index - 1
            )
            preferences.active_variable_index -= 1

        if (
            self.action == "DOWN"
            and active_variable_index < len(preferences.custom_variables) - 1
        ):
            preferences.custom_variables.move(
                active_variable_index, active_variable_index + 1
            )
            preferences.active_variable_index += 1

        return {"FINISHED"}


class Preferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    custom_variables: bpy.props.CollectionProperty(
        type=CustomVariablePropertiesGroup,
        name="Custom variables",
        description="Custom variables which will be used in render path",
        options={"HIDDEN"},
    )

    active_variable_index: bpy.props.IntProperty(
        name="Index of selected custom variable",
        default=0,
        options={"HIDDEN"},
    )

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="name")
        row.label(text="value")

        row = layout.row()
        row.template_list(
            "CUSTOM_VARIABLES_UL_name_value",
            "",
            self,
            "custom_variables",
            self,
            "active_variable_index",
            rows=len(self.custom_variables),
        )

        col = row.column(align=True)
        col.operator(
            "custom_render_path_variables.list_action",
            icon="ADD",
            text="",
        ).action = "ADD"
        col.operator(
            "custom_render_path_variables.list_action",
            icon="REMOVE",
            text="",
        ).action = "REMOVE"
        col.separator()
        col.operator(
            "custom_render_path_variables.list_action",
            icon="TRIA_UP",
            text="",
        ).action = "UP"
        col.operator(
            "custom_render_path_variables.list_action",
            icon="TRIA_DOWN",
            text="",
        ).action = "DOWN"
