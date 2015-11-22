###########
# GPL
###########
# ConnectBackToRigify : ver 1.0
#
# What to do...
#     Change all Armature modifier to selected armature.
#     Abort if multiple armatures are found in selected objects.
#     Note: All armature mods will get changed regardless related armatures.
#
# How to use...
#     Select Mesh objects and an Armature object.
#     (Other selected objects will be ignored (e.g. lamp))
#     Run this script.
##########

import bpy

def main():    
    if len(bpy.context.selected_objects) == 0:
        print("Warning: Nothing selected")
        return
    
    selectObjs = bpy.context.selected_objects
    armatureCount = 0
    rigifyObj = None
    for obj in selectObjs:
        if obj.type == 'ARMATURE':
            rigifyObj = obj
            armatureCount += 1
    
    if armatureCount == 0:
        print("Warning: No armature is selected.")
        return
    elif armatureCount >= 2:
        print("Warning: Multiple armatures are selected")
        return

    #----- point armature modifier to new rig ----
    for obj in selectObjs:
        if obj.type == 'MESH':
            for m in obj.modifiers:
                if m.type == 'ARMATURE':
                    m.object = rigifyObj
    
    print('ConnectBackToRigify : Done!')
    

################################################
################################################
main() #I wanna use 'return' to abort
