###############################################
###############################################
#-------Customizable Bone List --------------------
# None will be Separator in the menu
# first bone in the list will be set to active.
# first string becomes a key. therefore it must be unique.
# label can be arbitrary string. but it should be unique after replaced non alphanumeric with '_'. e.g. 'Fingers()' and 'Fingers$$' both become 'Fingers__' (both not unique!).  
# Sub menu can't be nested.

bones = [] 
bones.append(['Arm.R (FK)', ['upper_arm.fk.R', 'forearm.fk.R', 'hand.fk.R']]) 
bones.append(['Arm.L (FK)', ['upper_arm.fk.L', 'forearm.fk.L', 'hand.fk.L']]) 
bones.append(['Hand.R (IK)', ['hand.ik.R']]) 
bones.append(['Hand.L (IK)', ['hand.ik.L']])

bones.append(None)
subBones = []
subBones.append(['AllFingers.R', ['thumb.R', 'f_index.R', 'f_middle.R', 'f_ring.R', 'f_pinky.R']]) 
subBones.append(None)
subBones.append(['Thumb.R', ['thumb.R']]) 
subBones.append(['Index.R', ['f_index.R']]) 
subBones.append(['Middle.R', ['f_middle.R']]) 
subBones.append(['Ring.R', ['f_ring.R']]) 
subBones.append(['Pinky.R', ['f_pinky.R']]) 
bones.append(['Fingers.R', subBones])#don't foget this

subBones = [] #should be reset before start another
subBones.append(['AllFingers.L', ['thumb.L', 'f_index.L', 'f_middle.L', 'f_ring.L', 'f_pinky.L']]) 
subBones.append(None)
subBones.append(['Thumb.L', ['thumb.L']]) 
subBones.append(['Index.L', ['f_index.L']]) 
subBones.append(['Middle.L', ['f_middle.L']]) 
subBones.append(['Ring.L', ['f_ring.L']]) 
subBones.append(['Pinky.L', ['f_pinky.L']]) 
bones.append(['Fingers.L', subBones])
    
bones.append(None)
bones.append(['Head', ['head']]) 
bones.append(['Chest', ['chest']]) 
bones.append(['Torso', ['torso']])

bones.append(None)
bones.append(['Foot.R (IK)', ['foot.ik.R']]) 
bones.append(['Foot.L (IK)', ['foot.ik.L']]) 
bones.append(['FootRoll.R', ['foot_roll.ik.R']])
bones.append(['FootRoll.L', ['foot_roll.ik.L']])

bones.append(None)
bones.append(['Shoulder.R',['shoulder.R']])
bones.append(['Shoulder.L',['shoulder.L']])

bones.append(None)
subBones = []
subBones.append(['ArmTweaks.R', ['upper_arm_hose.R', 'elbow_hose.R', 'forearm_hose.R']])
subBones.append(['ArmTweaks.L', ['upper_arm_hose.L', 'elbow_hose.L', 'forearm_hose.L']])
subBones.append(['LegTweaks.R', ['thigh_hose.R', 'knee_hose.R', 'shin_hose.R']])
subBones.append(['LegTweaks.L', ['thigh_hose.L', 'knee_hose.L', 'shin_hose.L']])
subBones.append(None)
subBones.append(['Spine', ['spine']])
subBones.append(['Hips', ['hips']])
bones.append(['Others', subBones])

bones.append(None)
bones.append(['Root', ['root']]) 
#---------- end of customizable list ---------------
###############################################
###############################################


###############################################
# Default is Alt+Q. if you want to change key map, see very latter part of this code.
#
# This addon can be used any rig. Not limited to Rigify
# Though, i hope this functionality will be included into Rigify. I won't claim any rights.
#
# Operator has no hierarchy. all bone label in same level.
# then create subMenus class dynamically with according .boneKey enum prop
# Dynamic class creation is need to not limit the number of sub menus and where to place on root menu.
#----------------------
# my memo
# D.armatures['xxx'].edit_bones[0] is EditBone class
# D.objects['x'].pose.bones['x'].bone's class structure is .Pose.PoseBone.Bone
###############################################

import bpy, re

bl_info = {
    "name": "Easy Select Bones",
    "author": "Chichige-Bobo",
    "version": (1, 0),
    "blender": (2, 69),
    "location": "PoseMode > Alt+Q",
    "description": "Select Bones from Menu",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Rigging"}

# list is used for bones[]. because dict cannot be sorted.
# then create label and bone-name-list pair as dict to be used in execute(). 
# Submenu top label is omitted at conversion. 
bonesDict = {} 
for b in bones:
    if b:
        if len(b[1]) >= 2 and type(b[1][0]) is not str: #detect subBones
            for sb in b[1]:
                if sb:
                    bonesDict[sb[0]] = tuple(sb[1]) 
        else:
            bonesDict[b[0]] = b[1]
    

#################################################
class EasySelectBonesOp(bpy.types.Operator):
    bl_label = "EasySelectBones"
    bl_idname = "pose.easy_select_bones_op"
    bl_options = {'REGISTER', 'UNDO'}
    
    restrictVisibility = bpy.props.BoolProperty(name = 'Restrict Visibility',
                                                description = 'Only shows layers where selected bones reside',
                                                default = False)
    
    #--------
    def getBoneDictKeys(self, context):
        global bonesDict
        dictKeys = []
        for ky in bonesDict:
            if ky:
                #id is shown as menu item, name and desc is shown in combobox in toolbar
                #identifier, name, description 
                dictKeys.append((ky, ky, ('Select ' + ky + ' Bones') ))  
        return dictKeys
    
    boneKey = bpy.props.EnumProperty(
                    items = getBoneDictKeys, 
                    name="Bone Dict Key",
                    description="",
               )
    #--------
    
    
    @classmethod
    def poll(cls, context):
        return context.mode == 'POSE'

    def execute(self, context):        
        global bones
        
        poseBones = context.active_object.pose.bones
        armature = context.active_object.data

        isBoneMissing = False
        isFirstBone = True
        allExistLayers = []
        
        for pb in poseBones:
            pb.bone.select = False
        
        for bname in bonesDict[self.boneKey]:
            
            if bname in poseBones: 
                poseBones[bname].bone.select = True
                
                if isFirstBone:
                    armature.bones.active = armature.bones[bname]
                    isFirstBone = False
                
                #layers visibility
                existLayers = [i for i in range(32) if armature.bones[bname].layers[i]]
                if self.restrictVisibility:
                    allExistLayers += existLayers
                else:
                    for i in existLayers:
                        armature.layers[i] = True
            
            else:
                print(bname + ' is not found')
                isBoneMissing = True
        
        if self.restrictVisibility :
            armature.layers = [i in allExistLayers for i in range(32)]
            
        if isBoneMissing: 
            self.report({'WARNING'}, 'Some bones are missing. See the console')
        
        return {'FINISHED'}
      
# Menus ##############################################
# this class never registered but dynamically created sub classes will be
# sub classes will created at register(). 
class EasySelectBonesSubMenu_Base(bpy.types.Menu):
    bl_label = "Easy Select Bones Sub Menu"
    bl_idname = "pose.easy_select_bones_sub_menu_base"
       
    menuItems = []
    
    def draw(self, context):
        layout = self.layout
        
        for itm in self.menuItems:
            if itm:
                layout.operator('pose.easy_select_bones_op', itm).boneKey = itm
            else:
                layout.separator()

# this class will be reged.
class EasySelectBonesMenu(bpy.types.Menu):    
    bl_label = "Easy Select Bones"
    bl_idname = "pose.easy_select_bones_menu"
 
    def draw(self, context):
        layout = self.layout
        
        global bones
        for b in bones:
            if b:
                if len(b[1]) >= 2 and type(b[1][0]) is not str: #detect subBones
                    #these sub classes will be created at register()
                    global subMenuClassesDict
                    layout.menu(subMenuClassesDict[b[0]].bl_idname, b[0])
                else:
                    layout.operator('pose.easy_select_bones_op', b[0]).boneKey = b[0]
            else:
                layout.separator()
        
 
################################################

subMenuClassesDict = {}
myKeymaps = []

def register():   
    bpy.utils.register_class(EasySelectBonesOp)
    
    # create sub class of subMenu dynamically
    global bones
    for b in bones:
        if b and len(b[1]) >= 2 and type(b[1][0]) is not str: #subBones
            items = []
            for sb in b[1]:
                if sb:
                    items.append(sb[0])
                else:
                    items.append(None)
                    
            clsName = re.sub('[\W]', '_', b[0])
            idName = 'pose.easy_select_bones_sub_menu_' + re.sub('[\W]', '_', b[0]).lower()
            cls = type('EasySelectBonesSumMenu_' + clsName,
                        (EasySelectBonesSubMenu_Base,),
                        dict(   bl_label = b[0],
                                bl_idname = idName,
                                menuItems = items )
                      )

            global subMenuClassesDict
            subMenuClassesDict[b[0]] = cls
            bpy.utils.register_class(cls)
            
    bpy.utils.register_class(EasySelectBonesMenu)

    #---
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Pose', space_type='EMPTY') #'Pose Mode' not worked
    ##################################################################
    ##################################################################
    # hrer is key map.
    kmi = km.keymap_items.new('wm.call_menu', 'Q', 'PRESS', alt=True)
    ##################################################################
    ##################################################################
    kmi.properties.name = 'pose.easy_select_bones_menu' 
    global myKeymaps
    myKeymaps.append(km)


def unregister():
    
    bpy.utils.unregister_class(EasySelectBonesOp)
    for cls in subMenuClassesDict:
        bpy.utils.unregister_class(cls) 
    bpy.utils.unregister_class(EasySelectBonesMenu)
            
    global myKeymaps
    wm = bpy.context.window_manager
    for km in myKeymaps:
        wm.keyconfigs.addon.keymaps.remove(km)
    del myKeymaps[:]    

if __name__ == "__main__":
    register()
