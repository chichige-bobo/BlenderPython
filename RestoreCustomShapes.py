import bpy

##################
# Restore deleted CustomShape objects
#   why : mesh data linked new object cannot be used to edit custom shape.  
#   how : select some bones (no matter if it has custom shape or not) in PoseMode
#         or Armature object in ObjectMode. Then RunScript.
#   subject : against selected bones in Pose mode. All bones in Object mode.
#   where : restore on layer 20
#   for Blender ver2.69
#   by chichige-bobo
##################

curScene = bpy.context.scene

if bpy.context.active_object.type == 'ARMATURE':
    armObj = bpy.context.active_object
        
    #if in ObjectMode, toggle mode then select all.
    if bpy.context.mode != 'POSE':
        bpy.ops.object.mode_set(mode='POSE')
        for bone in armObj.data.bones:
            bone.select = True
        
    selectedBones = bpy.context.selected_pose_bones
    if selectedBones is not None: #never be False if run in Object mode
        
        restoredShapes = []

        for bone in selectedBones:
            c_shape = bone.custom_shape
            if c_shape is not None and curScene not in c_shape.users_scene:
                curScene.objects.link(c_shape)
                restoredShapes.append(c_shape)
  
                #below did not worked well. Should do in ObjectMode
                #bpy.ops.object.move_to_layer(layers=[(i == 19) for i in range(20)])
         
        #-------change layer----------
        if restoredShapes is not None:
            bpy.ops.object.mode_set(mode='OBJECT')
            armObj.select = False #if not do, armature will also be affected by move_to_layer.
            
            for rs in restoredShapes:
                bpy.context.scene.objects.active = rs
                rs.select = True
                bpy.ops.object.move_to_layer(layers=[(i == 19) for i in range(20)])#[False, False,,,,,True]

            #if you want to return to pose mode...
            #bpy.context.scene.objects.active = armObj
            #bpy.ops.object.mode_set(mode='POSE')
        
        if len(restoredShapes) > 0:
            print(str(len(restoredShapes)) + ' shapes restored!')
        else:
            print('No custom shapes restored.')     
    
    else:
        print('No bone is selected.')            
else:
    print('Active object is not Armature.')
