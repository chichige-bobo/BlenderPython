bl_info = {
    "name": "Mesh Order Research",
    "author": "Chichige-Bobo",
    "version": (1, 0),
    "blender": (2, 69, 0),
    "location": "View3D > Toolbar ",
    "description": "Everytime hit the button, next vertex/edge/face will be selected",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Mesh"}

import bpy
from bpy.props import *

class MeshOrderResearchOperator(bpy.types.Operator):
    """Advance to the next index when the button pressed"""
    bl_idname = "addongen.mesh_order_research_operator"
    bl_label = "Mesh Order Research Operator"
    bl_options = {'REGISTER','UNDO'}

    curIndex = IntProperty(min = 0)
    type = StringProperty()
    
    @classmethod
    def poll(cls, context):
        return context.object and context.object.type == 'MESH'
     
    def execute(self, context):
        me = context.object.data
        
        bpy.ops.object.mode_set(mode = 'OBJECT')
        for p in me.polygons:
            p.select = False
        for e in me.edges:
            e.select = False
        for v in me.vertices:
            v.select = False         
            
        if self.type == 'MeshLoop':
            self.loopMeshLoop(me)   
        elif self.type == 'Vertices':
            self.loopVertices(me)
        elif self.type == 'Edges':
            self.loopEdges(me)
        elif self.type == 'Polygons':
            self.loopPolygons(me)
        else:
            self.report({'WARNING'}, 'Done nothing')
            
        self.curIndex += 1
        bpy.ops.object.mode_set(mode = 'EDIT')
        
        return {'FINISHED'}
        
    def loopMeshLoop(self, me):
        if self.curIndex >= len(me.loops):
            self.curIndex = 0
        print(self.curIndex)
        me.vertices[me.loops[self.curIndex].vertex_index].select = True

    def loopVertices(self, me):
        if self.curIndex >= len(me.vertices):
            self.curIndex = 0
        print(self.curIndex)        
        me.vertices[self.curIndex].select = True
        
    def loopEdges(self, me):       
        if self.curIndex >= len(me.edges):
            self.curIndex = 0
        print(self.curIndex)
        me.edges[self.curIndex].select = True
        
    def loopPolygons(self, me):
               
        if self.curIndex >= len(me.polygons):
            self.curIndex = 0
        print(self.curIndex)
        me.polygons[self.curIndex].select = True
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "curIndex", text = "index")
        
class MeshOrderResearchPanel(bpy.types.Panel):
    bl_idname = "VIEW3D_PT_mesh_order_research"
    bl_label = "Mesh Order Research Panel"
    
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Tools'
    
    def draw(self, context):
        layout = self.layout
        layout.operator(MeshOrderResearchOperator.bl_idname, text = "MeshLoop", icon = 'LAYER_ACTIVE').type = "MeshLoop"
        layout.operator(MeshOrderResearchOperator.bl_idname, text = "Vertices", icon = 'VERTEXSEL').type = "Vertices"
        layout.operator(MeshOrderResearchOperator.bl_idname, text = "Edges", icon = 'EDGESEL').type = "Edges"
        layout.operator(MeshOrderResearchOperator.bl_idname, text = "Polygons", icon = 'FACESEL').type = "Polygons"

def register():
    bpy.utils.register_class(MeshOrderResearchOperator)
    bpy.utils.register_class(MeshOrderResearchPanel)

def unregister():
    bpy.utils.unregister_class(MeshOrderResearchOperator)
    bpy.utils.unregister_class(MeshOrderResearchPanel)
    
if __name__ == "__main__":
    register()
