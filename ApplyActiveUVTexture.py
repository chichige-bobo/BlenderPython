import bpy

#########################
# Internal renderer (not node) only.
# testing...
#########################

#bpy.data.meshes['Cube'].uv_textures['UVMap'].data[0].image  yields   xxxx.jpg
def mainLogic():
    actObj = bpy.context.active_object
    
    if actObj.type != 'MESH':
        print('Error: Active object is not Mesh!')
        return
     
    if actObj.data.uv_textures.active is None:
        print('Error: No UVMap is selected!')
        return
    
    if actObj.data.uv_textures.active.data[0].image is None:
        print('Error: The UVMap has no image!')
        return
    
    #######
    mat = actObj.active_material
    if mat is None:
        mat = bpy.data.materials.new('UVTexture')
        if len(actObj.material_slots) >= actObj.active_material_index:#slot with empty material exists
            #if actObj.material_slots[actObj.active_material_index].link == 'DATA':
            #   below is worked for both 'DATA' and 'OBJECT'
            actObj.material_slots[actObj.active_material_index].material = mat
        else:
            actObj.data.materials.append(mat)
   
    if mat.use_nodes:
        print('Error: Material node is not supported!')    
        return
    
    for i in range(17, -1, -1):
        if mat.texture_slots[i] is not None:
            if i == 17:
                print('Error: Texture slot is full!')
                break
            else:
                destIndex = i + 1
                break
        elif i == 0:
            destIndex = 0
            break
    
    #actUV is MeshTexturePolyLayer class, actUV.data[0] is MeshTexturePoly class
    actUV = actObj.data.uv_textures.active
    
    tex = bpy.data.textures.new(actUV.data[0].image.name, type = 'IMAGE')#ImageTexture class
    tex.image = actUV.data[0].image
    
    texSlot = mat.texture_slots.create(destIndex) #MaterialTextureSlot class
    texSlot.texture_coords = 'UV'
    texSlot.use_map_color_diffuse = True
    texSlot.uv_layer = actUV.name
    texSlot.texture = tex
     
    print('Success: Texture is added!')
    return

#######################
    
mainLogic()
