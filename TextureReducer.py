bl_info = {
    "name": "Texture Reducer - New UVMap",
    "author": "Chichige Bobo",
    "version": (0, 1),
    "blender": (2, 75, 0),
    "location": "Image-Window > Tool > Tools > TextureReducer",
    "description": "Create new uv map for a merged image",
    "warning": "Don't use this yet. Just backup purpose.",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Add Mesh"}

import bpy, bmesh
from bpy.props import BoolProperty, BoolVectorProperty, FloatProperty, FloatVectorProperty, IntProperty, IntVectorProperty, EnumProperty, StringProperty, PointerProperty

class TextureReducerOperator(bpy.types.Operator):
    """Make new UVMap for merged image"""
    bl_idname = "chichige.texture_reducer_operator"
    bl_label = "Texture Reducer Operator"
    bl_options = {'UNDO', 'INTERNAL'} #INTERNAL is that because numbers required to run.
    
    @classmethod
    def poll(cls, context):
        obj = context.object
        return context.mode == 'EDIT_MESH' and obj is not None# and obj.type == 'MESH'
    
    def execute(self, context):
        obj = context.object
        if len(obj.data.uv_layers) < 1:
            self.report({'WARNING'}, "No UVMap is found! Aborted")
            return {'CANCELLED'}
        elif len(obj.data.uv_layers) == 8:
            self.report({'WARNING'}, "There's already 8 UV maps. No room for new one. Aborted.")
            return {'CANCELLED'}
        
        bm = bmesh.from_edit_mesh(obj.data)
        
        selFaceCount = 0
        for face in bm.faces:
            if face.select:
                selFaceCount += 1
        
        if selFaceCount == 0:
            self.report({'WARNING'}, "No UVMap is found! Aborted.")
            bm.free()
            return {'CANCELLED'}                
        
        #bmesh.loops.layers.uv.new() doesn't make copy.
        bpy.ops.mesh.uv_texture_add()
        uv_act = bm.loops.layers.uv.active

        for face in bm.faces:
            if not face.select:
                continue
            
            for loop in face.loops:
                loop[uv_act].uv.x += 1
                loop[uv_act].uv.y += 1
                            
        bmesh.update_edit_mesh(obj.data)
        
        self.report({'INFO'}, "success!")
        return {'FINISHED'}

class TextureReducerPanel(bpy.types.Panel):
    """Texture Reducer Panel"""
    bl_idname = "chichige.texture_reducer_panel"
    bl_label = "Texture Reducer"
    
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'TOOLS'
    bl_category = 'Tools'   
           
    #Panels in ImageEditor are using .poll() instead of bl_context.
    @classmethod
    def poll(cls, context):
        sd = context.space_data
        return sd.show_uvedit and not context.tool_settings.use_uv_sculpt
        
        #This shows while OBJECT mode but EDIT_MESH mode. I don't know why
        #return obj is not None and obj.type == 'MESH'
    
    def draw(self, context):
        props = context.scene.chichige_texture_reducer_props
        
        layout = self.layout
        layout.prop(props, "method", expand = True)
        if props.method == 'GRID':
            layout.prop(props, "columns_rows")
            layout.prop(props, "cell_xy")
        else:
            layout.prop(props, "image_wh")
            layout.prop(props, "target_xy")
            layout.prop(props, "target_wh")
            
        layout.operator(TextureReducerOperator.bl_idname, text = "Create New UVMap", icon = 'GROUP_UVS')

class TextureReducerProps(bpy.types.PropertyGroup):
    columns_rows = IntVectorProperty(name = "Cols,Rows", description = "Grid : Columns & Rows", default = (3, 3), min = 1, max = 1000, size = 2)
    cell_xy = IntVectorProperty(name = "Cell XY", description = "Grid : position of the cell", default = (1, 1), min = 1, max = 1000, size = 2)
    image_wh = IntVectorProperty(name = "Image WH", description = "XY : width and height of merged image", default = (1024, 1024), min = 0, max = 999999, size = 2)
    target_xy = IntVectorProperty(name = "Target XY", description = "XY : upper left position of target portion", default = (100, 100), min = 0, max = 999999, size = 2)
    target_wh = IntVectorProperty(name = "Target WH", description = "XY : width and height of target portion", default = (300, 200), min = 0, max = 999999, size = 2)
    method = EnumProperty(items = [('GRID', 'GRID', 'Grid version'), 
                                    ('XY', 'XY', 'XY version')],
                                         name="Method",
                                         description="Way of execution",
                                         default="GRID")
def register():
    bpy.utils.register_class(TextureReducerProps)
    bpy.types.Scene.chichige_texture_reducer_props = PointerProperty(type = TextureReducerProps)

    bpy.utils.register_class(TextureReducerOperator)
    bpy.utils.register_class(TextureReducerPanel)

def unregister():
    bpy.utils.unregister_class(TextureReducerProps)
    del bpy.types.Scene.chichige_texture_reducer_props
    
    bpy.utils.unregister_class(TextureReducerOperator)
    bpy.utils.unregister_class(TextureReducerPanel)
    
if __name__ == "__main__":
    register()
