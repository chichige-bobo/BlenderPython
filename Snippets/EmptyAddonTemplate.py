bl_info = {
    "name": "Empty Addon Template",
    "author": "Your Name Here",
    "version": (1, 0),
    "blender": (2, 65, 0),
    "location": "View3D > Add > Mesh > New Object",
    "description": "Adds a new Mesh Object",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Add Mesh"}


import bpy

class EmptyTemplate(bpy.types.Operator):
    """ToolTip"""
    bl_idname = "chichige.empty_template"
    bl_label = "Empty Template"
    bl_options = {'REGISTER', 'UNDO'}
    
    # name for label, desc for tooltip in Operator Panel
    # options = Enumerator in [‘HIDDEN’, ‘SKIP_SAVE’, ‘ANIMATABLE’, ‘LIBRARY_EDITABLE’] (and ‘ENUM_FLAG’ for EnumProp)
    my_bool =     bpy.props.BoolProperty(name="Bool Value", description="", default=False)                                      # subtype=[‘UNSIGNED’, ‘PERCENTAGE’, ‘FACTOR’, ‘ANGLE’, ‘TIME’, ‘DISTANCE’, ‘NONE’].
    my_boolVec =  bpy.props.BoolVectorProperty(name="BoolVector Value", description="", default=(False, False, False), size=3)  # subtype =  [‘COLOR’, ‘TRANSLATION’, ‘DIRECTION’, ‘VELOCITY’, ‘ACCELERATION’, ‘MATRIX’, ‘EULER’, ‘QUATERNION’, ‘AXISANGLE’, ‘XYZ’, ‘COLOR_GAMMA’, ‘LAYER’, ‘NONE’] 
    my_float =    bpy.props.FloatProperty(name="Float Value", description="", default=0.0, step=3, precision=2)                 # subtype = [‘UNSIGNED’, ‘PERCENTAGE’, ‘FACTOR’, ‘ANGLE’, ‘TIME’, ‘DISTANCE’, ‘NONE’]   # unit = [‘NONE’, ‘LENGTH’, ‘AREA’, ‘VOLUME’, ‘ROTATION’, ‘TIME’, ‘VELOCITY’, ‘ACCELERATION’]
    my_floatVec = bpy.props.FloatVectorProperty(name="FloatVec Value", description="", default=(0.0, 0.0, 0.0), step=3, precision=2, size=3)  # subtype = [‘COLOR’, ‘TRANSLATION’, ‘DIRECTION’, ‘VELOCITY’, ‘ACCELERATION’, ‘MATRIX’, ‘EULER’, ‘QUATERNION’, ‘AXISANGLE’, ‘XYZ’, ‘COLOR_GAMMA’, ‘LAYER’, ‘NONE’] #unit =  [‘NONE’, ‘LENGTH’, ‘AREA’, ‘VOLUME’, ‘ROTATION’, ‘TIME’, ‘VELOCITY’, ‘ACCELERATION’]
    my_int =      bpy.props.IntProperty(name="Int Value", description="", default=0, step=1)                                             # subtype = [‘UNSIGNED’, ‘PERCENTAGE’, ‘FACTOR’, ‘ANGLE’, ‘TIME’, ‘DISTANCE’, ‘NONE’]
    my_intVec =   bpy.props.IntVectorProperty(name="IntVec Value", description="", default=(0, 0, 0), size=3)                               # subtype = [‘COLOR’, ‘TRANSLATION’, ‘DIRECTION’, ‘VELOCITY’, ‘ACCELERATION’, ‘MATRIX’, ‘EULER’, ‘QUATERNION’, ‘AXISANGLE’, ‘XYZ’, ‘COLOR_GAMMA’, ‘LAYER’, ‘NONE’]
    my_string =   bpy.props.StringProperty(name="String Value", description="", default="", maxlen=0)                                       # subtype = [‘FILE_PATH’, ‘DIR_PATH’, ‘FILENAME’, ‘NONE’]
    my_enum =     bpy.props.EnumProperty(items = [('ENUM1', 'enum1', 'enum prop 1', 0), #[(identifier, name, description, number), ...]
                                                  ('ENUM2', 'enum2', 'enum prop 2', 1)],
                                         name="Enum Value", description="", default="")
    
    @classmethod
    def poll(cls, context):
        return context.object is not None
    
    def execute(self, context):
        self.report({'INFO'}, "Test Operator")
        return {'FINISHED'}
    
    #def invoke(self, context, event):
    #    context.window_manager.modal_handler_add(self)    
    #def modal(self, context, event):
    #def draw(self, context, event):

class EmptyTemplatePanel(bpy.types.Panel):
    """Creates a Panel in the ToolShelf in 3DView"""
    bl_label = "Hello World Panel"
    bl_idname = "OBJECT_PT_hello"
    
    bl_space_type = 'VIEW_3D' #[‘EMPTY’, ‘VIEW_3D’, ‘GRAPH_EDITOR’, ‘OUTLINER’, ‘PROPERTIES’,... much more!
    bl_region_type = 'TOOLS' #‘WINDOW’, ‘HEADER’, ‘CHANNELS’, ‘TEMPORARY’, ‘UI’, ‘TOOLS’, ‘TOOL_PROPS’, ‘PREVIEW’
    #bl_options = {'DEFAULT_CLOSED'}

    #bl_space_type = 'PROPERTIES'
    #bl_region_type = 'WINDOW'
    #bl_context = "scene"
    #bl_options = {'HIDE_HEADER'}
    
    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.operator(EmptyTemplate.bl_idname).my_string = 'some'
        col.prop(context.scene.et_props, 'et_int')

#------------
class EmptyTemplate_PropsAttachedToScene(bpy.types.PropertyGroup):
    et_int = bpy.props.IntProperty()
    et_float = bpy.props.FloatProperty()
    et_string = bpy.props.StringProperty()
    
bpy.utils.register_class(EmptyTemplate_PropsAttachedToScene)
bpy.types.Scene.et_props = bpy.props.PointerProperty(type = EmptyTemplate_PropsAttachedToScene)

#-------------
def menu_func(self, context):
    self.layout.operator(EmptyTemplate.bl_idname, icon = 'PLUGIN')
    self.layout.operator(EmptyTemplate.bl_idname, text = "EmptyTemplate (with Prop)", icon = 'BLENDER').my_string = 'some'


# Registration---------------------------------------------

# store keymaps here to access after registration
addon_keymaps = []

def register():
    bpy.utils.register_class(EmptyTemplate)
    bpy.utils.register_class(EmptyTemplatePanel)
    bpy.types.VIEW3D_MT_object.append(menu_func)

    # handle the keymap
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
    kmi = km.keymap_items.new(EmptyTemplate.bl_idname, 'SPACE', 'PRESS', ctrl=True, shift=True)
    #kmi.properties.prop1 = 'some'
    addon_keymaps.append((km, kmi))

def unregister():
    bpy.utils.unregister_class(EmptyTemplate)
    bpy.types.VIEW3D_MT_object.remove(menu_func)

    # handle the keymap
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    
if __name__ == "__main__":
    register()
    
    #test call
    bpy.ops.chichige.empty_template('EXEC_DEFAULT')#, my_string = 'some') or 'INVOKE_DEFAULT'
