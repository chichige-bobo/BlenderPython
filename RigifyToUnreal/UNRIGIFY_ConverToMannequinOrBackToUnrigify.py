###########
# GPL
###########
# Conver to Mannequin or Back to Unrigify : ver 1.0
#
# What to do...
#     This script is aiming the 're-targeting' in UE4. (I don't know the retargeting well yet)
#     Subject is an armature and meshes just after the RigifyToUnreal script is applied.
#     Convert bone names and vertex group names from Rigify's to Mannequin's.
#     or reverse that name change.
#
# How to use...
#     Set isPitchiPoy variable below.
#     Select 'Unrigify' armature and meshes. (loose selection is ok.) 
#     Run this script to convert to names used in mannequin.
#     Run again to convert back to names used in rigify.
#     Convert direction is automatically detected
#     
#     Armature only or meshes only is supported.
#     Though, partial mesh only (w/o armature) is not allowed.
#     (Because checking torso bones to decide direction.) 
# 
# Some bones not matched and those with no correspond bones is not changed.
# Check for those after ran this script.
#
###################################
###################################
# False for traditional Rigify
# True for PitchiPoy version
isPitchiPoy = False
##################################
##################################



import bpy
 
#detect automatically in validate() then use this in main()
isBackward = False

def main():
    boneNames = getPitchiPoyBoneNames() if isPitchiPoy else getBoneNames() 

    changedBones = 0
    changedGroups = 0
            
    for obj in bpy.context.selected_objects:
        
        if obj.type == 'ARMATURE':
            bpy.context.scene.objects.active = obj
            bpy.ops.object.mode_set(mode = 'EDIT')
            for b in obj.data.edit_bones:
                for bn in boneNames:
                    if b.name == (bn[1] if isBackward else bn[0]):
                        b.name = bn[0] if isBackward else bn[1]
                        changedBones += 1
                        break
            bpy.ops.object.mode_set(mode = 'OBJECT')    
        
        elif obj.type == 'MESH':
            for vg in obj.vertex_groups:
                for bn in boneNames:
                    if vg.name == (bn[1] if isBackward else bn[0]):                            
                        vg.name = bn[0] if isBackward else bn[1]
                        changedGroups += 1 # BUG? when executed with an armature and a mesh selected, this line is not run. Though the line above seems executed.
                        break

    print('Done! ' + str(changedBones) + ' bones and ' + str(changedGroups) + ' vertex group names got changed.')

#=======================================================

def getBoneNames():
    # [rigify, mannequin]
    boneNames = [
              ['DEF-hips',       'pelvis'],
              ['DEF-spine',      'spine_01'],
              ['DEF-chest',      'spine_02'],
              ['DEF-neck',       'neck_01'], #spine_03 skipped
              ['DEF-head',       'head'],
              
              ['DEF-shoulder.L', 'clavicle_l'],
              
              ['DEF-upper_arm.01.L', 'upperarm_l'],
              ['DEF-upper_arm.02.L', 'upperarm_twist_01_l'],
              ['DEF-forearm.01.L',   'lowerarm_l'],
              ['DEF-forearm.02.L',   'lowerarm_twist_01_l'],
              ['DEF-hand.L',         'hand_l'],
              
              ['DEF-thumb.01.L.01',  'thumb_01_l'],
              ['DEF-thumb.02.L',     'thumb_02_l'], 
              ['DEF-thumb.03.L',     'thumb_03_l'],
              
              ['DEF-f_index.01.L.01', 'index_01_l'],
              ['DEF-f_index.02.L',    'index_02_l'],
              ['DEF-f_index.03.L',    'index_03_l'],
              
              ['DEF-f_middle.01.L.01', 'middle_01_l'],
              ['DEF-f_middle.02.L',    'middle_02_l'],
              ['DEF-f_middle.03.L',    'middle_03_l'],
              
              ['DEF-f_ring.01.L.01',  'ring_01_l'],
              ['DEF-f_ring.02.L',     'ring_02_l'],
              ['DEF-f_ring.03.L',     'ring_03_l'],
              
              ['DEF-f_pinky.01.L.01', 'pinky_01_l'],
              ['DEF-f_pinky.02.L',    'pinky_02_l'],
              ['DEF-f_pinky.03.L',    'pinky_03_l'],
              
              ['DEF-thigh.01.L', 'thigh_l'],
              ['DEF-thigh.02.L', 'thigh_twist_01_l'],
              ['DEF-shin.01.L',  'calf_l'],
              ['DEF-shin.02.L',  'calf_twist_01_l'],
              ['DEF-foot.L',     'foot_l'],
              ['DEF-toe.L',      'ball_l']]

    #adding flipped bones
    ref = boneNames[:]
    for bn in ref:
        if bn[0].endswith(('.L', '.L.01', '.L.02')):
            if bn[0].endswith('.L'):
                flipped = bn[0].rsplit('.L', 1)[0] + '.R'
            elif bn[0].endswith('.L.01'):
                flipped = bn[0].rsplit('L.01', 1)[0] + 'R.01'
            else:
                flipped = bn[0].rsplit('L.02', 1)[0] + 'R.02'
                                    
            #where rigify has left bone, mannequin too.
            mqFlipped = bn[1].rsplit('_l', 1)[0] + '_r'
            
            boneNames.append([flipped, mqFlipped])
    
    return boneNames

#-------------------------------
def getPitchiPoyBoneNames():
    # [PitchiPoy, Mannequin]
    boneNames = [
              ['DEF-spine',     'pelvis'],
              ['DEF-spine.001', 'spine_01'],
              ['DEF-spine.002', 'spine_02'],
              ['DEF-spine.003', 'spine_03'],
              ['DEF-spine.004', 'neck_01'],
              ['DEF-spine.006', 'head'],
                            
              ['DEF-shoulder.L', 'clavicle_l'],
              
              ['DEF-upper_arm.L',     'upperarm_l'],
              ['DEF-upper_arm.L.001', 'upperarm_twist_01_l'],
              ['DEF-forearm.L',       'lowerarm_l'],
              ['DEF-forearm.L.001',   'lowerarm_twist_01_l'],
              ['DEF-hand.L',          'hand_l'],
              
              ['DEF-thumb.01.L', 'thumb_01_l'],
              ['DEF-thumb.02.L', 'thumb_02_l'], 
              ['DEF-thumb.03.L', 'thumb_03_l'],
              
              ['DEF-f_index.01.L',  'index_01_l'],
              ['DEF-f_index.02.L',  'index_02_l'],
              ['DEF-f_index.03.L',  'index_03_l'],
              
              ['DEF-f_middle.01.L', 'middle_01_l'],
              ['DEF-f_middle.02.L', 'middle_02_l'],
              ['DEF-f_middle.03.L', 'middle_03_l'],
              
              ['DEF-f_ring.01.L',   'ring_01_l'],
              ['DEF-f_ring.02.L',   'ring_02_l'],
              ['DEF-f_ring.03.L',   'ring_03_l'],
              
              ['DEF-f_pinky.01.L',  'pinky_01_l'],
              ['DEF-f_pinky.02.L',  'pinky_02_l'],
              ['DEF-f_pinky.03.L',  'pinky_03_l'],
              
              ['DEF-thigh.L',     'thigh_l'],
              ['DEF-thigh.L.001', 'thigh_twist_01_l'],
              ['DEF-shin.L',      'calf_l'],
              ['DEF-shin.L.001',  'calf_twist_01_l'],
              ['DEF-foot.L',      'foot_l'],
              ['DEF-toe.L',       'ball_l']]

    #adding flipped bones
    ref = boneNames[:]
    for bn in ref:
        if bn[0].endswith('.L') or bn[0].endswith('.L.00', 0, -1): #there's L.001 to L.004
            if bn[0].endswith('.L'):
                flipped = bn[0].rsplit('.L', 1)[0] + '.R'
            else:
                temp = bn[0].rsplit('.L.00', 1)
                flipped = temp[0] + '.R.00' + temp[1]
            
            #where rigify has left bone, mannequin too.
            mqFlipped = bn[1].rsplit('_l', 1)[0] + '_r'
            
            boneNames.append([flipped, mqFlipped])
    
    return boneNames


#------------------------------------

def validate():
    global isBackward
    
    if len(bpy.context.selected_objects) == 0:
        print("Warning: Nothing selected")
        return False
    
    selectObjs = bpy.context.selected_objects
    armatureCount = 0
    meshCount = 0
    rigifyObj = None
    for obj in selectObjs:
        if obj.type == 'ARMATURE':
            rigifyObj = obj
            armatureCount += 1
        elif obj.type == 'MESH':
            meshCount += 1
    
    if meshCount == 0 and armatureCount == 0:
        print("Warning: no mesh and armature is selected")
        return False    
    elif armatureCount >= 2:
        print("Warning: Multiple armatures are selected")
        return False
    
    bpy.ops.object.mode_set(mode = 'OBJECT')

    mannequinCheck = ['pelvis', 'spine_01', 'spine_02', 'neck_01', 'head'] #spine_03 is skipped when converted from standard rigify
    
    #---------- detect from mesh whether forward (unrigify to mannequin) or backward --------   
    ################################
    # If you want to convert partial mesh, skip these check.
    # isBackward = True/False # Don't forget to set this value when you skip this section.
    if armatureCount == 0: #no armature means there's selected mesh
        checkNames = mannequinCheck[:]
        for obj in selectObjs:
            if obj.type == 'MESH':
                for vg in obj.vertex_groups:
                    if vg.name in checkNames:
                        checkNames.remove(vg.name)
                    
        if len(checkNames) == 0:
            isBackward = True
        elif len(checkNames) == 5:
            isBackward = False
        else:
            print("Warning: Detected vertex groups were not expected. Nothing was done.")
            return False
    # skip to here.
    #################################
    
    #----------- detect whether forward or not from armature ---------- 
    if armatureCount == 1:
        checkNames = mannequinCheck[:]
        for b in rigifyObj.data.bones:
            if b.name in checkNames:
                checkNames.remove(b.name)
        if len(checkNames) == 0:
            isBackward = True
        elif len(checkNames) == 5:
            isBackward = False
        else:
            print("Warning: Detected bone were not expected. Nothing was done.")
            return False
        
        #-------- check if isPitchiPoy value is correct -------------
        #Standard rigify unrigified: 78 bones, PitchiPoy rigify unrigified: 161 bones
        if not isBackward:
            if len(rigifyObj.data.bones) > 400:
                print("Warning: This script is not intended to be used on original Rigify.")
                print("         Please run on'Unrigified' object. or select mesh objects but armature and run again.")
                return False
            
            boneNames = getPitchiPoyBoneNames() if isPitchiPoy else getBoneNames()
            matched = 0
            for b in rigifyObj.pose.bones:
                for bn in boneNames:
                    if b.name == bn[0]:
                        matched +=  1
                        break
            
            if len(boneNames) != matched :
                print("Warning: Bones of unrigify armature did not match. Nothing was done.")
                return False
                        
    return True

################################################
################################################
if validate():
    main()
