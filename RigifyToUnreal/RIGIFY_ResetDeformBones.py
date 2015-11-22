###########
# GPL
###########
# ResetDeformBones : ver 1.0
#
# What to do...
#     Reset all deform bones (without constraints) of selected Rigify armature.
#     You will need this when accidentally set an Action which for 'Unrigify' rig.
#     i.e. if mesh object has odd distortion, you mistakenly had set a baked Action to the rigify object. 
#
# How to use...
#     Select a rigify object that causing weird distortion and Run this script. 
###########

import bpy

def main():
    bpy.ops.object.mode_set(mode = 'OBJECT')

    obj = bpy.context.object
    for b in obj.pose.bones:
        if b.name.startswith("DEF-") and len(b.constraints) == 0:
            b.location = (0, 0, 0)
            b.rotation_euler = (0, 0, 0)
            b.rotation_quaternion = (1, 0, 0, 0)
            b.scale = (1, 1, 1)
    
############
obj = bpy.context.object
if obj and obj.type == 'ARMATURE':
    main()    
