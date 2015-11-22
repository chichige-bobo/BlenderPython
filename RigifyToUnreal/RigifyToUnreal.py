#########################################################################
# Script is published under GPL
# feel free to modify and republish.
# I'm just start to learn UE4. I hope this concept is not much off base.
#
# (Mannequin model is probably not GPL though. It's not mine.)
# (Sintel model is Creative Commons Attribution 3.0
#  You can download at BlendSwap.com. Google with 'Sintel Lite BlendSwap')
#########################################################################
# RigifyToUnreal : ver 1.61
# Environment : Blender 2.75a, UnrealEditor 4.9.1
# Author : ChichigeBobo
#########################################################################
# What this script does -------
#   *Determine whether the rig is standard rigify or PitchiPoy by counting bones.
#   *Copy rigify rig then strip all bones except deform bones.
#   *Add constraints to overlap the rigify's bones.
#   *re-construct hierarchy for PhysicsAsset in UE4
#   *Add an empty as most parent to avoid 'too small bone' warning at importing
#   *Bake animation to new rig. Then name the Action with prefix 'Unrigify_'. 
#    (Frame range calculation is NLA aware.)
#    (If NLA is used but Action, baked Action name uses NLA's 1st track name.)
#    (If same name Action exists, old action gets suffix '.00x')
#   *Rewire mesh objects' Armature modifier to the new rig 
#    (Only when mesh objects are selected)
#    (If you have multiple mesh objects, this .blend file has another script for you.)
#   *Check selection to ready to export. 
#
# How To Use ------------------
#   *Prepare animation and rigify. 
#    (This script doesn't need to adjust size like tutorials that uses old version of blender. If a model is 1.8m, use as it is.)
#   *Select a rigify object and mesh objects 
#    (loose selection is ok. It means that selection can include lamps. But armature should not be multiple.)
#    (Only a rigify object (without mesh objects) is ok.)
#   *Run this script.
#   *export as FBX
#
# It's so easy. Thus you don't need to preserve the generated rig.
# If you want to export new animation later, create new one!
# Tiny empty is generated everytime. No problem to delete it with the rig.
##########################################################################
# Trouble shooting
#    Q.Mesh object has weird distortion.
#    A.You had accidentally set an Action (which baked by this script) to Rigify object.
#      That causes non-constraint deform bones to get unexpected transformation.
#      But you can't use Alt+G,R,S in Pose mode because they are locked.
#      Use another script named 'RIGIFY_ResetDeformBones.py' in this blend file.
#      (Or, do Alt+G,R,S to generated rig and copy all. Then paste it to the rigify.) 
#
#    Q.Imported fbx to Unreal. But bones are bending unexpectedly.
#    A.Probably same as above. The animation had been baked by 'affected' rigify.
#      Correct the rigify first, then bake again.
#
#    Q.Generated rig can't be moved.
#    A.If the rigify has no animation, all bones of new rig have constraints.
#      It's expecting you to bake animation manually. (Bake command has 'clear constraints' option) 
#
#    Q.Unreal doesn't recognize exported rig as same skeleton.
#    A.If exported rig's name is not same as earlier one's, it'll be treated as
#      different skeleton. This script asigns same rig name twice to avoid '.001'.
#      So, be careful when you try to export regs generated earlier.
#
#    Q.There's two animations when imported to Unreal.
#    A.If action is purged before export (as shown in the youtube video),
#      probably a mesh object has action. In this case, it's not relevant to this script.
#    
#    Q.Shape key is not imported as morph in Unreal.
#    A.At Unreal version 4.9.1, it seems requiring additional procedure
#      that right-clicking on Mesh then choose 'Reimport'.  
#########################################################################

#==========  CUSTOMIZATION  ===========================================
#Change to your favorite name.
newRigName = 'Unrigify'
newActionNamePrefix = 'Unrigify_'
newActionNameSuffix = ''

#use below if you have bones added.
nonDeleteBones = [] #These bones not deleted. e.g. 'DEF-eye_L', 'DEF-eye_R'
nonConstBones = [] #These bones' constraints get no change. In many cases, same as above.

#If you are not PitchiPoy version user, probably this option is not relevant. 
#These bones will be checked 'deform' state.
#If it is marked, treat as deform bone. If not, do nothing.
#i.e. you should turn 'deform' on to make this effective.
#(Why don't check all deform state? Because reconstruction process requires to know the parent.)
respectDeformStateBones = [ # bone name, parent bone, connected (this is mainly for Constrant of PhysicsAsset)
          ['MCH-eye.L', 'DEF-spine.006', False],
          ['MCH-eye.R', 'DEF-spine.006', False],
          ['teeth.T',   'DEF-spine.006', False],
          ['teeth.B',   'DEF-spine.006', False],
          
          ['DEF-hair.F.L',     'DEF-spine.006', False], #my custom bones.
          ['DEF-hair.F.L.001', 'DEF-hair.F.L',  True],  #It's ok to delete or not delete.
          ['DEF-hair.M.L',     'DEF-spine.006', False],
          ['DEF-hair.M.L.001', 'DEF-hair.M.L',  True],
          ['DEF-hair.B.L',     'DEF-spine.006', False],
          ['DEF-hair.B.L.001', 'DEF-hair.B.L',  True],
          ['DEF-hair.F.R',     'DEF-spine.006', False],
          ['DEF-hair.F.R.001', 'DEF-hair.F.R',  True],
          ['DEF-hair.M.R',     'DEF-spine.006', False],
          ['DEF-hair.M.R.001', 'DEF-hair.M.R',  True],
          ['DEF-hair.B.R',     'DEF-spine.006', False],
          ['DEF-hair.B.R.001', 'DEF-hair.B.R',  True]
 ]

#Baking frame range.
#If False, the range is calculated from Action and NLA.
#If True, use scene's StartFrame and EndFrame.
#If you don't wanna bake, just delete the Action after bake.
isBakeSceneFrameRange = False


# an option converting to mannequin name is separated at v1.6.
# use UNRIGIFY_ConverToMannequinOrBackToUnrigify
#======================================================================
import bpy, math

def main():
    
    initialSelection = bpy.context.selected_objects        
    for obj in initialSelection:
        if obj.type == 'ARMATURE':
            bpy.context.scene.objects.active = obj
            rigifyObj = obj
        else:
            obj.select = False

    isPitchiPoy = len(rigifyObj.data.bones) > 620 
    boneNames = getPitchiPoyBoneNames() if isPitchiPoy else getBoneNames()
    
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False}) #'invalid context' in console. I don't know how to fix

    newRigObj = bpy.context.object
    amt = newRigObj.data
    
    newRigObj.name = newRigName
    newRigObj.name = newRigName #prevent '.001'
    newRigObj.animation_data.action = None
    newRigObj.pose.bones['root'].custom_shape = None
    #amt.layers = [i in [28, 29] for i in range(32)]
    amt.layers =  [True for i in range(32)] # all
    
    #------- merge effective 'respectDeformStateBones' items to main bone names -------
    temp = []
    for b in rigifyObj.data.bones:
        for rdb in respectDeformStateBones:
            if b.name == rdb[0] and b.use_deform:
                rdb.append(rdb[0]) #bone name for mannequin
                temp.append(rdb)
                break
    boneNames.extend(temp)
        
    #------- delete bones but deforms ---------
    bpy.ops.object.mode_set(mode = 'EDIT')
    deleteBones = []
    for eb in amt.edit_bones:
        isFound = False
        for bn in boneNames:
            if eb.name == bn[0]:
                isFound = True
                break
        if not isFound:
            #print(eb.name)
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
                isFound = True
                b.parent = amt.edit_bones[bn[1]]
                b.use_connect = bn[2]
                b.use_inherit_rotation = False  #works fine w/o these. 
                b.use_inherit_scale = False     #otherwise, I don't know why work w/o these.
                if not bn[2]:
                    b.use_local_location = False
                break
        
    #------ set constraints (and unlock)---------- 
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    for b in newRigObj.pose.bones: 
        if b.name in nonConstBones:
            continue
        
        for c in b.constraints:
            b.constraints.remove(c)

        cnst = b.constraints.new('COPY_LOCATION')
        cnst.name = 'Copy Location'
        cnst.target = rigifyObj
        cnst.subtarget = b.name    
        
        cnst = b.constraints.new('COPY_ROTATION')
        cnst.name = 'Copy Rotation'
        cnst.target = rigifyObj
        cnst.subtarget = b.name    

        cnst = b.constraints.new('COPY_SCALE')
        cnst.name = 'Copy Scale'
        cnst.target = rigifyObj
        cnst.subtarget = b.name
        cnst.target_space = 'WORLD' #seems better than 'POSE'
        cnst.owner_space = 'POSE'
        
        #-- COPY_TRANSFORMS didn't work. Seems that loc and rot need World coord.
        
        b.lock_location = [False, False, False]
        b.lock_rotation = [False, False, False]
        b.lock_rotation_w = False
        b.lock_rotations_4d = False
        b.lock_scale = [False, False, False]
    
    #-------- size manipulation --------             
    empty = bpy.data.objects.new('Empty', None)
    empty.location = newRigObj.location
    bpy.context.scene.objects.link(empty)
    newRigObj.scale = (100, 100, 100)
    newRigObj.parent = empty
    empty.scale = (0.01, 0.01, 0.01)
    newRigObj.select = True
    
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    #--------- baking ---------------
    frameRange = getFrameRange(rigifyObj) #return None if animation doesn't exist. 
    if frameRange and isBakeSceneFrameRange:
        frameRange = [bpy.context.scene.frame_start, bpy.context.scene.frame_end]
    
    if frameRange:
        bpy.ops.nla.bake(frame_start=frameRange[0], frame_end=frameRange[1], step=1, only_selected=False, visual_keying=True, clear_constraints=True, bake_types={'POSE'})
        #bpy.ops.action.clean() #invalid context error.
        rigifyAction = rigifyObj.animation_data.action
        newAction = newRigObj.animation_data.action
        if rigifyAction:
            newAction.name = newActionNamePrefix + rigifyAction.name + newActionNameSuffix
            newAction.name = newActionNamePrefix + rigifyAction.name + newActionNameSuffix #prevent .001
        else:
            trackName = rigifyObj.animation_data.nla_tracks[0].name
            newAction.name = newActionNamePrefix + trackName + newActionNameSuffix
            newAction.name = newActionNamePrefix + trackName + newActionNameSuffix #prevent .001
        
        tracks = newRigObj.animation_data.nla_tracks
        if tracks:
            tracksCopy = tracks[:]
            for tc in tracksCopy:
                newRigObj.animation_data.nla_tracks.remove(tc)       
         
    #----- point armature modifier to new rig ----
    for obj in initialSelection:
        if obj.type == 'ARMATURE':
            obj.select = False
        elif obj.type == 'MESH':
            for m in obj.modifiers:
                if m.type == 'ARMATURE' and m.object == rigifyObj:
                    m.object = newRigObj
            obj.select = True
        else:
            obj.select = False     
    
    bpy.context.scene.objects.active = newRigObj

    print('RigifyToUnreal : Done!')
    
#=======================================================

def getBoneNames():
    # [subject, parent, connected]
    boneNames = [['root', None, False],
              ['DEF-hips',       'root',      False],
              ['DEF-spine',      'DEF-hips',  True],
              ['DEF-chest',      'DEF-spine', True],
              
              ['DEF-neck',       'DEF-chest', False],
              ['DEF-head',       'DEF-neck',  True],
              
              ['DEF-shoulder.L', 'DEF-chest', False],
              
              ['DEF-upper_arm.01.L', 'DEF-shoulder.L',     False],
              ['DEF-upper_arm.02.L', 'DEF-upper_arm.01.L', True],
              ['DEF-forearm.01.L',   'DEF-upper_arm.02.L', True],
              ['DEF-forearm.02.L',   'DEF-forearm.01.L',   True],
              ['DEF-hand.L',         'DEF-forearm.02.L',   True],
              
              ['DEF-thumb.01.L.01',  'DEF-hand.L',        False],
              ['DEF-thumb.01.L.02',  'DEF-thumb.01.L.01', True], 
              ['DEF-thumb.02.L',     'DEF-thumb.01.L.02', True], 
              ['DEF-thumb.03.L',     'DEF-thumb.02.L',    True],
              
              ['DEF-palm.01.L',       'DEF-hand.L',          False], 
              ['DEF-f_index.01.L.01', 'DEF-palm.01.L',       True],
              ['DEF-f_index.01.L.02', 'DEF-f_index.01.L.01', True],
              ['DEF-f_index.02.L',    'DEF-f_index.01.L.02', True],
              ['DEF-f_index.03.L',    'DEF-f_index.02.L',    True],
              
              ['DEF-palm.02.L',        'DEF-hand.L',           False],
              ['DEF-f_middle.01.L.01', 'DEF-palm.02.L',        True],
              ['DEF-f_middle.01.L.02', 'DEF-f_middle.01.L.01', True],
              ['DEF-f_middle.02.L',    'DEF-f_middle.01.L.02', True],
              ['DEF-f_middle.03.L',    'DEF-f_middle.02.L',    True],
              
              ['DEF-palm.03.L',       'DEF-hand.L',         False],
              ['DEF-f_ring.01.L.01',  'DEF-palm.03.L',      True],
              ['DEF-f_ring.01.L.02',  'DEF-f_ring.01.L.01', True],
              ['DEF-f_ring.02.L',     'DEF-f_ring.01.L.02', True],
              ['DEF-f_ring.03.L',     'DEF-f_ring.02.L',    True],
              
              ['DEF-palm.04.L',       'DEF-hand.L',          False],
              ['DEF-f_pinky.01.L.01', 'DEF-palm.04.L',       True],
              ['DEF-f_pinky.01.L.02', 'DEF-f_pinky.01.L.01', True],
              ['DEF-f_pinky.02.L',    'DEF-f_pinky.01.L.02', True],
              ['DEF-f_pinky.03.L',    'DEF-f_pinky.02.L',    True],
              
              ['DEF-thigh.01.L', 'DEF-hips',       False],
              ['DEF-thigh.02.L', 'DEF-thigh.01.L', True],
              ['DEF-shin.01.L',  'DEF-thigh.02.L', True],
              ['DEF-shin.02.L',  'DEF-shin.01.L',  True],
              ['DEF-foot.L',     'DEF-shin.02.L',  True],
              ['DEF-toe.L',      'DEF-foot.L',     True]]

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
                        
            boneNames.append([flipped, flippedPnt, bn[2]])
    
    return boneNames

#-------------------------------
def getPitchiPoyBoneNames():
    # [subject, parent, connected, mannequin]
    boneNames = [['root', None, False],
              ['DEF-spine',     'root',          False],
              ['DEF-spine.001', 'DEF-spine',     True],
              ['DEF-spine.002', 'DEF-spine.001', True],
              ['DEF-spine.003', 'DEF-spine.002', True],
              ['DEF-spine.004', 'DEF-spine.003', True],
              ['DEF-spine.005', 'DEF-spine.004', True],
              ['DEF-spine.006', 'DEF-spine.005', True],
                            
              ['DEF-pelvis.L',   'DEF-spine',     False],

              ['DEF-breast.L',   'DEF-spine.003', False],

              ['DEF-shoulder.L', 'DEF-spine.003', False],
              
              ['DEF-upper_arm.L',     'DEF-shoulder.L',      False],
              ['DEF-upper_arm.L.001', 'DEF-upper_arm.L',     True],
              ['DEF-forearm.L',       'DEF-upper_arm.L.001', True],
              ['DEF-forearm.L.001',   'DEF-forearm.L',       True],
              ['DEF-hand.L',          'DEF-forearm.L.001',   True],
              
              ['DEF-palm.01.L',  'DEF-hand.L',     False],
              ['DEF-palm.02.L',  'DEF-hand.L',     False], 
              ['DEF-palm.03.L',  'DEF-hand.L',     False],
              ['DEF-palm.04.L',  'DEF-hand.L',     False], 
              
              ['DEF-thumb.01.L', 'DEF-palm.01.L',  False],
              ['DEF-thumb.02.L', 'DEF-thumb.01.L', True], 
              ['DEF-thumb.03.L', 'DEF-thumb.02.L', True],
              
              ['DEF-f_index.01.L',  'DEF-palm.01.L',     False],
              ['DEF-f_index.02.L',  'DEF-f_index.01.L',  True],
              ['DEF-f_index.03.L',  'DEF-f_index.02.L',  True],
              
              ['DEF-f_middle.01.L', 'DEF-palm.02.L',     False],
              ['DEF-f_middle.02.L', 'DEF-f_middle.01.L', True],
              ['DEF-f_middle.03.L', 'DEF-f_middle.02.L', True],
              
              ['DEF-f_ring.01.L',   'DEF-palm.03.L',     False],
              ['DEF-f_ring.02.L',   'DEF-f_ring.01.L',   True],
              ['DEF-f_ring.03.L',   'DEF-f_ring.02.L',   True],
              
              ['DEF-f_pinky.01.L',  'DEF-palm.04.L',     False],
              ['DEF-f_pinky.02.L',  'DEF-f_pinky.01.L',  True],
              ['DEF-f_pinky.03.L',  'DEF-f_pinky.02.L',  True],
              
              ['DEF-thigh.L',     'DEF-spine',       False],
              ['DEF-thigh.L.001', 'DEF-thigh.L',     True],
              ['DEF-shin.L',      'DEF-thigh.L.001', True],
              ['DEF-shin.L.001',  'DEF-shin.L',      True],
              ['DEF-foot.L',      'DEF-shin.L.001',  True],
              ['DEF-toe.L',       'DEF-foot.L',      True],
              
              #----- face ----
              ['DEF-forehead.L',     'DEF-spine.006', False],
              ['DEF-forehead.L.001', 'DEF-spine.006', False],
              ['DEF-forehead.L.002', 'DEF-spine.006', False],
              
              ['DEF-brow.T.L',     'DEF-spine.006', False],
              ['DEF-brow.T.L.001', 'DEF-spine.006', False],
              ['DEF-brow.T.L.002', 'DEF-spine.006', False],
              ['DEF-brow.T.L.003', 'DEF-spine.006', False],

              ['DEF-brow.B.L',     'DEF-spine.006', False], #brow.B and lid are (indirectly) parented to master_eye.L
              ['DEF-brow.B.L.001', 'DEF-spine.006', False], 
              ['DEF-brow.B.L.002', 'DEF-spine.006', False],
              ['DEF-brow.B.L.003', 'DEF-spine.006', False],

              ['DEF-lid.T.L',     'DEF-spine.006', False],
              ['DEF-lid.T.L.001', 'DEF-spine.006', False],
              ['DEF-lid.T.L.002', 'DEF-spine.006', False],
              ['DEF-lid.T.L.003', 'DEF-spine.006', False],
              
              ['DEF-lid.B.L',     'DEF-spine.006', False],
              ['DEF-lid.B.L.001', 'DEF-spine.006', False],
              ['DEF-lid.B.L.002', 'DEF-spine.006', False],
              ['DEF-lid.B.L.003', 'DEF-spine.006', False],
              
              ['DEF-nose',     'DEF-spine.006', False],
              ['DEF-nose.001', 'DEF-spine.006', False],
              ['DEF-nose.002', 'DEF-spine.006', False],
              ['DEF-nose.003', 'DEF-spine.006', False],
              ['DEF-nose.004', 'DEF-spine.006', False],

              ['DEF-nose.L',     'DEF-spine.006', False],
              ['DEF-nose.L.001', 'DEF-spine.006', False],

              ['DEF-cheek.T.L',     'DEF-spine.006', False],
              ['DEF-cheek.T.L.001', 'DEF-spine.006', False],
              ['DEF-cheek.B.L',     'DEF-spine.006', False],
              ['DEF-cheek.B.L.001', 'DEF-spine.006', False],
              
              ['DEF-lip.T.L',     'DEF-spine.006', False],
              ['DEF-lip.T.L.001', 'DEF-spine.006', False],
              ['DEF-lip.B.L',     'DEF-spine.006', False],
              ['DEF-lip.B.L.001', 'DEF-spine.006', False],

              ['DEF-tongue',     'DEF-spine.006', False],
              ['DEF-tongue.001', 'DEF-spine.006', False],
              ['DEF-tongue.002', 'DEF-spine.006', False],
              
              ['DEF-chin',      'DEF-spine.006', False],
              ['DEF-chin.001',  'DEF-spine.006', False],

              ['DEF-chin.L',    'DEF-spine.006', False],
              
              ['DEF-jaw',       'DEF-spine.006', False],

              ['DEF-jaw.L',     'DEF-spine.006', False],
              ['DEF-jaw.L.001', 'DEF-spine.006', False],
              
              ['DEF-temple.L',  'DEF-spine.006', False],

              ['DEF-ear.L',     'DEF-spine.006', False],
              ['DEF-ear.L.001', 'DEF-spine.006', False],
              ['DEF-ear.L.002', 'DEF-spine.006', False],
              ['DEF-ear.L.003', 'DEF-spine.006', False],
              ['DEF-ear.L.004', 'DEF-spine.006', False]]

    #adding flipped bones
    ref = boneNames[:]
    for bn in ref:
        if bn[0].endswith('.L') or bn[0].endswith('.L.00', 0, -1): #there's L.001 to L.004
            if bn[0].endswith('.L'):
                flipped = bn[0].rsplit('.L', 1)[0] + '.R'
            else:
                temp = bn[0].rsplit('.L.00', 1)
                flipped = temp[0] + '.R.00' + temp[1]
                        
            if bn[1].endswith('.L') or bn[1].endswith('.L.00', 0, -1): 
                if bn[1].endswith('.L'):
                    flippedPnt = bn[1].rsplit('.L', 1)[0] + '.R'
                else:
                    temp = bn[1].rsplit('.L.00', 1)
                    flippedPnt = temp[0] + '.R.00' + temp[1]
            else:
                flippedPnt = bn[1]
            
            boneNames.append([flipped, flippedPnt, bn[2]])
    
    return boneNames

#-------------------------------

#If no animation found, returns None. Fcurve's mute is not checked.
def getFrameRange(obj):
    ad = obj.animation_data
    if ad:
        min = None
        max = None

        if ad.action:
            min, max = ad.action.frame_range
            
        isActionHampersBefore = (ad.action and ad.action_blend_type == 'REPLACE' and ad.action_extrapolation == 'HOLD')
        isActionHampersAfter = (ad.action and ad.action_blend_type == 'REPLACE' and ad.action_extrapolation != 'NOTHING')
        
        if ad.use_nla: #speaker icon
            
            for track in ad.nla_tracks:
                if not track.mute:
                    
                    for strip in track.strips:
                        if not min: #there's no Action
                            min = strip.frame_start
                            max = strip.frame_end
                        else:
                            if min > strip.frame_start and not isActionHampersBefore:
                                min = strip.frame_start
                            if max < strip.frame_end and not isActionHampersAfter:
                                max = strip.frame_end
        
        if min is None: #'not min' is not adequate. Because if an action starts at frame 0, it is treated as None. 
            return None
        else:
            min = math.ceil(min)
            max = math.ceil(max)
            return [min, max]
    
    else:
        return None

#------------------------------------

def validate():
    if len(bpy.context.selected_objects) == 0:
        print("Warning: Nothing selected")
        return False
    
    selectObjs = bpy.context.selected_objects
    armatureCount = 0
    rigifyObj = None
    for obj in selectObjs:
        if obj.type == 'ARMATURE':
            rigifyObj = obj
            armatureCount += 1
    
    if armatureCount == 0:
        print("Warning: No armature is selected.")
        return False
    elif armatureCount >= 2:
        print("Warning: Multiple armatures are selected")
        return False
    
    #-----check rigify version----------
    #Standard rigify: 431 bones, PitchiPoy rigify: 627 bones
    if len(rigifyObj.data.bones) < 400:
        print("Too less bones. Probably the armature is not Rigify.")
        return False
        
    boneNames = getPitchiPoyBoneNames() if len(rigifyObj.data.bones) > 620 else getBoneNames()
    matched = 0
    for b in rigifyObj.pose.bones:
        for bn in boneNames:
            if b.name == bn[0]:
                matched +=  1
                break
        
    if len(boneNames) != matched :
        print("Bones of rigify did not match. Change the script or use Blender ver2.75a.")
        return False
                
    return True

################################################
################################################
if validate():
    main()
