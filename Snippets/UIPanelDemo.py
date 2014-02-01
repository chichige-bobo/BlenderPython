import bpy
from bpy.props import *
######################################################
# Index
# advancedBox_reflesh()
# class UIDemo_AdvancedBoxElements
# class UIDemo_PropsAttachedToScene
#
# class DoNothingOperator
#
# class UIPanelDemo_Layout
# class UIPanelDemo_Props
# class UIPanelDemo_Misc
########################################################

# This function called when following prop's IntProp named 'demo_advanced_box_num'
# I got AttributeError when I tried to do in panel's draw()
#http://lists.blender.org/pipermail/bf-blender-cvs/2011-June/036463.html
def advancedBox_reflesh(self, context):
    scene = context.scene
    ps = scene.chichige_ui_demo_props

    boxNum = ps.demo_advanced_box_num
    if boxNum < 0 or boxNum > 5:
        boxNum = 5
   
    boxElems = ps.demo_advanced_box_elements
    if len(boxElems) < boxNum:
        for i in range(len(boxElems), boxNum):
            boxElems.add()
    elif len(boxElems) > boxNum:
        for i in range(boxNum, len(boxElems)):
            boxElems.remove(i)

class UIDemo_AdvancedBoxElements(bpy.types.PropertyGroup):
    box_file =  StringProperty(name="StringName", default="", subtype='FILE_PATH')
    box_tab = EnumProperty(items = [('ENUM1_ID', 'TabLikeEnum1', 'enum1 desc'), 
                                    ('ENUM2_ID', 'TabLikeEnum2', 'enum2 desc')],
                                         name="TabLikeEnumTopName",
                                         description="",
                                         default="ENUM1_ID")
  
#------------
class UIDemo_PropsAttachedToScene(bpy.types.PropertyGroup):
    demo_bool =     BoolProperty(       name="BoolName",     description="Bool desc")                          
    demo_boolVec =  BoolVectorProperty( name="BoolVecName",  description="BoolVec desc")  
    demo_float =    FloatProperty(      name="FloatName",    description="Float desc")       
    demo_floatVec = FloatVectorProperty(name="FloatVecName", description="FloatVec desc") 
    demo_int =      IntProperty(        name="IntName",      description="Int desc")                      
    demo_intVec =   IntVectorProperty(  name="IntVecName",   description="IntVec desc")              
    demo_string =   StringProperty(     name="StringName",   description="String desc",  maxlen=0)            
    #----
    demo_bool_unsigned = BoolProperty( name="BoolName", description="Bool desc", subtype = 'UNSIGNED')
    demo_bool_angle =    BoolProperty( name="BoolName", description="Bool desc", subtype = 'ANGLE')
    demo_boolVec_color = BoolVectorProperty(  name="BoolVecName", description="BoolVec desc", subtype = 'COLOR')
    demo_boolVec_xyz =   BoolVectorProperty(  name="BoolVecName", description="BoolVec desc", subtype = 'XYZ')
    demo_boolVec_layer = BoolVectorProperty(  name="BoolVecName", description="BoolVec desc", subtype = 'LAYER', size=32)

    demo_float_minMax = FloatProperty(name="FloatName",     description="Float desc", min = -100, max = 100)
    demo_float_softMinMax = FloatProperty(name="FloatName", description="Float desc", soft_min = -100, soft_max = 100)
    demo_float_bothMinMax = FloatProperty(name="FloatName", description="Float desc", min = -200, max = 200, soft_min = -100, soft_max = 100)
    demo_float_step16 = FloatProperty(name="FloatName",     description="Float desc", step = 16)
    demo_float_prec6 = FloatProperty(name="FloatName",      description="Float desc", precision = 6)
    
    demo_float_factor_length = FloatProperty(name="FloatName", description="Float desc", subtype = 'FACTOR', unit = 'LENGTH')
    demo_float_factor_area =   FloatProperty(name="FloatName", description="Float desc", subtype = 'FACTOR', unit = 'AREA')
    demo_float_factor_volume = FloatProperty(name="FloatName", description="Float desc", subtype = 'FACTOR', unit = 'VOLUME')
    demo_float_time_none = FloatProperty(name="FloatName", description="Float desc", subtype = 'TIME', unit = 'NONE')
    demo_float_time_time = FloatProperty(name="FloatName", description="Float desc", subtype = 'TIME', unit = 'TIME')

    demo_floatVec_size2=     FloatVectorProperty(name="FloatVecName", description="FloatVec desc", size = 2)
    demo_floatVec_color =    FloatVectorProperty(name="FloatVecName", description="FloatVec desc", subtype = 'COLOR') 
    demo_floatVec_trans =    FloatVectorProperty(name="FloatVecName", description="FloatVec desc", subtype = 'TRANSLATION') 
    demo_floatVec_direct =   FloatVectorProperty(name="FloatVecName", description="FloatVec desc", subtype = 'DIRECTION') 
    demo_floatVec_velocity = FloatVectorProperty(name="FloatVecName", description="FloatVec desc", subtype = 'VELOCITY') 
    demo_floatVec_accel =    FloatVectorProperty(name="FloatVecName", description="FloatVec desc", subtype = 'ACCELERATION') 
    demo_floatVec_matrix =   FloatVectorProperty(name="FloatVecName", description="FloatVec desc", subtype = 'MATRIX') 
    demo_floatVec_euler =    FloatVectorProperty(name="FloatVecName", description="FloatVec desc", subtype = 'EULER') 
    demo_floatVec_quater =   FloatVectorProperty(name="FloatVecName", description="FloatVec desc", subtype = 'QUATERNION') 
    demo_floatVec_axis =     FloatVectorProperty(name="FloatVecName", description="FloatVec desc", subtype = 'AXISANGLE') 
    demo_floatVec_xyz =      FloatVectorProperty(name="FloatVecName", description="FloatVec desc", subtype = 'XYZ') 
    demo_floatVec_colorGamma = FloatVectorProperty(name="FloatVecName_colorGamma", description="FloatVec desc", subtype = 'COLOR_GAMMA') 
    demo_floatVec_layer =    FloatVectorProperty(name="FloatVecName_layer", description="FloatVec desc", subtype = 'LAYER') 

    demo_string_max5  = StringProperty(name="StringName", description="String desc", maxlen=5)            
    demo_string_fpath = StringProperty(name="StringName", description="String desc", subtype = 'FILE_PATH')            
    demo_string_dir   = StringProperty(name="StringName", description="String desc", subtype = 'DIR_PATH')            
    demo_string_fname = StringProperty(name="StringName", description="String desc", subtype = 'FILE_NAME')            
    #------
    demo_enum = EnumProperty(items = [('ENUM1_ID', 'enum1_name', 'enum1 desc'), 
                                      ('ENUM2_ID', 'enum2_name', 'enum2 desc'),
                                      ('ENUM3_ID', 'enum3_name', 'enum3 desc')],
                             name="EnumTopName",
                             description="Enum top desc",
                             default= "ENUM1_ID") 
    
    demo_enum_multi = EnumProperty(items = [('MUL1_ID', 'mul1_name', 'enum1 desc', 1), # it seemed ok if the number omitted 
                                            ('MUL2_ID', 'mul2_name', 'enum2 desc', 2), # Used numbers are just guess work. I don't know exact rule. bit?
                                            ('MUL3_ID', 'mul3_name', 'enum3 desc', 4),
                                            ('MUL4_ID', 'mul4_name', 'enum4 desc', 8)],
                                   name="EnumMultiTopName",
                                   description="EnumMulti top desc",
                                   default= {"MUL1_ID", "MUL3_ID"},
                                   options = {"ENUM_FLAG"}) 
    #-------
    demo_advanced_box_num = IntProperty(name="IntName", min = 0, max = 5, update = advancedBox_reflesh)
    demo_advanced_box_elements = CollectionProperty(type = UIDemo_AdvancedBoxElements)
    
bpy.utils.register_class(UIDemo_AdvancedBoxElements)
bpy.utils.register_class(UIDemo_PropsAttachedToScene)

# Add these properties to every scene in the entire Blender system (muha-haa!!)
bpy.types.Scene.chichige_ui_demo_props = PointerProperty(type = UIDemo_PropsAttachedToScene)

# subtype is...
# Bool        ['UNSIGNED', 'PERCENTAGE', 'FACTOR', 'ANGLE', 'TIME', 'DISTANCE', 'NONE'].
# BoolVector  ['COLOR', 'TRANSLATION', 'DIRECTION', 'VELOCITY', 'ACCELERATION', 'MATRIX', 'EULER', 'QUATERNION', 'AXISANGLE', 'XYZ', 'COLOR_GAMMA', 'LAYER', 'NONE'] 
# Float       ['UNSIGNED', 'PERCENTAGE', 'FACTOR', 'ANGLE', 'TIME', 'DISTANCE', 'NONE'] 
#      unit = ['NONE', 'LENGTH', 'AREA', 'VOLUME', 'ROTATION', 'TIME', 'VELOCITY', 'ACCELERATION']
# FloatVector ['COLOR', 'TRANSLATION', 'DIRECTION', 'VELOCITY', 'ACCELERATION', 'MATRIX', 'EULER', 'QUATERNION', 'AXISANGLE', 'XYZ', 'COLOR_GAMMA', 'LAYER', 'NONE'] 
#     unit =  ['NONE', 'LENGTH', 'AREA', 'VOLUME', 'ROTATION', 'TIME', 'VELOCITY', 'ACCELERATION']
# Int         ['UNSIGNED', 'PERCENTAGE', 'FACTOR', 'ANGLE', 'TIME', 'DISTANCE', 'NONE']
# IntVector   ['COLOR', 'TRANSLATION', 'DIRECTION', 'VELOCITY', 'ACCELERATION', 'MATRIX', 'EULER', 'QUATERNION', 'AXISANGLE', 'XYZ', 'COLOR_GAMMA', 'LAYER', 'NONE']
# String      ['FILE_PATH', 'DIR_PATH', 'FILENAME', 'NONE']

##############################################################################################
##############################################################################################

class DoNothingOp(bpy.types.Operator):
    """ToolTip is written in class doc"""
    bl_idname = "do.nothing"
    bl_label = "DoNothingOperator"
    bl_options = {'REGISTER', 'UNDO'}
    
    ### these props will automatically shown in OperatorPanel when executed.
    # name for label, desc for tooltip in Operator Panel
    # options = Enumerator in ['HIDDEN', 'SKIP_SAVE', 'ANIMATABLE', 'LIBRARY_EDITABLE'] (and 'ENUM_FLAG' for EnumProp)
    my_bool =     BoolProperty(       name="BoolName",     description="Bool desc",)
    my_boolVec =  BoolVectorProperty( name="BoolVecName",  description="BoolVec desc") 
    my_float =    FloatProperty(      name="FloatName",    description="Float desc")  
    my_floatVec = FloatVectorProperty(name="FloatVecName", description="FloatVec desc")  
    my_int =      IntProperty(        name="IntName",      description="Int desc") 
    my_intVec =   IntVectorProperty(  name="IntVecName",   description="IntVec desc")
    my_string =   StringProperty(     name="StringName",   description="String desc") 
    #[(identifier, name, description, number), ...]
    my_enum =     EnumProperty(items = [('ENUM1_ID', 'enum1_name', 'enum1 desc'), 
                                        ('ENUM2_ID', 'enum2_name', 'enum2 desc'),
                                        ('ENUM3_ID', 'enum3_name', 'enum3 desc')],
                                         name="Operator'sEnumTopName",
                                         description="",
                                         default="ENUM1_ID")
    
    def execute(self, context):
        print(self)
        self.report({'INFO'}, "Hello UILayout")
        return {'FINISHED'}
    
    #def draw(self, context, event):

##############################################################################################
##############################################################################################

class UIPanelDemo_Layout(bpy.types.Panel):
    """UIPanel Demo Layout class doc"""
    bl_label = "UIPanel Demo Layout bl_label"
    bl_idname = "ui_panel_demo_layout"
    
    # Tool shelf
    bl_space_type = 'VIEW_3D' 
    bl_region_type = 'TOOLS' 
    
    def draw(self, context):
        layout = self.layout

        #layout.operator_context = 'INVOKE_DEFAULT'#[‘INVOKE_DEFAULT’, ‘INVOKE_REGION_WIN’, ‘INVOKE_REGION_CHANNELS’, ‘INVOKE_REGION_PREVIEW’, ‘INVOKE_AREA’, ‘INVOKE_SCREEN’, ‘EXEC_DEFAULT’, ‘EXEC_REGION_WIN’, ‘EXEC_REGION_CHANNELS’, ‘EXEC_REGION_PREVIEW’, ‘EXEC_AREA’, ‘EXEC_SCREEN’]
        
        #if you want to designate some operator props
        #layout.operator(DoNothingOp.bl_idname).my_string = 'some'
        # or
        #temp = layout.operator(DoNothingOp.bl_idname)
        #temp.my_string = 'some'
        #temp.my_int = 10
        
        layout.label('Direct Placement ----------------')
        layout.operator(DoNothingOp.bl_idname, text = 'Operator')
        layout.operator(DoNothingOp.bl_idname, text = 'Operator')
        layout.label('Column --------------------------')
        col = layout.column()
        col.operator(DoNothingOp.bl_idname, text = 'Operator')
        col.operator(DoNothingOp.bl_idname, text = 'Operator')
        layout.label('Column with align  -------------')
        col = layout.column(align = True)
        col.operator(DoNothingOp.bl_idname, text = 'Operator')
        col.operator(DoNothingOp.bl_idname, text = 'Operator')
        layout.label('Column flow (3) ----------------')
        col = layout.column_flow(3)
        col.operator(DoNothingOp.bl_idname, text = 'Op1')
        col.operator(DoNothingOp.bl_idname, text = 'Op2')
        col.operator(DoNothingOp.bl_idname, text = 'Op3')
        col.operator(DoNothingOp.bl_idname, text = 'Op4')
        col.operator(DoNothingOp.bl_idname, text = 'Op5')
        col.operator(DoNothingOp.bl_idname, text = 'Op6')
        col.operator(DoNothingOp.bl_idname, text = 'Op7')
        layout.label('Box ---------------------------')
        box = layout.box()
        box.operator(DoNothingOp.bl_idname, text = 'Operator')
        box.operator(DoNothingOp.bl_idname, text = 'Operator')
        layout.label('Split -------------------------')
        spl = layout.split()
        col = spl.column()
        col.operator(DoNothingOp.bl_idname, text = 'Op1')
        col.operator(DoNothingOp.bl_idname, text = 'Op2')
        col.operator(DoNothingOp.bl_idname, text = 'Op3')
        col = spl.column()        
        col.operator(DoNothingOp.bl_idname, text = 'Op1')
        col.separator()
        col.operator(DoNothingOp.bl_idname, text = 'Op2')
        col.separator()
        col.operator(DoNothingOp.bl_idname, text = 'Op3')
        col = spl.column()
        col.label('longtextlabel_123456789012345678901234567890')
        col.label('Seems splited evenly')
        col.operator(DoNothingOp.bl_idname, text = 'Op1')
        col.operator(DoNothingOp.bl_idname, text = 'Op2')
        col.operator(DoNothingOp.bl_idname, text = 'Op3')
        col.operator(DoNothingOp.bl_idname, text = 'Op4')

        layout.label('Split(0.5) --------------------')
        spl = layout.split(0.5)
        spl.operator(DoNothingOp.bl_idname, text = 'Operator')
        spl.operator(DoNothingOp.bl_idname, text = 'Operator')
        spl.operator(DoNothingOp.bl_idname, text = 'Operator')
        spl.operator(DoNothingOp.bl_idname, text = 'Operator')
        layout.label('Split(0.8) --------------------')
        spl = layout.split(0.8)
        spl.operator(DoNothingOp.bl_idname, text = 'Operator')
        spl.operator(DoNothingOp.bl_idname, text = 'Operator')
        spl.operator(DoNothingOp.bl_idname, text = 'Operator')
        spl.operator(DoNothingOp.bl_idname, text = 'Operator')
        col = layout.column()
        col.scale_x = col.scale_y = 2
        col.label('Column (scale_x,_y = 2) ---------')
        col.operator(DoNothingOp.bl_idname, text = 'Operator')
        col.operator(DoNothingOp.bl_idname, text = 'Operator')
        col = layout.column()
        col.scale_x = 0.5
        col.alignment = 'LEFT'
        col.label('Column (scale_x = 0.5 & LEFT alignment) -------')
        col.operator(DoNothingOp.bl_idname, text = 'Operator')
        col.operator(DoNothingOp.bl_idname, text = 'Operator')
        layout.label('Row --------------------------')
        row = layout.row()
        row.operator(DoNothingOp.bl_idname, text = 'Operator')
        row.operator(DoNothingOp.bl_idname, text = 'Operator')
        row.operator(DoNothingOp.bl_idname, text = 'Operator')
        layout.label('Another Row --------------------------')
        row = layout.row()
        row.operator(DoNothingOp.bl_idname, text = 'Operator')
        row.operator(DoNothingOp.bl_idname, text = 'Operator')
        col = row.column()
        col.label('Col in Row --------------------------')
        col.operator(DoNothingOp.bl_idname, text = 'Operator')
        col.operator(DoNothingOp.bl_idname, text = 'Operator')
        row.operator(DoNothingOp.bl_idname, text = 'Operator')



            
##############################################################################################
##############################################################################################

class UIPanelDemo_Props(bpy.types.Panel):
    """UIPanel Demo Props class doc"""
    bl_label = "UIPanel Demo Props bl_label"
    bl_idname = "ui_panel_demo_props"
    
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS' 
    
    def draw(self, context):
        layout = self.layout
        layout.label('Bool -----------------------------')
        #prop(data, property, text="", icon='NONE', expand=False, slider=False, toggle=False, icon_only=False, event=False, full_event=False, emboss=True, index=-1)
        ps = context.scene.chichige_ui_demo_props
        row = layout.row()
        row.prop(ps, 'demo_bool')
        row.prop(ps, 'demo_bool', text = 'Bool(icon_only)', icon_only = True)
        row = layout.row()
        row.prop(ps, 'demo_bool', text = 'Bool(no emboss)', emboss = False)
        row.prop(ps, 'demo_bool_unsigned')
        row = layout.row()
        row.prop(ps, 'demo_bool_angle', text = 'angle')
        row.prop(ps, 'demo_bool_angle', text = 'angle (toggle)', toggle = True)
        
        layout.label('BoolVector -----------------------------')
        layout.prop(ps, 'demo_boolVec_color', text = 'BoolVec_color (default)')
        layout.prop(ps, 'demo_boolVec_color', text = 'BoolVec_color (icon)', icon = 'BLENDER')
        layout.prop(ps, 'demo_boolVec_color', text = 'BoolVec_color (no expand)', expand = False)
        layout.prop(ps, 'demo_boolVec_color', text = 'BoolVec_color (expand)', expand = True)
        layout.prop(ps, 'demo_boolVec_color', text = 'BoolVec_color (expand, toggle)', expand = True, toggle = True)
        layout.separator()
        layout.prop(ps, 'demo_boolVec_xyz',   text = 'BoolVec_xyz (expand)',  expand = True)
        layout.prop(ps, 'demo_boolVec_layer', text = 'BoolVec_layer (size = 32)') #size is set on definition
                
        layout.label('Float ---------------------------------')
        col = layout.column(align = True)
        col.prop(ps, 'demo_float', text = 'Float (default)')
        col.prop(ps, 'demo_float', text = 'Float (icon)', icon = 'BLENDER')
        col.prop(ps, 'demo_float', text = 'Float (no expand)', expand = False)
        col.prop(ps, 'demo_float', text = 'Float (expand)', expand = True)
        col.prop(ps, 'demo_float', text = 'Float (expand, slider, toggle)', expand = True,  slider = True, toggle = True)
        col.separator()
        col.prop(ps, 'demo_float_minMax', text = 'Float_minMax', slider = True)
        col.prop(ps, 'demo_float_softMinMax', text = 'Float_softMinMax', slider = True)
        col.prop(ps, 'demo_float_bothMinMax', text = 'Float(soft_max=100, max=200)', slider = True)
        col.prop(ps, 'demo_float_step16', text = 'Float_step16', slider = True)
        col.prop(ps, 'demo_float_prec6', text = 'Float_precision6', slider = True)
        col.separator()
        col.prop(ps, 'demo_float_factor_length', text = 'Float_factor_length')
        col.prop(ps, 'demo_float_factor_area',  text = 'Float_factor_area')
        col.prop(ps, 'demo_float_factor_volume', text = 'Float_factor_volume')
        col.separator()
        col.prop(ps, 'demo_float_time_none', text = 'Float_time_none')
        col.prop(ps, 'demo_float_time_time', text = 'Float_time_time')
        
        layout.label('FloatVector ---------------------------------')
        layout.prop(ps, 'demo_floatVec',        text = 'FloatVec (default)')
        layout.prop(ps, 'demo_floatVec_size2',  text = 'FloatVec_size2')
        layout.prop(ps, 'demo_floatVec_color',  text = 'FloatVec_matrix', expand = True)
        layout.prop(ps, 'demo_floatVec_trans',  text = 'FloatVec_translation')
        layout.prop(ps, 'demo_floatVec_direct', text = 'FloatVec_direction')
        layout.prop(ps, 'demo_floatVec_velocity', text = 'FloatVec_velocity')
        layout.prop(ps, 'demo_floatVec_accel', text = 'FloatVec_acceleration')
        layout.prop(ps, 'demo_floatVec_matrix', text = 'FloatVec_matrix')
        layout.prop(ps, 'demo_floatVec_euler', text = 'FloatVec_euler')
        layout.prop(ps, 'demo_floatVec_quater', text = 'FloatVec_quaternion')
        layout.prop(ps, 'demo_floatVec_axis', text = 'FloatVec_axisangle')
        layout.prop(ps, 'demo_floatVec_xyz', text = 'FloatVec_xyz')
        layout.prop(ps, 'demo_floatVec_colorGamma', text = 'FloatVec_colorGamma')
        layout.prop(ps, 'demo_floatVec_layer', text = 'FloatVec_layer')

        col = layout.column()
        col.prop(ps, 'demo_floatVec', text = 'FloatVec added to a column')
        col.prop(ps, 'demo_floatVec_direct', text = 'FloatVecDirection added to a column')

        layout.label('Int, IntVector -----------------------------')
        layout.prop(ps, 'demo_int', text = 'Int (default)')
        layout.prop(ps, 'demo_intVec', text = 'IntVec (default)')
        
        layout.label('String ------------------------------------')
        layout.prop(ps, 'demo_string')
        layout.prop(ps, 'demo_string_max5', text = 'String_max5')
        layout.prop(ps, 'demo_string_fpath', text = 'String_filePath')
        layout.prop(ps, 'demo_string_dir', text = 'String_dirPath')
        layout.prop(ps, 'demo_string_fname', text = 'String_fileName')

        layout.label('Enum ------------------------------------')
        layout.label('.prop()')        
        layout.prop(ps, 'demo_enum')
        layout.label('.prop() (expand = True)')        
        layout.prop(ps, 'demo_enum', expand = True)
        
        layout.label('.props_enum()') # careful, this is not .prop_enum() which requires calling for each values
        layout.props_enum(ps, 'demo_enum')
        col = layout.column(align = True)
        col.label('.props_enum() in col.align = True')
        col.props_enum(ps, 'demo_enum')
        layout.label('.prop_menu_enum()')
        layout.prop_menu_enum(ps, 'demo_enum', icon='BLENDER')
        
        col = layout.column(align = True)
        col.label('.prop_enum() x3 in col.align = True')
        col.prop_enum(ps, 'demo_enum', value='ENUM1_ID', icon='PLUGIN')
        col.prop_enum(ps, 'demo_enum', value='ENUM2_ID', icon='PLUGIN')
        col.prop_enum(ps, 'demo_enum', value='ENUM3_ID', icon='PLUGIN')
        
        layout.separator()
        layout.label('multi selectable (EnumProperty(options={"ENUM_FLAG"}))')
        layout.label('.prop() (expand = False)')
        layout.prop(ps, 'demo_enum_multi', expand = False)
        layout.label('.prop() (expand = True)')
        layout.prop(ps, 'demo_enum_multi', expand = True)
        
        layout.separator()
        layout.label('.operator_enum()')
        layout.operator_enum(DoNothingOp.bl_idname, 'my_enum')
        layout.label('.operator_menu_enum()')
        layout.operator_menu_enum(DoNothingOp.bl_idname, 'my_enum')        
        #layout.prop_search(ps, 'demo_string', context.scene.render.layers.active, 'material_override', text="", icon='NONE')

        # complex layout #################
        layout.separator()
        layout.label('##################################')
        layout.label('=== Advanced =========================')
        layout.label('Example1 : Click to open/close---------------')
        ps = context.scene.chichige_ui_demo_props
        box = layout.box()
        row = box.row(align=True)
        row.prop(ps, "demo_bool", text="", emboss=False, icon = ('TRIA_DOWN' if ps.demo_bool else 'TRIA_RIGHT'))
        row.label(text="Custom Openable Panel")
        if ps.demo_bool:
            box.operator(DoNothingOp.bl_idname, text = 'Operator')
            box.operator(DoNothingOp.bl_idname, text = 'Operator')
       
        # more complex one ###############
        layout.separator()
        col = layout.column(align=True)
        col.label('Example2 :----------------------------- ')
        col.label(' Change box count then press Tab like button')
        box = layout.box()
        row = box.split(0.3)
        row.label('Box count')
        row.prop(ps, "demo_advanced_box_num", slider=False, text = "Inc/Dec Box")

        boxNum = ps.demo_advanced_box_num
        if boxNum < 0 or boxNum > 5 :
            boxNum = 0    
        
        boxElems = ps.demo_advanced_box_elements
        for i in range(boxNum):
            subBox = box.box()
            subBox.prop(boxElems[i], 'box_file')
            row = subBox.row()
            row.prop(boxElems[i], 'box_tab', expand=True)
            subBox.label('-----------------------------------------------------------------------------')
            if boxElems[i].box_tab == 'ENUM1_ID':
                col = subBox.column(align = True)
                col.operator(DoNothingOp.bl_idname, text = 'Operator')
                col.operator(DoNothingOp.bl_idname, text = 'Operator')
                col.operator(DoNothingOp.bl_idname, text = 'Operator')
            else:
                row = subBox.row()
                row.scale_y = 3
                row.operator(DoNothingOp.bl_idname, text = 'Operator')
                row.operator(DoNothingOp.bl_idname, text = 'Operator')
                row.operator(DoNothingOp.bl_idname, text = 'Operator')
                
##############################################################################################
##############################################################################################
  
class UIPanelDemo_Misc(bpy.types.Panel):
    """UIPanel Demo Miscellaneous class doc"""
    bl_label = "UIPanel Demo Miscellaneous bl_label"
    bl_idname = "ui_panel_demo_misc"
    
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS' 
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        ps = scene.chichige_ui_demo_props
        
        layout.label('.menu() ---------------------')
        layout.menu("VIEW3D_MT_object")
        layout.menu("VIEW3D_MT_view")
        
        layout.separator()
        layout.label('.prop_search() (all connected to .demo_string) ---------------------') # I couldn't find a way to pass my property to search_property parameter
        col = layout.column(align = True)
        col.prop_search(ps, property = 'demo_string', search_data = bpy.data, search_property= 'actions', text='D.actions')
        col.prop_search(ps, property = 'demo_string', search_data = bpy.data, search_property= 'meshes', text='D.meshes')
        col.prop_search(ps, property = 'demo_string', search_data = bpy.data, search_property= 'groups', text='D.groups')
        col.prop_search(ps, property = 'demo_string', search_data = bpy.data, search_property= 'objects', text='D.objects')
        col.prop_search(ps, property = 'demo_string', search_data = scene, search_property= 'objects', text='scene.objects')
        col.prop_search(ps, property = 'demo_string', search_data = scene, search_property= 'timeline_markers', text='Scene.TLMarkers')
        
        layout.separator()
        layout.label('.prop() against Builtin prop ---------------------')
        layout.prop(context.scene, 'camera')
        layout.prop(context.scene, 'world')
        if context.object:
            layout.prop(context.object, 'active_material')
            layout.prop(context.object, 'scale')
        
        layout.separator()
        layout.label('.template_ID() ---------------------')
        sd = context.space_data
        if sd.background_images:
            bg = context.space_data.background_images[0]
            layout.template_ID(bg, "image", open="image.open")
        else:
            layout.label('    (required background image to show this example)')
        
        if context.object:        
            layout.template_ID(context.object, "active_material", new="material.new")
        else:    
            layout.label('    (required to select object to show this example)')

        layout.separator()
        layout.label('.template_ID_preview() ---------------------')
        spl = layout.split()
        col = spl.column() #this prevents from collapsing format
        col.template_ID_preview(context.tool_settings.image_paint, "brush", new="brush.add", rows=2, cols=6)
        col = spl.column()
        col.template_ID_preview(context.tool_settings.image_paint.brush, "texture", new="texture.new", rows=3, cols=8)

        layout.separator()
        layout.label('.template_header() ---------------------')
        layout.template_header(menus = True)
        layout.template_header(menus = False)
        
        layout.separator()
        layout.label('.template_any_ID(), .template_path_builder() ---------------------')
        ks = scene.keying_sets.active
        ksp  = ks.paths.active if ks else None
        if ksp:
            layout.template_any_ID(ksp, "id", "id_type")
            layout.template_path_builder(ksp, "data_path", ksp.id)
        else:    
            layout.label("    (requires to prepare keying set (and path) to show this example)")
        
        layout.separator()
        layout.label('.template_modifier() ---------------------')
        mods = context.object.modifiers if context.object else None
        if mods and len(mods) > 0:
            layout.template_modifier(mods[0])
        else:       
            layout.label("    (required to add a modifier to show this example)")

        layout.separator()
        layout.label('.template_constrant() ---------------------')
        cons = context.object.constraints if context.object else None
        if cons and len(cons) > 0:
            box = layout.template_constraint(cons[0])
            box.label('Here is returned UILayout')
        else:       
            layout.label("    (required to add a constraint to show this example)")

        layout.separator()
        layout.label('.template_preview() ---------------------')
        if context.object and context.object.active_material:
            #template_preview(id, show_buttons=True, parent=None, slot=None)
            layout.template_preview(context.object.active_material)
        else:       
            layout.label("    (required to add a material to show this example)")

        layout.separator()
        layout.label(".template_curve_mapping('uv_sculpt.brush') ---------------------")
        layout.template_curve_mapping(scene.tool_settings.uv_sculpt.brush, 'curve')
        
        layout.separator()
        layout.label('.template_curve_mapping() ---------------------')
        if bpy.data.lamps and len(bpy.data.lamps) > 0:
            layout.template_curve_mapping(bpy.data.lamps[0], "falloff_curve")        
        else:       
            layout.label("    (required to add a lamp to show this example)")
        
        layout.separator()
        layout.label('.template_color_ramp(expand = True) ---------------------')
        if context.object and context.object.active_material:
            layout.template_color_ramp(context.object.active_material, "diffuse_ramp", expand=True)
        else:       
            layout.label("    (required to add a material to show this example)")

        
        imgEdSpace = None ########### search for ImageEditor Space
        for area in context.window.screen.areas:
            if area.type == 'IMAGE_EDITOR':
                imgEdSpace = area.spaces.active
                break
            
        layout.separator()
        layout.label('.template_histogram() ---------------------')
        if imgEdSpace:
            layout.template_histogram(imgEdSpace, "sample_histogram")
        else:
            layout.label("    (required to ImageEditor is shown in somewhere to show this example)")
        
        layout.separator()
        layout.label('.template_waveform() ---------------------')
        if imgEdSpace:
            layout.template_waveform(imgEdSpace, "scopes")
        else:
            layout.label("    (required to ImageEditor is shown in somewhere to show this example)")
            
        layout.separator()
        layout.label('.template_vectorscope() ---------------------')
        if imgEdSpace:
            layout.template_vectorscope(imgEdSpace, "scopes")
        else:
            layout.label("    (required to ImageEditor is shown in somewhere to show this example)")

        layout.separator()
        layout.label('.template_layers() ---------------------')
        layout.template_layers( scene, "layers", ps, "demo_boolVec", 0)

        layout.separator()
        layout.label('.template_color_picker() ---------------------')
        layout.template_color_picker(scene.world, "ambient_color", value_slider=True)
        #rename template_color_wheel() to template_color_picker()
        #http://lists.blender.org/pipermail/bf-blender-cvs/2012-November/051210.html
        
        layout.separator()
        layout.label('.template_image_layers() ---------------------')
        if imgEdSpace:
            if imgEdSpace.show_render:
                layout.template_image_layers(imgEdSpace.image , imgEdSpace.image_user)
            else:
                layout.label("    (required to RenderResult is shown in ImageEditor to show this example)")
        else:
            layout.label("    (required to ImageEditor is shown in somewhere to show this example)")

        layout.separator()
        layout.label('.template_image() in box() ---------------------')
        if imgEdSpace:
            box = layout.box()
            box.template_image(imgEdSpace, 'image', imgEdSpace.image_user, compact=False)
        else:
            layout.label("    (required to ImageEditor is shown in somewhere to show this example)")

        layout.separator()
        layout.label('.template_image_settings() in box()---------------------')
        layout.box().template_image_settings(scene.render.image_settings, color_management=True)

        clipEdSpace = None ########### search for ClipEditor Space
        for area in context.window.screen.areas:
            if area.type == 'CLIP_EDITOR':
                clipEdSpace = area.spaces.active
                break
        layout.separator()
        layout.label('.template_movieclip()---------------------')
        if clipEdSpace:
            layout.template_movieclip(clipEdSpace, 'clip', compact = False)
        else:
            layout.label("    (required to ClipEditor is shown in somewhere to show this example)")
        
        layout.separator()
        layout.label('.template_track()---------------------')
        if clipEdSpace:
            layout.template_track(clipEdSpace, 'scopes')
        else:
            layout.label("    (required to ClipEditor is shown in somewhere to show this example)")
    
        layout.separator()
        layout.label('.template_marker()---------------------')
        if clipEdSpace and clipEdSpace.clip and clipEdSpace.clip.tracking.tracks.active:
            layout.template_marker(clipEdSpace, "clip", clipEdSpace.clip_user, clipEdSpace.clip.tracking.tracks.active, compact=True)
        else:
            layout.label("    (required to set up a track in ClipEditor to show this example)")

        layout.separator()
        layout.label('.template_list()---------------------')
        if clipEdSpace and clipEdSpace.clip:
            layout.template_list("CLIP_UL_tracking_objects", "", clipEdSpace.clip.tracking, "objects", 
                              clipEdSpace.clip.tracking, "active_object_index", rows=3)        
        else:
            layout.label("    (required to set up a clip in ClipEditor to show this example)")
        
        layout.separator()
        layout.label('.template_running_jobs() ---------------------')
        layout.template_running_jobs()
        
        layout.separator()
        layout.label('.template_operator_search() ---------------------')        
        layout.template_operator_search()
        
        layout.separator()
        layout.label('.template_header_3D() in row() ---------------------')
        row = layout.row()
        row.template_header_3D()
        
        layout.separator()
        layout.label('.template_edit_mode_selection() ---------------------')
        layout.template_edit_mode_selection()
        
        col = layout.column(align = True)
        col.separator()
        col.label('.template_reports_banner() ---------------------')
        col.template_reports_banner()
        col.operator(DoNothingOp.bl_idname, text='Press to show a report on above')
             
        layout.separator()
        layout.label('.template_node_link()---------------------')
        if scene.use_nodes and scene.node_tree.nodes.active and len(scene.node_tree.nodes.active.inputs) > 0:
            layout.template_node_link(scene.node_tree, scene.node_tree.nodes.active, scene.node_tree.nodes.active.inputs[0])
        else:
            layout.label("    (required a Node that has input socket to be active in somewhere to show this example)")
        
        layout.separator()
        layout.label('.template_node_view()---------------------')
        if scene.use_nodes and scene.node_tree.nodes.active and len(scene.node_tree.nodes.active.inputs) > 0:
            layout.template_node_view(scene.node_tree, scene.node_tree.nodes.active, scene.node_tree.nodes.active.inputs[0])
        else:
            layout.label("    (required a Node that has input socket to be active in somewhere to show this example)")

        layout.separator()
        layout.label('.template_texture_user() ---------------------')
        layout.template_texture_user() # Seems not work. 
        # Probably this is a menu shown at top of TexturePanel of PopertiesWindow when Other icon (not world, material) is toggled. ('Brush' is selected for the menu at default)
        
        layout.label('.template_keymap_item_properties() ---------------------')
        kms = context.window_manager.keyconfigs[2].keymaps
        layout.template_keymap_item_properties(kms[8].keymap_items[0])# I don't know what key affected by this keymap
        layout.template_keymap_item_properties(kms[14].keymap_items[0])
        
        layout.label('.introspect() -----------------------------')
        temp = layout.introspect()
        layout.label("    .introspect() : returned String's len() is " + str(len(temp)))
        #print(temp) 
        
            
        layout.separator()
        layout.label('.template_colorspace_settings() -----------------------------')        
        if imgEdSpace and imgEdSpace.image:
            layout.template_colorspace_settings(imgEdSpace.image, 'colorspace_settings')
        else:
            layout.label("    (required to ImageEditor is shown in somewhere to show this example)")
        
        layout.separator()
        layout.label('.colormanaged_view_settings() -----------------------------')
        layout.template_colormanaged_view_settings(scene, "view_settings")
        
        #layout.context_pointer_set()
        #http://blenderartists.org/forum/showthread.php?283720-What-is-context_pointer_set
  


##############################################################################################
##############################################################################################


# Registration---------------------------------------------
def register():
    
    bpy.utils.register_class(DoNothingOp)    
    bpy.utils.register_class(UIPanelDemo_Layout)
    bpy.utils.register_class(UIPanelDemo_Props)
    bpy.utils.register_class(UIPanelDemo_Misc)

def unregister():
    bpy.utils.unregister_class(DoNothingOp)
    bpy.utils.unregister_class(UIPanelDemo_Layout)
    bpy.utils.unregister_class(UIPanelDemo_Props)
    bpy.utils.unregister_class(UIPanelDemo_Misc)
    
if __name__ == "__main__":
    register()
