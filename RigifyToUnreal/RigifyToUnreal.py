#########################################################################
# GPL
# feel free to modify and republish.
# I'm just start to learn UE4. I hope this is not much off base.
# (Suzanne's body is Unreal's mannequine model. It's not mine.)  
#########################################################################
# RigifyToUnreal : ver 1.1
# Environment : Blender 2.75a, UnrealEditor 4.8.3
# Author : ChichigeBobo
#########################################################################
# What this script does-------
#  *Copy rigify rig then strip all bones except deform bones.
#  *Add constraints to overlap the rigify's bones.
#  *re-construct hierarchy for PhysicsAsset in UE4
#  *Add an empty as most parent to avoid 'too small bone' warning at importing
#
# HowToUse------------------
#  *Prepare animation and rigify. (Assumes that rigify's scale is 1.0)
#  *Select regify and run this script.
#  *3DView>Object menu>Animation>BakeAction...
#   (setting is VisualSetting and ClearConstraints are checked. And select POSE)
#  *Rewire the mesh object's Armature modifier to the generated rig
#  (parenting is optional.)
#  *Rename object name of the rig to share the skeleton in UE4
#  *Select the rig and Mesh object then export as FBX
#
# It's so easy. Thus you don't need to preserve the generated rig.
# If you want to export new animation, create new one!
# Tiny empty is generated everytime. No problem to delete it with the rig.
##########################################################################

#==========  CUSTOMIZATION  ===========================================

#change name according to Mannequine.
#some inconsistency exist. (e.g. spine_03, palm_01_l, thumb_01a_l)
isConvertToMannequine = True

#use below if you have bones added.
nonDeleteBones = [] #These bones not deleted.
nonConstBones = [] #These bones' constraints get no change

#======================================================================

import bpy 

def main():
    obj = bpy.context.object
    boneNames = getBoneNames()
    targetRigName = obj.name
    
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    #-----check regify version----------
    matched = 0
    for b in obj.pose.bones:
        for bn in boneNames:
            if b.name == bn[0]:
                matched +=  1
                break
    if len(boneNames) != matched :
        print("Version of regify did not match. Change the script or use Blender ver2.75a.")
        return
        
    bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False}) #'invalid context' in console. I don't know how to fix
    
    obj = bpy.context.object
    amt = obj.data
    
    obj.animation_data.action = None
    obj.pose.bones['root'].custom_shape = None
    amt.layers = [i in [28, 29] for i in range(32)]
    
    #------- delete obnes but deforms ---------
    bpy.ops.object.mode_set(mode = 'EDIT')
    deleteBones = []
    for eb in amt.edit_bones:
        isFound = False
        for bn in boneNames:
            if eb.name == bn[0]:
                isFound = True
                break
        if not isFound:
            print(eb.name)
            deleteBones.append(eb)
     
    for db in deleteBones:
        if db.name in nonDeleteBones:
            pass
        else:
            amt.edit_bones.remove(db)
    
    #------ set hierarchy -----------
    for b in amt.edit_bones:
        for bn in boneNames:
            if b.name == bn[0] and bn[1] != None:
                b.parent = amt.edit_bones[bn[1]]
                b.use_connect = bn[2]
                b.use_inherit_rotation = False  #works fine w/o these. 
                b.use_inherit_scale = False     #otherwise, I don't know why work w/o these.
                if not bn[2]:
                    b.use_local_location = False
                break
    
    #------ set constraints ---------- 
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    for b in obj.pose.bones: 
        if b.name in nonConstBones:
            continue
        
        for c in b.constraints:
            b.constraints.remove(c)

        cnst = b.constraints.new('COPY_LOCATION')
        cnst.name = 'Copy Location'
        cnst.target = bpy.data.objects[targetRigName]
        cnst.subtarget = b.name    
        
        cnst = b.constraints.new('COPY_ROTATION')
        cnst.name = 'Copy Rotation'
        cnst.target = bpy.data.objects[targetRigName]
        cnst.subtarget = b.name    

        cnst = b.constraints.new('COPY_SCALE')
        cnst.name = 'Copy Scale'
        cnst.target = bpy.data.objects[targetRigName]
        cnst.subtarget = b.name
        cnst.target_space = 'WORLD' #seems better than 'POSE'
        cnst.owner_space = 'POSE'
        
        #-- below didn't work. Seems that loc and rot need World coord.
        #cnst = b.constraints.new('COPY_TRANSFORMS')
        #cnst.name = 'Copy Transforms'
        #cnst.target = bpy.data.objects[targetRigName]
        #cnst.subtarget = b.name
        #cnst.target_space = 'POSE'
        #cnst.owner_space = 'POSE'
    
    #--------- change names to mannequine
    if isConvertToMannequine:
        bpy.ops.object.mode_set(mode = 'EDIT')
        for b in amt.edit_bones:
            for bn in boneNames:
                if b.name == bn[0]:
                    b.name = bn[3]
                    break
        bpy.ops.object.mode_set(mode = 'OBJECT')
                 
    empty = bpy.data.objects.new('Empty', None)
    empty.location = obj.location
    bpy.context.scene.objects.link(empty)
    obj.scale = (100, 100, 100)
    obj.parent = empty
    empty.scale = (0.01, 0.01, 0.01)
    obj.select = True
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)


#=======================================================

def getBoneNames(isManeqquine = False):
    # [subject, parent, connected]
    boneNames = [['root', None, False, 'root', None],
              ['DEF-hips',       'root',      False, 'pelvis'],
              ['DEF-spine',      'DEF-hips',  True,  'spine_01'],
              ['DEF-chest',      'DEF-spine', True,  'spine_02'],
              
              ['DEF-neck',       'DEF-chest', False, 'neck_01'], #spine_03 skipped
              ['DEF-head',       'DEF-neck',  True,  'head'],
              
              ['DEF-shoulder.L', 'DEF-chest', False, 'clavicle_l'],
              
              ['DEF-upper_arm.01.L', 'DEF-shoulder.L',     False, 'upperarm_l'],
              ['DEF-upper_arm.02.L', 'DEF-upper_arm.01.L', True,  'upperarm_twist_01_l'],
              ['DEF-forearm.01.L',   'DEF-upper_arm.02.L', True,  'lowerarm_l'],
              ['DEF-forearm.02.L',   'DEF-forearm.01.L',   True,  'lowerarm_twist_01_l'],
              ['DEF-hand.L',         'DEF-forearm.02.L',   True,  'hand_l'],
              
              ['DEF-thumb.01.L.01',  'DEF-hand.L',        False, 'thumb_01_l'],
              ['DEF-thumb.01.L.02',  'DEF-thumb.01.L.01', True,  'thumb_01a_l'], #none in mannequine
              ['DEF-thumb.02.L',     'DEF-thumb.01.L.02', True,  'thumb_02_l'], 
              ['DEF-thumb.03.L',     'DEF-thumb.02.L',    True,  'thumb_03_l'],
              
              ['DEF-palm.01.L',       'DEF-hand.L',          False, 'palm_01_l'], #none in mannequine
              ['DEF-f_index.01.L.01', 'DEF-palm.01.L',       True,  'index_01_l'],
              ['DEF-f_index.01.L.02', 'DEF-f_index.01.L.01', True,  'index_01a_l'],
              ['DEF-f_index.02.L',    'DEF-f_index.01.L.02', True,  'index_02_l'],
              ['DEF-f_index.03.L',    'DEF-f_index.02.L',    True,  'index_03_l'],
              
              ['DEF-palm.02.L',        'DEF-hand.L',           False, 'palm_02_l'],
              ['DEF-f_middle.01.L.01', 'DEF-palm.02.L',        True,  'middle_01_l'],
              ['DEF-f_middle.01.L.02', 'DEF-f_middle.01.L.01', True,  'middle_01a_l'],
              ['DEF-f_middle.02.L',    'DEF-f_middle.01.L.02', True,  'middle_02_l'],
              ['DEF-f_middle.03.L',    'DEF-f_middle.02.L',    True,  'middle_03_l'],
              
              ['DEF-palm.03.L',       'DEF-hand.L',         False, 'palm_03_l'],
              ['DEF-f_ring.01.L.01',  'DEF-palm.03.L',      True,  'ring_01_l'],
              ['DEF-f_ring.01.L.02',  'DEF-f_ring.01.L.01', True,  'ring_01a_l'],
              ['DEF-f_ring.02.L',     'DEF-f_ring.01.L.02', True,  'ring_02_l'],
              ['DEF-f_ring.03.L',     'DEF-f_ring.02.L',    True,  'ring_03_l'],
              
              ['DEF-palm.04.L',       'DEF-hand.L',          False, 'palm_04_l'],
              ['DEF-f_pinky.01.L.01', 'DEF-palm.04.L',       True,  'pinky_01_l'],
              ['DEF-f_pinky.01.L.02', 'DEF-f_pinky.01.L.01', True,  'pinky_01a_l'],
              ['DEF-f_pinky.02.L',    'DEF-f_pinky.01.L.02', True,  'pinky_02_l'],
              ['DEF-f_pinky.03.L',    'DEF-f_pinky.02.L',    True,  'pinky_03_l'],
              
              ['DEF-thigh.01.L', 'DEF-hips',       False, 'thigh_l'],
              ['DEF-thigh.02.L', 'DEF-thigh.01.L', True,  'thigh_twist_01_l'],
              ['DEF-shin.01.L',  'DEF-thigh.02.L', True,  'calf_l'],
              ['DEF-shin.02.L',  'DEF-shin.01.L',  True,  'calf_twist_01_l'],
              ['DEF-foot.L',     'DEF-shin.02.L',  True,  'foot_l'],
              ['DEF-toe.L',      'DEF-foot.L',     True,  'ball_l']]

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
                        
            if bn[1].endswith(('.L', '.L.01', '.L.02')):
                if bn[1].endswith('.L'):
                    flippedPnt = bn[1].rsplit('.L', 1)[0] + '.R'
                elif bn[1].endswith('.L.01'):
                    flippedPnt = bn[1].rsplit('L.01', 1)[0] + 'R.01'
                else:
                    flippedPnt = bn[1].rsplit('L.02', 1)[0] + 'R.02'
            else:
                flippedPnt = bn[1]
            
            #where rigify has left bone, mannequine too.
            mqFlipped = bn[3].rsplit('_l', 1)[0] + '_r'
            
            boneNames.append([flipped, flippedPnt, bn[2], mqFlipped])
    
    return boneNames

################################################
################################################
obj = bpy.context.object
if obj and obj.type == 'ARMATURE':
    main()
else:
    print("Please select rigify object.")
