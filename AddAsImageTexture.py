bl_info = {
    "name": "AddAsImageTexture",
    "description": "Add current uv map image as real texture",
    "author": "Chichige-Bobo",
    "version": (1, 1),
    "blender": (2, 69),
    "location": "UV/ImageEditor > AddAsTexture(header)",
    "warning": "", # used for warning icon and text in addons panel
    "wiki_url": "",
    "category": "UV"}

#############################################################
# 1.New material added if no one exists or use active one. 
#   (not assign to any faces explicitly.)
#   
# Cycles -------------
#   2.AttributeNode with UV map name and ImageTextureNode added.
#   3.If no output node found, new output and diffuse nodes are added then connected.  
# 
# Internal (node) -------
#   2.GeometryNode with UV map name and TextureNode added.
#   3.If no output node found, new output and material nodes are added then connected.  
#
# Internal (slots) --------
#   2.New texture added on next to last texture.
#     (at least, last texture slot must be empty)
#   3.Set the image and change the mapping to UV. done.
#
#############################################################
# ChangeLog
#   1.1 Node support (Cycles and Internal) added. 
#   1.0 released
##############################################################

import bpy

class AddAsImageTexture(bpy.types.Operator):
    bl_label = "Add UVTexture Image As Image Texture"
    bl_idname = "object.add_as_image_texture"
    bl_options = {'UNDO'} 
 
    @classmethod
    def poll(cls, context):
        
        if context.mode != 'OBJECT' or context.area.type != 'IMAGE_EDITOR': 
            return False
        
        actObj = context.active_object 
        if not actObj or actObj.type != 'MESH': #should not restrict to mesh?
            return False
        
        actSpace = context.area.spaces.active
        if not context.edit_image or actSpace.mode != 'VIEW':# or actSpace.show_render:
            return False
        
        return True    
       
    def execute(self, context):
        if not context.active_object.data.uv_textures.active:
            self.report({'WARNING'}, 'No UVMapping layer is found.')    
            return {'CANCELLED'}
        
        if context.scene.render.engine == 'CYCLES':
            return self.whenCycles(context)
        else:
            return self.whenInternal(context)
    
    #====================================
    def whenCycles(self, context):
        actObj = context.active_object #guaranteed it's not null at poll()
        mat = actObj.active_material
        
        if mat:
            if not mat.node_tree: # a material made at the Internal has no node_tree.
                mat.use_nodes = True # This creates node_tree and default two nodes.
                mat.use_nodes = False # Respect current state.
                               
        else:
            mat = bpy.data.materials.new('UVTexMaterial') # This doesn't create node_tree
            mat.use_nodes = True
            
            if len(actObj.material_slots) != 0:#slot with empty material exists.
                # below is worked for both 'DATA' and 'OBJECT'
                actObj.material_slots[actObj.active_material_index].material = mat
            else:
                actObj.data.materials.append(mat)
             
        #-----
        nodes = mat.node_tree.nodes                    

        texNode = nodes.new('ShaderNodeTexImage')
        texNode.image = context.edit_image
        texNode.location = [-300, 300]
        attrNode = nodes.new('ShaderNodeAttribute')
        attrNode.attribute_name = actObj.data.uv_textures.active.name
        attrNode.location = [-600 ,300]
        mat.node_tree.links.new(attrNode.outputs['Vector'], texNode.inputs['Vector'])
         
        if len(nodes) == 4 and nodes[0].type == 'OUTPUT_MATERIAL' and nodes[1].type == 'BSDF_DIFFUSE':
            mat.node_tree.links.new(texNode.outputs['Color'], nodes[1].inputs['Color'])
        else: # Situation which not default and no output node exists 
            outNode = None
            for n in mat.node_tree.nodes:
                if n.type == 'OUTPUT_MATERIAL':
                    outNode = n
                    break
                
            if not outNode:
                difNode = nodes.new(type = 'ShaderNodeBsdfDiffuse')
                difNode.location = [10, 300]
                outNode = nodes.new(type = 'ShaderNodeOutputMaterial')
                outNode.location = [300,300]
                mat.node_tree.links.new(difNode.outputs['BSDF'], outNode.inputs['Surface'])
                mat.node_tree.links.new(texNode.outputs['Color'], difNode.inputs['Color'])                  

        for n in mat.node_tree.nodes:
            n.select = (n == attrNode or n == texNode)

        mat.node_tree.nodes.active = texNode
                                    
        if mat.use_nodes:
            self.report({'INFO'}, 'Texture is successfully added to slots!')            
        else:
            self.report({'WARNING'}, 'Careful, UseNodes is off. ImageTexNode is successfully added though.')
                 
        return {'FINISHED'}
    
    #==============================================
    def whenInternal(self, context):
        actObj = context.active_object #guaranteed it's not null at poll()
        mat = actObj.active_material
                
        if mat:
            if not mat.use_nodes and mat.texture_slots[17]:
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

        #-----
        tex = bpy.data.textures.new(context.edit_image.name, type = 'IMAGE')#ImageTexture
        tex.image = context.edit_image

        if mat.use_nodes:
            nodes = mat.node_tree.nodes
            
            texNode = nodes.new(type = 'ShaderNodeTexture')
            texNode.texture = tex
            texNode.location = [-300, 300]
            geoNode = nodes.new(type = 'ShaderNodeGeometry')
            geoNode.uv_layer = actObj.data.uv_textures.active.name
            geoNode.location = [-600 ,300]
            mat.node_tree.links.new(geoNode.outputs['UV'], texNode.inputs['Vector'])
                   
            if len(nodes) == 4 and nodes[0].type == 'OUTPUT' and nodes[1].type == 'MATERIAL':
                mat.node_tree.links.new(texNode.outputs['Color'], nodes[1].inputs['Color'])
            else: # Situation which not default and no output node exists 
                outNode = None
                for n in mat.node_tree.nodes:
                    if n.type == 'OUTPUT':
                        outNode = n
                        break
                    
                if not outNode:
                    matNode = nodes.new(type = 'ShaderNodeMaterial')
                    matNode.location = [10, 300]
                    outNode = nodes.new(type = 'ShaderNodeOutput')
                    outNode.location = [300,300]
                    mat.node_tree.links.new(matNode.outputs['Color'], outNode.inputs['Color'])
                    mat.node_tree.links.new(texNode.outputs['Color'], matNode.inputs['Color'])                   

            for n in mat.node_tree.nodes:
                n.select = (n == geoNode or n == texNode)
            mat.node_tree.nodes.active = texNode
            
            self.report({'INFO'}, 'Texture node is successfully added!')
            
        else:
            for i in range(16, -1, -1): #texture_slots[17] is already checked as empty
                if mat.texture_slots[i] is not None:
                    destIndex = i + 1
                    break
                elif i == 0:
                    destIndex = 0
                    break

            texSlot = mat.texture_slots.create(destIndex) #MaterialTextureSlot
            texSlot.texture_coords = 'UV'
            texSlot.uv_layer = actObj.data.uv_textures.active.name #MeshTexturePolyLayer.name
            texSlot.texture = tex
            mat.active_texture_index = destIndex
            self.report({'INFO'}, 'Texture is successfully added to slots!')            
             
        return {'FINISHED'}

def image_editor_add_as_texture_button(self, context):

    layout = self.layout

    row = layout.row()
    row.operator("object.add_as_image_texture", text="AddAsTex", icon='FACESEL_HLT')
    
#######################
def register():
    bpy.utils.register_class(AddAsImageTexture)
    bpy.types.IMAGE_HT_header.append(image_editor_add_as_texture_button)
    
def unregister():
    bpy.utils.unregister_class(AddAsImageTexture)
    bpy.types.IMAGE_HT_header.remove(image_editor_add_as_texture_button)
    
if __name__ == "__main__":
    register()
