#######################
# AddAsImageTexture
#   what this script does...
#       add real texture with current uv map image
#   details...
#       0.For internal renderer and not for node material
#       1.New material added if no one exists or use active one. 
#         (not assign to any faces explicitly.)
#       2.New texture added on next to last texture.
#         (at least, last texture slot must be empty)
#       3.Set the image and change the mapping to UV. done.
# ver 1.0
# by chichige-bobo.   
#######################

import bpy

bl_info = {
    "name": "AddAsImageTexture",
    "description": "Add current uv map image as real texture",
    "author": "Chichige-Bobo",
    "version": (1, 0),
    "blender": (2, 69),
    "location": "UV/ImageEditor>AddAsTexture(header)",
    "warning": "", # used for warning icon and text in addons panel
    "wiki_url": "",
    "category": "UV"}

class AddAsImageTexture(bpy.types.Operator):
    bl_label = "Add UVTexture Image As Image Texture"
    bl_idname = "object.add_as_image_texture"
    bl_options = {'REGISTER', 'UNDO'} 
 
    @classmethod
    def poll(cls, context):
        if context.area.type != 'IMAGE_EDITOR': 
            return False
        
        actObj = context.active_object 
        if actObj is None:
            return False
        
        if actObj.type != 'MESH': #should not restrict to mesh?
            return False
        
        return True    
       
    def execute(self, context):
        
        actObj = context.active_object #guaranteed it's not null at poll()
        
        if context.scene.render.engine != 'BLENDER_RENDER':
            self.report({'WARNING'}, 'Only InternalRenderer is supported.')    
            return {'CANCELLED'}
        if actObj.data.uv_textures.active is None:
            self.report({'WARNING'}, 'No UVMapping layer is found.')    
            return {'CANCELLED'}
        if context.edit_image is None: #this prop available only in IMAGE_EDITOR
            self.report({'WARNING'}, 'Image is not setted.')    
            return {'CANCELLED'}
        
        mat = actObj.active_material
        if mat:
            if mat.use_nodes:
                self.report({'WARNING'}, 'Material NODE is not supported.')    
                return {'CANCELLED'}
            if mat.texture_slots[17] is not None:
                self.report({'ERROR'} ,'Texture slot is full.')
                return {'CANCELLED'}
        else:
            mat = bpy.data.materials.new('UVTexMaterial')
            if len(actObj.material_slots) != 0:#slot with empty material exists
                #if actObj.material_slots[actObj.active_material_index].link == 'DATA':
                #   below is worked for both 'DATA' and 'OBJECT'
                actObj.material_slots[actObj.active_material_index].material = mat
            else:
                actObj.data.materials.append(mat)
       
        
        for i in range(16, -1, -1): #texture_slots[17] is already checked as empty
            if mat.texture_slots[i] is not None:
                destIndex = i + 1
                break
            elif i == 0:
                destIndex = 0
                break
               
        tex = bpy.data.textures.new(context.edit_image.name, type = 'IMAGE')#ImageTexture
        tex.image = context.edit_image
        
        texSlot = mat.texture_slots.create(destIndex) #MaterialTextureSlot
        texSlot.texture_coords = 'UV'
        texSlot.uv_layer = actObj.data.uv_textures.active.name #MeshTexturePolyLayer.name
        texSlot.texture = tex
         
        self.report({'INFO'}, 'Texture is successfully added!')
        return {'FINISHED'}


def image_editor_add_as_texture_button(self, context):

    layout = self.layout

    row = layout.row(align=True)
    row.operator("object.add_as_image_texture", text="AddAsTexture", icon='FACESEL_HLT')
    
#######################
def register():
    bpy.utils.register_class(AddAsImageTexture)
    bpy.types.IMAGE_HT_header.append(image_editor_add_as_texture_button)
    
def unregister():
    bpy.utils.unregister_class(AddAsImageTexture)
    bpy.types.IMAGE_HT_header.remove(image_editor_add_as_texture_button)
    
if __name__ == "__main__":
    register()
