bl_info = {
    "name": "Shapes by Frames",
    "author": "Senshellshark",
    "version": (0, 1, 0),
    "blender": (2, 80, 0),
    "location": "View3D",
    "description": "Creates shape keys from animation frames named according to a text file",
    "warning": "",
    "doc_url": "",
    "category": "Object",
}


import bpy
from bpy.types import (
    Operator,
    Panel,
    PropertyGroup
)
from bpy.props import (
    PointerProperty,
    EnumProperty
)


class SBF_Properties(PropertyGroup):
    object : PointerProperty(name="Target", type=bpy.types.Object)
    names : PointerProperty(name="Frame Names", type=bpy.types.Text)


class SBF_PT_Panel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Shapes by Frames"
    bl_category = "Shape Keys"
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.sbf
        
        row = layout.row()
        col = row.column()
        col.prop(props, 'object')
        col.prop(props, 'names')
        col.operator("object.create_shape_keys", text="Create Shape Keys", icon="SHAPEKEY_DATA")


class SBF_OT_Create_Shape_Keys_Op(Operator):
    bl_idname = "object.create_shape_keys"
    bl_label = "Create Shape Keys"
    bl_description = "Create shape keys for every name, skipping blanks"
    
    @classmethod
    def poll(cls, context):
        obj = context.scene.sbf.object
        txt = context.scene.sbf.names
        
        if obj is not None and txt is not None:
            if obj.mode == "OBJECT":
                return True
        return False
    
    def execute(self, context):
        obj = context.scene.sbf.object
        txt = context.scene.sbf.names
        arm = obj.modifiers["Armature"]
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        
        for f in range(len(txt.lines)):
            context.scene.frame_current = f + 1
            shape_name = txt.lines[f].body
            bpy.ops.object.modifier_apply_as_shapekey(keep_modifier=True, modifier="Armature")
            obj.data.shape_keys.key_blocks[-1].name = shape_name
        context.scene.frame_current = 0
        return {'FINISHED'}


classes = (SBF_Properties, SBF_OT_Create_Shape_Keys_Op, SBF_PT_Panel)


def register():
    for c in classes:
        bpy.utils.register_class(c)
        bpy.types.Scene.sbf = PointerProperty(type=SBF_Properties)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
        del bpy.types.Scene.sbf


if __name__ == "__main__":
    register()
