import bpy


class CUSTOM_VARIABLES_UL_name_value(bpy.types.UIList):
    def draw_item(
        self, context, layout, data, item, icon, active_data, active_propname, index
    ):
        layout.prop(data=item, property="name", text="")
        layout.prop(data=item, property="value", text="")


class CustomVariablesPropertiesGroup(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(
        name="Field Name",
        description="The name of the field to import",
        default="Имя переменной",
    )
    value: bpy.props.StringProperty(
        name="Field Name",
        description="The name of the field to import",
        default="Значение переменной",
    )


class CUSTOM_VARIABLES_OT_actions(bpy.types.Operator):
    """Move items up and down, add and remove"""

    bl_idname = "custom.list_action"
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
        preferences = context.preferences.addons[__name__].preferences
        active_data_field_index = preferences.active_data_field_index

        if self.action == "ADD":
            preferences.data_fields.add()
            preferences.active_data_field_index = len(preferences.data_fields) - 1

        if self.action == "REMOVE":
            preferences.data_fields.remove(active_data_field_index)

        if self.action == "UP" and active_data_field_index >= 1:
            preferences.data_fields.move(
                active_data_field_index, active_data_field_index - 1
            )
            preferences.active_data_field_index -= 1

        if (
            self.action == "DOWN"
            and active_data_field_index < len(preferences.data_fields) - 1
        ):
            preferences.data_fields.move(
                active_data_field_index, active_data_field_index + 1
            )
            preferences.active_data_field_index += 1

        return {"FINISHED"}


class Preferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    data_fields: bpy.props.CollectionProperty(
        type=CustomVariablesPropertiesGroup,
        name="Field names",
        description="All the fields that should be imported",
        options={"HIDDEN"},
    )

    active_data_field_index: bpy.props.IntProperty(
        name="Index of data_fields",
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
            "data_fields",
            self,
            "active_data_field_index",
            rows=len(self.data_fields),
        )

        col = row.column(align=True)
        col.operator("custom.list_action", icon="ADD", text="").action = "ADD"
        col.operator("custom.list_action", icon="REMOVE", text="").action = "REMOVE"
        col.separator()
        col.operator("custom.list_action", icon="TRIA_UP", text="").action = "UP"
        col.operator("custom.list_action", icon="TRIA_DOWN", text="").action = "DOWN"
