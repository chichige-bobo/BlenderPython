import bpy


class PreparedValueProps(bpy.types.PropertyGroup):
    armatureObjectName = bpy.props.StringProperty(name="ArmaObjName", default='Armature', description="Name of Armature Object which contains controll bone")
    boneName_const = bpy.props.StringProperty(name="TransController", default='TransformController', description="Name of a Bone which becomes the Target of ActionConstraint")
    boneName_vis = bpy.props.StringProperty(name="VisController", default='VisibilityController', description="Name of a Bone which Controls Visibility via Driver") #if not use this function, no need to set
    
    action_frameStart = bpy.props.IntProperty(name="StartFrame", default=1, description="Start frame designated in ActionConstraint")
    action_frameEnd = bpy.props.IntProperty(name="EndFrame", default=100, description="End frame designated in ActionConstraint")


#################################################################
# What this operator do...
# 1. Add new ActionConstraint named 'TransformAction' to selected objects
# 2. Unlink the action from the objects to avoid dual effect.
# 3. Clear location, rotation, size which controled by the action.
#  
# You MUST prepare Armature and set its name.
#
class ChangeToActionConstraintOperator(bpy.types.Operator):
    """Change Linked Action to ActionConstraint named 'TransformAction'"""
    bl_idname = "object.change_to_action_constraint_operator"
    bl_label = "Change to Action Constraint for Selected Objects"

    @classmethod
    def poll(cls, context):
        return (context.area.type == 'VIEW_3D' and \
                context.mode == 'OBJECT' and \
                len(context.selected_objects) > 0 )

    def execute(self, context):
    
        armatureObjectName = context.scene.linkAnimProps.armatureObjectName
        boneName_const = context.scene.linkAnimProps.boneName_const
        
        action_frameStart = context.scene.linkAnimProps.action_frameStart
        action_frameEnd = context.scene.linkAnimProps.action_frameEnd
                
        # validation---------------
        if armatureObjectName.strip() == '':
            return self.abort('Armature object name is not correct')

        if boneName_const.strip() == '':
            return self.abort('Name of Tranfom controller bone is not correct')
                
        if not armatureObjectName in bpy.data.objects.keys():
            return self.abort(armatureObjectName + ' was not found')

        armaObj = bpy.data.objects[armatureObjectName]        
        if not boneName_const in armaObj.data.bones.keys():
            return self.abort(boneName_const + ' bone was not found')
        
        if len(context.selected_objects) == 0:
            return self.abort('Nothing selected')
        
        for obj in context.selected_objects:
            if not obj.animation_data or not obj.animation_data.action:
                return self.abort(obj.name + ' has no Action')
            if 'TransformAction' in obj.constraints.keys():
                return self.abort(obj.name + ' already has TransformAction constraint')

        # execute ------------------ 
        
        armaObj = bpy.data.objects[armatureObjectName]
    
        for obj in context.selected_objects:
            cnst = obj.constraints.new(type = 'ACTION')    
            cnst.name = 'TransformAction'
            cnst.target = armaObj
            cnst.subtarget = boneName_const
            cnst.transform_channel = 'LOCATION_Y'
            cnst.target_space = 'LOCAL'
            cnst.action = bpy.data.actions[obj.animation_data.action.name]
            cnst.min = 0
            cnst.max = 3
            cnst.frame_start = action_frameStart
            cnst.frame_end = action_frameEnd
            
            # detouch action and clear values which is in the action
            # this section below doesn't care about delta transform. sorry.
            # how to distinct each curve. .data_path == 'location' and .array_index == 0 is XLocation 
            # http://blenderartists.org/forum/archive/index.php/t-207568.html
            act = obj.animation_data.action
            obj.animation_data.action = None #if do this later, automatically keyed?
            
            for fcrv in act.fcurves:
                if fcrv.data_path == 'location':
                    obj.location[fcrv.array_index] = 0
                elif fcrv.data_path == 'rotation_euler':
                    obj.rotation_euler[fcrv.array_index] = 0
                elif fcrv.data_path == 'rotation_quaternion':
                    obj.rotation_quaternion[fcrv.array_index] = 0
                elif fcrv.data_path == 'scale':
                    obj.scale[fcrv.array_index] = 0
        
        return {'FINISHED'}

    def abort(self, mes):
        print(mes)
        self.report({'WARNING'}, "Couldn't execute. See the console for details...")
        return {'CANCELLED'}
  
#####################################################################

class UpdateValuesOfTransformActionConstraintOperator(bpy.types.Operator):
    """Update Values of ActionConstrint named TransformAction on Selected Objects"""

    bl_idname = "object.update_values_of_action_constraint_operator"
    bl_label = "Update Values of TransformAction Constraint on Selected Objects"

    @classmethod
    def poll(cls, context):
        return (context.area.type == 'VIEW_3D' and \
                context.mode == 'OBJECT' and \
                len(context.selected_objects) > 0 )

    def execute(self, context):
        
        armatureObjectName = context.scene.linkAnimProps.armatureObjectName
        boneName_const = context.scene.linkAnimProps.boneName_const
                 
        action_frameStart = context.scene.linkAnimProps.action_frameStart
        action_frameEnd = context.scene.linkAnimProps.action_frameEnd

        # validation---------------
        # this op is maintenance purpose. so, not strictly restricted 
        if armatureObjectName.strip() == '':
            return self.abort('Armature object name is not correct')

        if boneName_const.strip() == '':
            return self.abort('Name of Tranfom controller bone is not correct')
                
        if not armatureObjectName in bpy.data.objects.keys():
            return self.abort(armatureObjectName + ' was not found')

        armaObj = bpy.data.objects[armatureObjectName]        
        if not boneName_const in armaObj.data.bones.keys():
            return self.abort(boneName_const + ' bone was not found')
        
        if len(context.selected_objects) == 0:
            return self.abort('Nothing selected')
        
        # execute ------------------ 
        
        armaObj = bpy.data.objects[armatureObjectName]
    
        for obj in context.selected_objects:
            for cnst in obj.constraints:
                if cnst.name == 'TransformAction' and cnst.type == 'ACTION':    
                    cnst.target = armaObj
                    cnst.subtarget = boneName_const
                    cnst.transform_channel = 'LOCATION_Y'
                    cnst.target_space = 'LOCAL'
                    #cnst.action = bpy.data.actions[obj.name + 'Action']
                    cnst.min = 0
                    cnst.max = 5
                    cnst.frame_start = action_frameStart
                    cnst.frame_end = action_frameEnd
                    
        return {'FINISHED'}

    def abort(self, mes):
        print(mes)
        self.report({'WARNING'}, "Couldn't execute. See the console for details...")
        return {'CANCELLED'}

#################################################################    
class RestoreTransformActionConstraintToLinkedActionOperator(bpy.types.Operator):
    """Restore TransformAction Constraint to Linked Action"""
    bl_idname = "object.restore_transform_action_const_to_linked_operator"
    bl_label = "Restore TransformAction Constraint to Linked Action for Selected Objects"

    @classmethod
    def poll(cls, context):
        return (context.area.type == 'VIEW_3D' and \
                context.mode == 'OBJECT' and \
                len(context.selected_objects) > 0 )

    def execute(self, context):
        
        # validation---------------        
        # this op is maintenance purpose. so, not strictly restricted                       
        if len(context.selected_objects) == 0:
            return self.abort('Nothing selected')
        
        # if not check at here, some objects remained with constraints after execution.
        for obj in context.selected_objects:
            if obj.animation_data and obj.animation_data.action:
                return self.abort(obj.name + ' already has linked Action')
        
        # execute ------------------ 
        
        
        for obj in context.selected_objects:
            for cnst in obj.constraints:
                if cnst.name == 'TransformAction' and cnst.type == 'ACTION':
                    act = cnst.action
                    obj.constraints.remove(cnst)   
                    obj.animation_data.action = act

        return {'FINISHED'}

    def abort(self, mes):
        print(mes)
        self.report({'WARNING'}, "Couldn't execute. See the console for details...")
        return {'CANCELLED'}

##############################################################
# Connect a bone as driver to selected objects.
# Subject properties are Eye icon and Camera icon in Outliner.
# If the object already has visibility driver, this op modifies it.
# If the driver has GENERATOR modifier on slot 0, the mod will get deleted
#  (the mod automatically added by driver_add(). If the driver added through GUI, no modefier is added)
#
class AddVisibilityDriverOperator(bpy.types.Operator):
    """Connect a Bone as Driver to Selected Objects"""

    bl_idname = "object.add_visibility_driver_operator"
    bl_label = "Add Visibility Driver to Selected Objects"
        
    @classmethod
    def poll(cls, context):
        return (context.area.type == 'VIEW_3D' and \
                context.mode == 'OBJECT' and \
                len(context.selected_objects) > 0 )

    def execute(self, context):
        
        armatureObjectName = context.scene.linkAnimProps.armatureObjectName
        boneName_vis = context.scene.linkAnimProps.boneName_vis
        
        # validation---------------
        
        if armatureObjectName.strip() == '':
            return self.abort('Armature object name is not correct')

        if boneName_vis.strip() == '':
            return self.abort('Name of Visibility controller bone is not correct')
                
        isError = False
        armaObj = bpy.data.objects[armatureObjectName]
        if not armaObj:
            return self.abort(armatureObjectName + ' was not found')
        
        if not boneName_vis in armaObj.data.bones.keys():
            return self.abort(boneName_vis + ' bone was not found')
        
        if len(context.selected_objects) == 0:
            return self.abort('Nothing selected')

        allowedTypes = ['MESH', 'CURVE', 'SURFACE', 'META', 'FONT', 'LAMP']
        for obj in context.selected_objects:
            if not obj.type in allowedTypes:
                return self.abort(obj.name + ' is not allowed type')
        
        
        # execute ------------------ 
        
        for obj in context.selected_objects:           
            self.setDriverToFCurve(obj.driver_add('hide'), armatureObjectName, boneName_vis) #probably driver_add() is singleton in my experiment.
            self.setDriverToFCurve(obj.driver_add('hide_render'), armatureObjectName, boneName_vis) 
        
        return {'FINISHED'}
    
    
    def setDriverToFCurve(self, fcrv, armatureObjectName, boneName_vis):

        drv = fcrv.driver
        if len(drv.variables) == 0:
            drv.variables.new() 
        
        drvVar = drv.variables[0] 
        drvVar.name = 'var'
        drvVar.type = 'TRANSFORMS'
        drvVar.targets[0].id = bpy.data.objects[armatureObjectName]
        drvVar.targets[0].bone_target = boneName_vis
        drvVar.targets[0].transform_type = 'LOC_Y'
        drvVar.targets[0].transform_space = 'LOCAL_SPACE'
        drv.type = 'SCRIPTED'
        drv.expression = 'True if var > 0.25 else False'
        
        if len(fcrv.modifiers) > 0 and fcrv.modifiers[0].type == 'GENERATOR':
            fcrv.modifiers.remove(fcrv.modifiers[0])
    
    def abort(self, mes):
        print(mes)
        self.report({'WARNING'}, "Couldn't execute. See the console for details...")
        return {'CANCELLED'}

###############################################################

class RemoveVisibilityDriverOperator(bpy.types.Operator):
    """Remove Visibility Driver from Selected Objects   """

    bl_idname = "object.remove_visibility_driver_operator"
    bl_label = "Remove Visibility Driver from Selected Objects"
      
    @classmethod
    def poll(cls, context):
        return (context.area.type == 'VIEW_3D' and \
                context.mode == 'OBJECT' and \
                len(context.selected_objects) > 0 )

    def execute(self, context):
 
        # validation---------------
        # out of types means set by other way.
        allowedTypes = ['MESH', 'CURVE', 'SURFACE', 'META', 'FONT', 'LAMP']
        for obj in context.selected_objects:
            if not obj.type in allowedTypes:
                print(obj.name + ' is not allowed type.')
                self.report({'WARNING'}, "Couldn't execute. See the console for details...")
                return {'CANCELLED'}
                
        # execute ------------------ 
        
        for obj in context.selected_objects:
            obj.driver_remove('hide')
            obj.driver_remove('hide_render')          
        
        return {'FINISHED'}


############################################################
# Toolbar Panel
class LinkableAnimationPanel(bpy.types.Panel):
    """Collection of Buttons to Convert Objects to Linkable Animation"""

    bl_label = "Linkable Animation"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    #bl_context = "object"

    def draw(self, context):
        layout = self.layout

        col = layout.column()
        col.label('--- Properties -----------------------')
        col.prop(context.scene.linkAnimProps, 'armatureObjectName')
        col.prop(context.scene.linkAnimProps, 'boneName_const')
        col.prop(context.scene.linkAnimProps, 'boneName_vis')
        col.separator()
        row = col.row(align = True)
        row.prop(context.scene.linkAnimProps, 'action_frameStart')
        row.prop(context.scene.linkAnimProps, 'action_frameEnd')
        col.separator()
        
        #col.prop("object.change_to_action_constraint_operator", 'armaObjName')
        col.label('--- Main Operation -------------------')
        col.label('parent to root bone before change to')
        col.operator('object.change_to_action_constraint_operator', text='Change To Constrinat', icon = 'CONSTRAINT')
        col.operator('object.add_visibility_driver_operator', text = 'Add Visibility Driver', icon = 'DRIVER')

        col = layout.column(align=True)
        col.label('--- Maintenance ----------------------')
        col.operator('object.update_values_of_action_constraint_operator', text = 'Update Constraints', icon = 'CONSTRAINT_DATA')
        col.operator('object.restore_transform_action_const_to_linked_operator', text = 'Restore Action', icon = 'ACTION')
        
        col = layout.column()
        col.operator('object.remove_visibility_driver_operator', text = 'Remove Vis Driver', icon = 'PANEL_CLOSE')


def register():    
    bpy.utils.register_class(PreparedValueProps)
    bpy.types.Scene.linkAnimProps = bpy.props.PointerProperty(type=PreparedValueProps)
    
    bpy.utils.register_class(AddVisibilityDriverOperator)
    bpy.utils.register_class(RemoveVisibilityDriverOperator)
    bpy.utils.register_class(ChangeToActionConstraintOperator)
    bpy.utils.register_class(UpdateValuesOfTransformActionConstraintOperator)
    bpy.utils.register_class(RestoreTransformActionConstraintToLinkedActionOperator)
    bpy.utils.register_class(LinkableAnimationPanel)

def unregister():
    bpy.utils.unregister_class(AddVisibilityDriverOperator)
    bpy.utils.unregister_class(RemoveVisibilityDriverOperator)
    bpy.utils.unregister_class(ChangeToActionConstraintOperator)
    bpy.utils.unregister_class(UpdateValuesOfTransformActionConstraintOperator)
    bpy.utils.unregister_class(RestoreTransformActionConstraintToLinkedActionOperator)
    bpy.utils.unregister_class(LinkableAnimationPanel)

if __name__ == "__main__":
    register()
