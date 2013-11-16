import bpy

#######################
# ApplyCurrentUVTextureImage
#   what this script does...
#       create real texture with current uv map image
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

class ApplyCurrentUVTextureImage(bpy.types.Operator):
    bl_label = "Apply Current UVTexture Image"
    bl_idname = "object.apply_uv_texture_image"
    bl_options = {'REGISTER', 'UNDO'} 
 
    @classmethod
    def poll(cls, context):
        if bpy.context.area.type != 'IMAGE_EDITOR':
            return False
        
        if bpy.context.edit_image is None:
            return False
                
        actObj = context.active_object
        if actObj.type != 'MESH':
            return False
        
        if actObj.data.uv_textures.active is None:
            return False
        
        return True    
       
    def execute(self, context):
        actObj = context.active_object
                 
        mat = actObj.active_material
        if mat is not None:
            if mat.use_nodes:
                self.report({'ERROR'}, 'Material node is not supported!')    
                return {'CANCELED'}
            if mat.texture_slots[17] is not None:
                self.report({'ERROR'} ,'Texture slot is full!')
                return {'CANCELED'}
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
        
        #actUV is MeshTexturePolyLayer class
        actUV = actObj.data.uv_textures.active
        
        tex = bpy.data.textures.new(context.edit_image.name, type = 'IMAGE')#ImageTexture
        tex.image = context.edit_image
        
        texSlot = mat.texture_slots.create(destIndex) #MaterialTextureSlot
        texSlot.texture_coords = 'UV'
        texSlot.use_map_color_diffuse = True
        texSlot.uv_layer = actUV.name
        texSlot.texture = tex
         
        self.report({'INFO'}, 'Texture is successfully added!')
        return {'FINISHED'}
    
#######################
def register():
    bpy.utils.register_class(ApplyCurrentUVTextureImage)
    
def unregister():
    bpy.utils.unregister_class(ApplyCurrentUVTextureImage)
    
if __name__ == "__main__":
    register()
