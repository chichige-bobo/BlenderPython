##########################################
# Add/Remove ConstantKeyframes (Visibility, Dynamic (Rigidbody) and Animated (Rigidbody) keyframes)
# Where : RunScript Then 3DView > Toolbar
# How : If GroupName is empty, selected objects become subject.
# version : 1.1
# I'll claim no right about this code. Use or distribute at your own risk.
# #######################################

import bpy

bpy.types.Scene.constantKeyframes_groupName = bpy.props.StringProperty(name="GroupName", description="If empty, selected objects become subject", default="")

class ConstantKeyframesOperator(bpy.types.Operator):
    """Add or Delete Keyframes for 1 Bit Properties for Group/Selected Objects at Current Frame"""
    bl_idname = "object.constant_keyframes_operator"
    bl_label = "constant Keyframes Operator"

    opType = bpy.props.EnumProperty(
                              items=(('ADD_VISIBLE', 'AddVisible', 'Add Visible Keyframes'),
                                     ('ADD_INVISIBLE','AddInvisible', 'Add Invisible Keyframes'),
                                     ('DELETE_VISIBILITY', 'DeleteVisibility', 'Delete Visibility Keyframes'), 
                                     ('ADD_DYNAMIC','AddDynamic', 'Add Dynamic (Rigidbody) Keyframes'),
                                     ('ADD_UNDYNAMIC', 'AddUndynamic', 'Add Undynamic (Rigidbody) Keyframes'), 
                                     ('DELETE_DYNAMIC','DeleteDynamic', 'Delete Dynamic (Rigidbody) Keyframes'),
                                     ('ADD_ANIMATED', 'AddAnimated', 'Add Animated (Rigidbody) Keyframes'), 
                                     ('ADD_INANIMATED','AddInanimated', 'Add Inanimated (Rigidbody) Keyframes'),
                                     ('DELETE_ANIMATED', 'DeleteAnimated', 'Delete Animated Keyframes')), 
                                    name="Operation Type", 
                                    description="Add/Remove Constant Keyframes at Current Frame",
                                    default="ADD_VISIBLE")

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT'

    def execute(self, context):
        
        groupName = context.scene.constantKeyframes_groupName
        
        #--- validation ----------
        if groupName.strip() == '' and len(context.selected_objects) == 0:
            return self.abort('No object is selected')
        
        if groupName.strip() != '' and not groupName in bpy.data.groups.keys():
            return self.abort('Inputted group name was not found')
        
        if groupName.strip() != '' and len(bpy.data.groups[groupName].objects) == 0:
            return self.abort('The group has no object')
        
        #---- execution --------
        obj = bpy.context.active_object
        curFrame = context.scene.frame_current
        
        if groupName.strip() == '':
            targetObjects = context.selected_objects
        else:
            targetObjects = bpy.data.groups[groupName].objects     
        
        if self.opType.startswith('ADD_'):
            
            for obj in targetObjects:
                    
                if not obj.animation_data: #this holds Action, Driver and NLA (and other?)
                    obj.animation_data_create()
                    
                if not obj.animation_data.action:
                    obj.animation_data.action = bpy.data.actions.new(obj.name + 'Action')
                
                if self.opType == 'ADD_VISIBLE' or self.opType == 'ADD_INVISIBLE':
                    self.addKeyframe(obj, 'hide', curFrame)
                    self.addKeyframe(obj, 'hide_render', curFrame)
                elif self.opType == 'ADD_DYNAMIC' or self.opType == 'ADD_UNDYNAMIC':
                    self.addKeyframe(obj, 'rigid_body.enabled', curFrame)
                elif self.opType == 'ADD_ANIMATED' or self.opType == 'ADD_INANIMATED':
                    self.addKeyframe(obj, 'rigid_body.kinematic', curFrame)
                else:
                    return self.abort('Encountered Unexpected Error.' + obj.name)
                    
            self.report({'INFO'}, 'Done.') #no check if done successfully.
                        
        else: # DELETE
            
            isSuccess = True
                       
            for obj in targetObjects:
                if obj.animation_data and obj.animation_data.action:
                    
                    if self.opType == 'DELETE_VISIBILITY':
                        if not self.deleteKeyframe(obj, 'hide', curFrame):
                            isSuccess = False
                        if not self.deleteKeyframe(obj, 'hide_render', curFrame):
                            isSuccess = False
                    elif self.opType == 'DELETE_DYNAMIC':    
                        if not self.deleteKeyframe(obj, 'rigid_body.enabled', curFrame):
                            isSuccess = False
                    elif self.opType == 'DELETE_ANIMATED':
                        if not self.deleteKeyframe(obj, 'rigid_body.kinematic', curFrame):
                            isSuccess = False
                    else:
                        return self.abort('Encountered Unexpected Error.' + obj.name)
                    
                    # delete action if no fcurves remained. 
                    if len(obj.animation_data.action.fcurves) == 0:
                        obj.animation_data.action = None
                    # i won't do obj.animation_data_clear() because uncertain if it's ok to be deleted.
                
                else:
                    print(obj.name + ' has no action')
                    isSuccess = False
            
            if not isSuccess:
                print("if your objects share an action, warning is normal. I just didn't check these situation.")
                if self.opType == 'DELTE_VISIBILITY':
                    print("Also note, 'hide' means Visibility and 'hide_render' means RenderingVisibility")
                self.report({'WARNING'}, 'Done. Some were not succeed. See the console for details.')
            else:
                self.report({'INFO'}, 'Done Successfully.')
                
        return {'FINISHED'}
    
    #----------------
    def addKeyframe(self, obj, propName, curFrame):                
        
        targetFCurve = None
                
        for fcrv in obj.animation_data.action.fcurves:
            if fcrv.data_path == propName:
                targetFCurve = fcrv
                break
        
        if not targetFCurve:
            targetFCurve = obj.animation_data.action.fcurves.new(data_path=propName)
        
        y_val_is_zero = ['ADD_VISIBLE', 'ADD_UNDYNAMIC', 'ADD_INANIMATED']                 
        y_val = 0 if self.opType in y_val_is_zero else 1
        
        #.insert(frame, value, {'REPLACE', 'NEEDED', 'FAST'})
        kp = targetFCurve.keyframe_points.insert(curFrame, y_val , {'NEEDED','FAST'})
        kp.interpolation = 'CONSTANT'
        
    #------------------------
    def deleteKeyframe(self, obj, propName, curFrame):
        
        for fcrv in obj.animation_data.action.fcurves:
            if fcrv.data_path == propName:
                for kp in fcrv.keyframe_points:
                    if kp.co[0] == curFrame:
                        fcrv.keyframe_points.remove(kp, True) #2nd arg is FAST-enabled
                        if len(fcrv.keyframe_points) == 0:
                            obj.animation_data.action.fcurves.remove(fcrv)
                        
                        return True
                #end of for kep
        #end of for fcrv

        print(obj.name + "'s keyframe '" + propName + "' was not found.")
        return False

    #--------------
    def abort(self, mes):
        print(mes)
        self.report({'WARNING'}, "Couldn't execute. See the console for details...")
        return {'CANCELLED'}
    
####################################################### 
class ConstantKeyframesPanel(bpy.types.Panel):
    """Add/Remove Constant Keyframes"""

    bl_label = "Constant Keyframes"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_context = 'objectmode'
    
    def draw(self, context):
        layout = self.layout
        col = layout.column(align = True)
        col.label('If empty, selected objects are subject')
        col.prop(context.scene, 'constantKeyframes_groupName')
        col.separator()
        
        col.label('--- Visibility -------------------------------')
        col.operator('object.constant_keyframes_operator', text='Add Visible', icon='RESTRICT_VIEW_OFF').opType = 'ADD_VISIBLE'
        col.operator('object.constant_keyframes_operator', text='Add Invisible', icon='RESTRICT_VIEW_ON').opType = 'ADD_INVISIBLE'
        col.operator('object.constant_keyframes_operator', text='Delete', icon='X').opType = 'DELETE_VISIBILITY'
        
        col.separator()
        col.label('--- RigidBody -------------------------------')
        col.operator('object.constant_keyframes_operator', text='Add Dynamic', icon='UNPINNED').opType = 'ADD_DYNAMIC'
        col.operator('object.constant_keyframes_operator', text='Add Undynamic', icon='PINNED').opType = 'ADD_UNDYNAMIC'
        col.operator('object.constant_keyframes_operator', text='Delete', icon='X').opType = 'DELETE_DYNAMIC'

        col.separator()
        col.operator('object.constant_keyframes_operator', text='Add Animated', icon='POSE_DATA').opType = 'ADD_ANIMATED'
        col.operator('object.constant_keyframes_operator', text='Add Inanimated', icon='ARMATURE_DATA').opType = 'ADD_INANIMATED'
        col.operator('object.constant_keyframes_operator', text='Delete', icon='X').opType = 'DELETE_ANIMATED'

def register():
    bpy.utils.register_class(ConstantKeyframesOperator)
    bpy.utils.register_class(ConstantKeyframesPanel)


def unregister():
    bpy.utils.unregister_class(ConstantKeyframesOperator)
    bpy.utils.unregister_class(ConstantKeyframesPanel)



if __name__ == "__main__":
    register()
