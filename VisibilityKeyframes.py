##########################################
# Add/Remove VisibilityKeyframes
# Where : RunScript Then 3DView > Toolbar
# How : GroupName is empty, target is selected objects.
# version : 1.0
# I'll claim no right. Use or distribute at your own risk.
#########################################

import bpy

bpy.types.Scene.visKeyframes_groupName = bpy.props.StringProperty(name="GroupName", description="If empty, selected objects become subject", default="")

class VisibilityKeyframesOperator(bpy.types.Operator):
    """Add or Delete Keyframes for Viewport and Render Visibility at Current Frame"""
    bl_idname = "object.visibility_keyframes_operator"
    bl_label = "Visibility Keyframes Operator"

    opType = bpy.props.EnumProperty(
                              items=(('VISIBLE', 'Visible', 'Add Visible Keyframes'),
                                     ('INVISIBLE','Invisible', 'Add Invisible Keyframes'),
                                     ('DELETE', 'Delete', 'Delete Keyframes')), 
                                    name="Operation Type", 
                                    description="Add Keyframes (VISIBLE, INVISIBLE) or DELETE at Current Frame",
                                    default="VISIBLE")

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT'

    def execute(self, context):
        
        groupName = context.scene.visKeyframes_groupName
        
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

        if self.opType != 'DELETE':
            
            for obj in targetObjects:
                    
                    if not obj.animation_data: #this holds Action, Driver and NLA (and other?)
                        obj.animation_data_create()
                        
                    if not obj.animation_data.action:
                        obj.animation_data.action = bpy.data.actions.new(obj.name + 'Action')
                
                    fcrv_hide = None
                    fcrv_hideRender = None
                    
                    for fcrv in obj.animation_data.action.fcurves:
                        if fcrv.data_path == 'hide':
                            fcrv_hide = fcrv
                        elif fcrv.data_path == 'hide_render':
                            fcrv_hideRender = fcrv
                    
                    if not fcrv_hide:
                        fcrv_hide = obj.animation_data.action.fcurves.new(data_path="hide")
                    if not fcrv_hideRender:
                        fcrv_hideRender = obj.animation_data.action.fcurves.new(data_path="hide_render")
                                     
                    y_val = 0 if self.opType == 'VISIBLE' else 1
                    #.insert(frame, value, {'REPLACE', 'NEEDED', 'FAST'})
                    kp = fcrv_hide.keyframe_points.insert(curFrame, y_val , {'NEEDED','FAST'})
                    kp.interpolation = 'CONSTANT'
                    kp = fcrv_hideRender.keyframe_points.insert(curFrame, y_val , {'NEEDED','FAST'})
                    kp.interpolation = 'CONSTANT'
            
            self.report({'INFO'}, 'Done.') #no check if done successfully.
                        
        else: # opType == DELETE
            foundCount_hide = 0
            foundCount_hideRender = 0
            
            for obj in targetObjects:
                if obj.animation_data and obj.animation_data.action:
                    
                    for fcrv in obj.animation_data.action.fcurves:
                        if fcrv.data_path == 'hide' or fcrv.data_path == 'hide_render':                            
                            
                            for kp in fcrv.keyframe_points:
                                if kp.co[0] == curFrame:
                                    fcrv.keyframe_points.remove(kp, True) #2nd arg is FAST-enabled
                                    if len(fcrv.keyframe_points) == 0:
                                        obj.animation_data.action.fcurves.remove(fcrv)
                                    
                                    if fcrv.data_path == 'hide':
                                        foundCount_hide += 1
                                    else:
                                        foundCount_hideRender += 1
                                    
                                    break #get out of keyframe_points and goto next fcurve
                    
                    # delete action if no fcurves remained. 
                    if len(obj.animation_data.action.fcurves) == 0:
                        obj.animation_data.action = None
                    # i won't do obj.animation_data_clear() because uncertain if it's ok to be deleted.
            
            objCount = len(targetObjects)
            if foundCount_hide < objCount or foundCount_hideRender < objCount:
                self.report({'WARNING'}, 'Done. Some keyframes were not found.')
            else:
                self.report({'INFO'}, 'Done Successfully.')
                
        return {'FINISHED'}
    
    def abort(self, mes):
        print(mes)
        self.report({'WARNING'}, "Couldn't execute. See the console for details...")
        return {'CANCELLED'}
    
 
class VisibilityKeyframesPanel(bpy.types.Panel):
    """Collection of Buttons to Convert Objects to Linkable Animation"""

    bl_label = "Linkable Animation"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_context = 'objectmode'
    
    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.label('If empty, selected objects are subject')
        col.prop(context.scene, 'visKeyframes_groupName')
        col.separator()
        col.operator('object.visibility_keyframes_operator', text='Add Visible', icon='RESTRICT_VIEW_OFF').opType = 'VISIBLE'
        col.operator('object.visibility_keyframes_operator', text='Add Invisible', icon='RESTRICT_VIEW_ON').opType = 'INVISIBLE'
        col.operator('object.visibility_keyframes_operator', text='Delete', icon='X').opType = 'DELETE'


def register():
    bpy.utils.register_class(VisibilityKeyframesOperator)
    bpy.utils.register_class(VisibilityKeyframesPanel)


def unregister():
    bpy.utils.unregister_class(VisibilityKeyframesOperator)
    bpy.utils.unregister_class(VisibilityKeyframesPanel)



if __name__ == "__main__":
    register()
