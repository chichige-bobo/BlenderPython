bl_info = {
    "name": "Addon Template Generator",
    "author": "chichige-bobo",
    "version": (1, 0, 1),
    "blender": (2, 80, 0),
    "location": "TextEditor > Templates > AddonTemplateGenerator, TextEditor > PropertiesBar > AddSnippet",
    "description": "Generate empty addon template. Add snippet of propertes and samples",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Development"}

# LET USERS TO MANIPULATE AFTER GENERATED, NOT COMPLETE AT DIALOG
import bpy
from bpy.props import *

#####################################################################################

def getMajorSpaceRegionItems(self, context):
    items = [('VIEW_3D-TOOLS',     '3DView-Tools',     'Toolbar of 3DView',       'VIEW3D', 0),
             ('VIEW_3D-TOOLPROPS', '3DView-ToolProps', 'Below Toolbar of 3DView', 'VIEW3D', 1),
             ('VIEW_3D-UI',        '3DView-UI',        'PropertyBar of 3DView',   'VIEW3D', 2),
             ('PROPERTIES-WINDOW-render',       'Props-Window-Render',      '', 'SCENE', 3),
             ('PROPERTIES-WINDOW-render_layer', 'Props-Window-RenderLayer', '', 'RENDERLAYERS', 4),
             ('PROPERTIES-WINDOW-scene',        'Props-Window-Scene',       '', 'SCENE_DATA', 5),
             ('PROPERTIES-WINDOW-world',        'Props-Window-World',       '', 'WORLD_DATA', 6),
             ('PROPERTIES-WINDOW-object',       'Props-Window-Object',      '', 'OBJECT_DATA', 7),
             ('PROPERTIES-WINDOW-constraint',   'Props-Window-Constraint',  '', 'CONSTRAINT', 8),
             ('PROPERTIES-WINDOW-modifier',     'Props-Window-Modifier',    '', 'MODIFIER', 9),
             ('PROPERTIES-WINDOW-data',         'Props-Window-Data',        '', 'MESH_DATA', 10),
             ('PROPERTIES-WINDOW-material',     'Props-Window-Material',    '', 'MATERIAL', 11),
             ('PROPERTIES-WINDOW-texture',      'Props-Window-Texture',     '', 'TEXTURE', 12)]
    return items
    
###############################################################################################
class AddonTemplateGeneratorOp(bpy.types.Operator):
    """Create empty addon template at once"""
    bl_idname = "chichige.addon_template_generator_operator"
    bl_label = "Addon Template Generator"
    bl_options = {'PRESET', 'INTERNAL'}
    
    # name for label, desc for tooltip in Operator Panel
    # options = Enumerator in ['HIDDEN', 'SKIP_SAVE', 'ANIMATABLE', 'LIBRARY_EDITABLE'] (and 'ENUM_FLAG' for EnumProp)
    
    p_name = StringProperty(name = "Overall Name", description="Used for various places", default="Hello World")
    p_opOptions = EnumProperty(items = [('REGISTER', 'Register', 'Display in the info window and support the redo toolbar panel.'), 
                                        ('UNDO',     'Undo', 'Push an undo event (needed for operator redo)'),
                                        ('BLOCKING', 'Blocking', 'Block anything else from using the cursor'),
                                        ('MACRO',    'Macro', 'Use to check if an operator is a macro'),
                                        ('GRAB_POINTER', 'GrabPointer', 'Use so the operator grabs the mouse focus, enables wrapping when continuous grab is enabled'),
                                        ('PRESET', 'Preset', 'Display a preset button with the operators settings'),
                                        ('INTERNAL', 'Internal', 'Removes the operator from search results')],
                              name="bl_options", 
                              description="bl_options for this operator", 
                              default={'REGISTER'}, 
                              options = {'ENUM_FLAG'})
    
    isUseOpProps: BoolProperty(name='Add Operator Properties', description = "Add a set of properties for this operator", default = False )

    isUsePanel: BoolProperty(name='Add Panel Class', description = "Whether use Panel class.", default = True)
    p_panelOptions: EnumProperty(items = [('DEFAULT_CLOSED', 'DefaultClosed', 'Defines if the panel has to be open or collapsed at the time of its creation'), 
                                           ('HIDE_HEADER', 'HideHeader', 'If set to False, the panel shows a header, which contains a clickable arrow to collapse the panel and the label')],
                                  name="PanelOptions",
                                  description="bl_options for this Panel",
                                  default = set(),
                                  options = {'ENUM_FLAG'})
    
    p_panelSpaceRegion: EnumProperty(items = getMajorSpaceRegionItems ,
                                      name="SpaceRegionType", 
                                      description="Panel's bl_space_type, bl_region_type and bl_context")                                

    isUseMenu: BoolProperty(name='Add Menu Class', description = "Whether use Menu class.", default = False)

    isUseGPLNotice:  BoolProperty(name = 'Add GPL Notification', default = False)
    isUseSceneProps: BoolProperty(name = 'Add Scene Properties', default = False )
    isUseMenuFunc:   BoolProperty(name = 'Add Menu Function', default = False)
    isUseKeymap:     BoolProperty(name = 'Add Keymapping', default = False )
    
    #=AddonTempGen execute=======================================
    def execute(self, context):
        txt = ""
        txt += "" if not self.isUseGPLNotice else txt_GPL
        txt += txt_blInfo % (self.p_name)

        #-----
        txt += "import bpy\n"
        if self.isUseOpProps or self.isUseSceneProps:
            txt += "from bpy.props import BoolProperty, BoolVectorProperty, FloatProperty, FloatVectorProperty, IntProperty, IntVectorProperty, EnumProperty, StringProperty, PointerProperty\n"
        txt += "\n"
        
        #-----operator               
        txt_name = self.p_name.strip()#re.sub('[\W]', '_', txt_name)
        txt_name = txt_name if txt_name != '' else 'Hello World'
        txt_className = txt_name.replace(" ", "") + "Operator" 
        txt_blIdname = 'addongen.' + txt_name.replace(" ", "_").lower() + '_operator'
        txt_blLabel = txt_name + " Operator"
        context.scene.chichige_add_snippet_props.overallName = txt_name
        
        txt_blOptions = ""
        if len(self.p_opOptions) > 0:
            temp = list(self.p_opOptions)[::-1] #I want 'REGISTER' to be first.
            for t in temp:
                txt_blOptions += "," if txt_blOptions != "" else ""
                txt_blOptions += "'%s'" % t
            txt_blOptions = "    bl_options = {%s}\n\n" % txt_blOptions
        
        temp = "" if not self.isUseOpProps else txt_props
        txt += txt_operator % (txt_className, '"ToolTip of ' + txt_className + '"', txt_blIdname, txt_blLabel, txt_blOptions, temp)
        
        #---
        if self.p_panelSpaceRegion.startswith("PROP"):
            ctgrConv = self.p_panelSpaceRegion.split("-")[2].replace("_", "").upper()
        else:
            ctgrConv = self.p_panelSpaceRegion.split("-")[0].replace("_", "")
        
        
        #-----panel
        txt_className_p = txt_name.replace(" ", "") + "Panel"
        if self.p_panelSpaceRegion.startswith("PROP"):
            ctgrConv = self.p_panelSpaceRegion.split("-")[2].replace("_", "").upper()
        else:
            ctgrConv = self.p_panelSpaceRegion.split("-")[0].replace("_", "")
        txt_blIdname_p = ctgrConv + '_PT_' + txt_name.replace(" ", "_").lower()
        txt_blLabel_p = txt_name + " Panel"
        
        txt_blOptions_p = ""
        temp = list(self.p_panelOptions) #p_panelOptions.pop() not worked well.(returned one value multiple times)
        for i in range(len(temp)):
            txt_blOptions_p += "" if i == 0 else ", "
            txt_blOptions_p += "'%s'" % temp[i]
        if txt_blOptions_p != "":
            txt_blOptions_p = "bl_options = {" + txt_blOptions_p + "}\n"
                        
        temp = self.p_panelSpaceRegion.split("-")
        txt_space_p = "bl_space_type = '%s'\n" % temp[0]
        txt_region_p = "    bl_region_type = '%s'" % temp[1]
        txt_context_p = "" if len(temp) < 3 else "\n    bl_context = '%s'" % temp[2]
        txt_category_p = "" if self.p_panelSpaceRegion != 'VIEW_3D-TOOLS' else "\n    bl_category = 'Tools'"
        txt += "" if not self.isUsePanel else txt_panel % (txt_className_p, '"Docstring of ' + txt_className_p + '"', 
                                                            txt_blIdname_p, txt_blLabel_p, txt_blOptions_p, 
                                                            txt_space_p + txt_region_p + txt_context_p + txt_category_p,
                                                            txt_className, txt_name)
        
        #-----menu
        txt_className_m = txt_name.replace(" ", "") + "Menu"
        txt_blIdname_m = ctgrConv + '_MT_' + txt_name.replace(" ", "_").lower()
        txt_blLabel_m = txt_name + " Menu"
        txt += "" if not self.isUseMenu else txt_menu % (txt_className_m, txt_blIdname_m, txt_blLabel_m, txt_className)
        
        
        #-----
        if self.isUseSceneProps:
            txt += ("class %sProps(bpy.types.PropertyGroup):\n" % txt_name.replace(" ", "")) + txt_props + "\n"
           
        #-----
        if self.isUseMenuFunc:
            txt += "def menu_func(self, context):\n"
            txt += "    self.layout.operator(%s.bl_idname, icon = 'PLUGIN')\n\n" % txt_className
        
        #-----
        temp1 = ""
        temp2 = ""
        if self.isUseSceneProps:
            temp1 += "bpy.utils.register_class(%sProps)\n" % txt_name.replace(" ", "") 
            temp1 += "    bpy.types.Scene.%s_props = PointerProperty(type = %sProps)\n\n" % ("addongen_" + txt_name.replace(" ", "_").lower(), txt_name.replace(" ", ""))
            temp1 += "    "
            temp2 += "bpy.utils.unregister_class(%sProps)\n" % txt_name.replace(" ", "")
            temp2 += "    #del bpy.types.Scene.%s_props\n\n" % ("addongen_" + txt_name.replace(" ", "_").lower())
            temp2 += "    "
            
        temp1 += "bpy.utils.register_class(%s)" % txt_className
        temp1 += "" if not self.isUsePanel else "\n    bpy.utils.register_class(%s)" % txt_className_p
        temp1 += "" if not self.isUseMenu else "\n    bpy.utils.register_class(%s)" % txt_className_m
        temp1 += "" if not self.isUseMenuFunc else "\n    bpy.types.VIEW3D_MT_object.append(menu_func)"
        temp2 += "bpy.utils.unregister_class(%s)" % txt_className
        temp2 += "" if not self.isUsePanel else "\n    bpy.utils.unregister_class(%s)" % txt_className_p
        temp2 += "" if not self.isUseMenu else "\n    bpy.utils.unregister_class(%s)" % txt_className_m
        temp2 += "" if not self.isUseMenuFunc else "\n    bpy.types.VIEW3D_MT_object.remove(menu_func)"
        if not self.isUseKeymap:
            txt += txt_reg % (temp1, temp2)
        else:
            if self.isUseMenu:
                txt += txt_reg_keymap % (temp1, '"wm.call_menu"', "kmi.properties.name = %s.bl_idname" % txt_className_m, temp2)
            else:
                #txt_reg_keymap % (bpy.utils.register(), keymap_items.new(%s,,,,) ,assign prop to kmi, bpy.utils.unregister())    
                txt += txt_reg_keymap % (temp1, txt_className + ".bl_idname", "#kmi.properties.prop1 = 'some'", temp2)
        
        #-----
        textObj = bpy.data.texts.new(txt_name.replace(" ", "_") + ".py")
        textObj.write(txt)
        context.space_data.text = textObj
        self.report({'INFO'}, "'%s' was created." % textObj.name)
        return {'FINISHED'}
        
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width = 400, height=500) # returns {'RUNNING_MODAL'} and calls execute() when 'OK' button is pressed
    
    #= AddonTempGen draw =================            
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.alignment = 'CENTER'
        row.label(text='(Some options can be multi-selected with Shift-Click)')
        
        layout.separator()
        layout.prop(self, 'p_name')
        row = layout.row(align = True)
        #row.alignment = 'CENTER'
        col = row.column(align = True)
        col.label(text="            When above name is 'Hello World'...")
        col.label(text="                ClassName = 'HellowWorldOperator'")
        col.label(text="                bl_idname = 'addongen.hello_world_operator'")
        
        layout.label(text='Operator ' + ('-' * 110))
        split = layout.split(factor=0.2)
        col_L = split.column()
        col_L.alignment = 'RIGHT'
        col_L.label(text='bl_options')
        col_L.label(text='Use Op Props')
        col_R = split.column()
        col_R.row().prop(self, 'p_opOptions')
        col_R.prop(self, 'isUseOpProps')
        
        layout.separator()
        layout.label(text='Panel ' + ('-' * 116))
        split = layout.split(factor=0.2)
        col_L = split.column()
        col_L.alignment = 'RIGHT'
        col_L.label(text='Use Panel')
        col_L.label(text='Place')
        col_L.label(text='')
        col_L.label(text='bl_options') 
        col_R = split.column()
        col_R.prop(self, 'isUsePanel')
        col_R.prop(self, 'p_panelSpaceRegion', text = '')
        col_R.label(text='(Full list is in props panel. Replace with after completion.)')
        row = col_R.split(factor=0.6).row().prop(self, 'p_panelOptions')

        layout.separator()
        layout.label(text='Menu ' + ('-' * 116))
        split = layout.split(factor=0.2)
        split.alignment = 'RIGHT'
        split.label(text='Use Menu')
        #split = split.row()
        split.prop(self, 'isUseMenu')
    
        layout.separator()
        layout.label(text='Misc ' + ('-' * 116))
        split = layout.split(factor=0.2)
        col_L = split.column()
        col_L.alignment = 'RIGHT'
        col_L.label(text='GPL Notice')
        col_L.label(text='Scene Props')
        col_L.label(text='Menu Func')
        col_L.label(text='Keymap')
        col_R = split.column()
        col_R.prop(self, 'isUseGPLNotice')
        col_R.prop(self, 'isUseSceneProps')
        col_R.prop(self, 'isUseMenuFunc')
        col_R.prop(self, 'isUseKeymap')
        #---
        layout.separator()
    
        
        
####################################################################################
class AddSnippetOp_Props(bpy.types.Operator):
    """Add a property to current cursor position"""
    bl_idname = "chichige.add_snippet_operator_props"
    bl_label = "Add Snippet Operator - Props"
    bl_options = {'INTERNAL', 'UNDO'}
    
    type: StringProperty(name="OperationType")
    
    #Added step of IntVec, unit of FloatVec                           
    refDic = {'Bool'        : "(%s, default=False, options={'ANIMATABLE'}, subtype='NONE', update=None, get=None, set=None)",
              'BoolVector'  : "(%s, default=(False, False, False), options={'ANIMATABLE'}, subtype='NONE', size=3, update=None, get=None, set=None)",
              'Int'         : "(%s, default=0, min=-sys.maxint, max=sys.maxint, soft_min=-sys.maxint, soft_max=sys.maxint, step=1, options={'ANIMATABLE'}, subtype='NONE', update=None, get=None, set=None)",
              'IntVector'   : "(%s, default=(0, 0, 0), min=-sys.maxint, max=sys.maxint, soft_min=-sys.maxint, soft_max=sys.maxint, step=1, options={'ANIMATABLE'}, subtype='NONE', size=3, update=None, get=None, set=None)",
              'Float'       : "(%s, default=0.0, min=sys.float_info.min, max=sys.float_info.max, soft_min=sys.float_info.min, soft_max=sys.float_info.max, step=3, precision=2, options={'ANIMATABLE'}, subtype='NONE', unit='NONE', update=None, get=None, set=None)",
              'FloatVector' : "(%s, default=(0.0, 0.0, 0.0), min=sys.float_info.min, max=sys.float_info.max, soft_min=sys.float_info.min, soft_max=sys.float_info.max, step=3, precision=2, options={'ANIMATABLE'}, subtype='NONE', unit='NONE', size=3, update=None, get=None, set=None)",
              'String'      : "(%s, %s, maxlen=0, options={'ANIMATABLE'}, subtype='NONE', update=None, get=None, set=None)",
              'Enum'        : "(items, %s, %s, options={'ANIMATABLE'}, update=None, get=None, set=None)",
              'Collection'  : "(items, %s, options={'ANIMATABLE'})",
              'Pointer'     : "(%s, options={'ANIMATABLE'}, update=None)"}
    defaultDic = {'Bool' : "False", 'BoolVector' : "(False, False, False)", 'Int' : "0", 'IntVector' : "(0, 0, 0)", 'Float' : "0.0", 'FloatVector' : "(0.0, 0.0, 0.0)", 'String' : '""', 'Enum': '""'} 
              
    def execute(self, context):
        pps = context.scene.chichige_add_snippet_props
        
        if self.type.startswith("CHECK"):
            self.changeCheckState(context)
            return {'FINISHED'}
                   
        txt = ""
        refNameDesc = 'name="", description=""'
        if pps.isAddRefComment:
            txt = "#%sProperty" % self.type 
            if self.type == 'String' or self.type == 'Enum':
                txt += self.refDic[self.type] % (refNameDesc, 'default=""')
            elif self.type == 'Collection' or self.type == 'Pointer':
                txt += self.refDic[self.type] % ('type = "", description = ""') 
            else:
                txt += self.refDic[self.type] % refNameDesc
            txt+= "\n"
                
        txt += ("" if not pps.isAddPrefix else "bpy.props.") + self.type + "Property("
        
        subText = ""
        if self.type == 'Enum':
            subText = "items = [('ENUM1', 'Enum1', 'Enum1Desc'), ('ENUM2', '', '')]"
        elif self.type == 'Collection' or self.type == 'Pointer':
            subText = "type = ClassName"
        
        subText += "" if not pps.isAddName else (", " if subText else "") + 'name = ""'
        subText += "" if not pps.isAddDesc else (", " if subText else "") + 'description = ""'
    
        if self.type != 'Collection' and self.type != 'Pointer':
            subText += "" if not pps.isAddDefault else (", " if subText else "") + 'default = ' + self.defaultDic[self.type]
            
        isInt = self.type.startswith("Int")
        if isInt or self.type.startswith("Float"):
            if pps.isAddMinMax:
                (minStr, maxStr) = ("-sys.minint", "sys.maxint") if self.type.startswith("Int") else ("sys.float_info.min", "sys.float_info.max")
                subText += (", " if subText else "") + "min = %s, max = %s" % (minStr, maxStr)
            if pps.isAddSoftMinMax:
                (minStr, maxStr) = ("-sys.minint", "sys.maxint") if isInt else ("sys.float_info.min", "sys.float_info.max")
                subText += (", " if subText else "") + "soft_min = %s, soft_max = %s" % (minStr, maxStr)
            if pps.isAddStep:
                subText += (", " if subText else "") + "step = " + ("1" if isInt else "3")
            if not isInt:
                subText += "" if not pps.isAddFloatPrec else (", " if subText else "") + "precision = 2"
                subText += "" if pps.floatUnit == 'NO' else (", " if subText else "") + "unit = '%s'" % pps.floatUnit
        
        if self.type == 'Enum' and pps.isAddEnumFlag:
            temp = pps.propOptions.copy()
            temp.add('ENUM_FLAG')
            subText += (", " if subText else "") + 'options = %s' % str(temp)
        else:
            subText += "" if not pps.propOptions else (", " if subText else "") + 'options = %s' % str(pps.propOptions)
        
        if self.type != 'Enum' and self.type != 'Collection' and self.type != 'Pointer' :
            if self.type != 'String':
                if self.type.endswith("Vector"):
                    subText += "" if pps.propVecSubtype == 'NO'   else (", " if subText else "") + "subtype = '%s'" % pps.propVecSubtype 
                else:
                    subText += "" if pps.propSubtype == 'NO'   else (", " if subText else "") + "subtype = '%s'" % pps.propSubtype 
            else:                
                subText += "" if pps.stringSubtype == 'NO'   else (", " if subText else "") + "subtype = '%s'" % pps.stringSubtype
                
            if self.type.endswith("Vector"):
                subText += "" if not pps.isAddSize else (", " if subText else "") + "size = 3"
                
        if self.type != 'Collection':
            subText += "" if not pps.isAddUpdate else (", " if subText else "") + 'update = None'
                
        txt += subText + ")\n"
        
        if pps.isClipboard:
            context.window_manager.clipboard = txt
            self.report({'INFO'}, "Property was copied to Clipboard.")
        else:    
            sd = context.space_data
            if not sd.text:
                sd.text = bpy.data.texts.new('SnippetText')
            sd.text.write(txt)
            self.report({'INFO'}, "Property insertion was done.")

        return {'FINISHED'}
    
  
    def changeCheckState(self, context):
        pps = context.scene.chichige_add_snippet_props
        if self.type == "CHECK_CLEAR":
            pps.isAddRefComment = pps.isAddPrefix = pps.isAddName = pps.isAddDesc = pps.isAddDefault = False
            pps.isAddMinMax = pps.isAddSoftMinMax =  pps.isAddStep = pps.isAddSize = pps.isAddUpdate = False
            pps.propOptions = set()# I don't know if this is correct way
            pps.propSubtype =  pps.propVecSubtype = pps.floatUnit = pps.stringSubtype =  'NO'
            pps.isAddFloatPrec = pps.isAddEnumFlag =  False
        
        elif self.type == "CHECK_DEFAULT":
            pps.isAddPrefix = pps.isAddName = pps.isAddDesc = pps.isAddDefault = pps.isAddMinMax = True
            pps.isAddRefComment = pps.isAddSoftMinMax =  pps.isAddStep = pps.isAddSize = pps.isAddUpdate = False
            pps.propOptions = set()
            pps.propSubtype =  pps.propVecSubtype = pps.floatUnit = pps.stringSubtype =  'NO'
            pps.isAddFloatPrec = pps.isAddEnumFlag =  False

        elif self.type == "CHECK_ALL":
            pps.isAddRefComment = pps.isAddPrefix = pps.isAddName = pps.isAddDesc = pps.isAddDefault = True
            pps.isAddMinMax = pps.isAddSoftMinMax =  pps.isAddStep = pps.isAddSize = pps.isAddUpdate = True
            pps.propOptions = {'ANIMATABLE'}
            pps.propSubtype =  pps.propVecSubtype = pps.floatUnit = pps.stringSubtype =  'NONE'
            pps.isAddFloatPrec = pps.isAddEnumFlag =  True
        
        
####################################################################################        
class AddSnippetOp_Samples(bpy.types.Operator):
    """Add sample code to current cursor position"""
    bl_idname = "chichige.add_snippet_operator_samples"
    bl_label = "Add Snippet Operator - Samples"
    bl_options = {'INTERNAL', 'UNDO'}
    
    type: EnumProperty(items = [('PanelPlace', 'PanelPlace', 'Insert/Copy selected place'),
                                 ('AddonParts', 'AddonParts', 'Insert/Copy selected addon parts'), 
                                 ('HintSnippets', 'HintSnippets', 'Insert/Copy selected hint'),
                                 ('UILayoutMembers', 'UILayoutMembers', 'Insert/Copy selected member'),
                                 ('INEFFECTIVE', 'INEFFECTIVE', 'Separator selected. Do nothing.'),
                                 ('Keymap', 'Keymap', 'Insert/Copy keymap combination.'),
                                 ('CheckKeymapConflicts', 'CheckKeymapConflicts', 'Check conflicts then print to console')])
    
    uiLayoutParamDic = {'active':               'active = False', 
                        'alert' :               'alert = False',
                        'alignment':            "alignment = 'EXPAND' #enum in ['EXPAND', 'LEFT', 'CENTER', 'RIGHT']",
                        'enabled':              'enabled = False',
                        'operator_context':     "operator_context = 'INVOKE_DEFAULT' #enum in ['INVOKE_DEFAULT', 'INVOKE_REGION_WIN', 'INVOKE_REGION_CHANNELS', 'INVOKE_REGION_PREVIEW', 'INVOKE_AREA', 'INVOKE_SCREEN', 'EXEC_DEFAULT', 'EXEC_REGION_WIN', 'EXEC_REGION_CHANNELS', 'EXEC_REGION_PREVIEW', 'EXEC_AREA', 'EXEC_SCREEN']",
                        'scale_x':              'scale_x = 0.0', 
                        'scale_y':              'scale_y = 0.0',
                        'row()':                'row(align = False)', 
                        'column()':             'column(align = False)', 
                        'column_flow()':        'column_flow(columns = 0, align = False)',
                        'box()':                'box()', 
                        'split()':              'split(percentage = 0.0, align = False)', 
                        'prop()':               'prop(data, property, text = "", text_ctxt = "", translate = True, icon = %s, expand = False, slider = False, toggle = False, icon_only = False, event = False, full_event = False, emboss = True, index = -1)' % "'NONE'",
                        'props_enum()':         'props_enum(data, property)',
                        'prop_menu_enum()':     'prop_menu_enum(data, property, text = "", text_ctxt = "", translate = True, icon = %s)' % "'NONE'", 
                        'prop_enum()':          'prop_enum(data, property, value, text = "", text_ctxt = "", translate = True, icon = %s)' % "'NONE'", 
                        'prop_search()':        'prop_search(data, property, search_data, search_property, text = "", text_ctxt = "", translate = True, icon = %s)' % "'NONE'", 
                        'operator()':           'operator(operator, text = "", text_ctxt = "", translate = True, icon = %s, emboss = True)' % "'NONE'", 
                        'operator_enum()':      'operator_enum(operator, property)', 
                        'operator_menu_enum()': 'operator_menu_enum(operator, property, text = "", text_ctxt = "", translate = True, icon = %s)' % "'NONE'", 
                        'label()':              'label(text="", text_ctxt="", translate=True, icon=%s, icon_value=0)' % "'NONE'", 
                        'menu()':               'menu(menu, text = "", text_ctxt = "", translate = True, icon = %s)' % "'NONE'", 
                        'separator()':          'separator()'}
    
    def execute(self, context):
        pps = context.scene.chichige_add_snippet_props
        
        if self.type == 'PanelPlace':
            txt = self.getPanelPlace(context)
        elif self.type == 'AddonParts':
            txt = self.getAddonParts(context)
        elif self.type == 'HintSnippets':
            txt = globals()["txt_hint_%s" % pps.hintSnippets] #in my experiment, global() doesn't contain another addon's
        elif self.type == 'UILayoutMembers':
            txt = self.getUILayoutMembers(context)
        elif self.type == 'INEFFECTIVE':
            return {'CANCELLED'}
        elif self.type == 'Keymap':
            txt = self.getKeymap(context)
        elif self.type == 'CheckKeymapConflicts':
            self.checkKeymapConflicts(context)
            return {'FINISHED'}       
        
        if pps.isClipboard:
            context.window_manager.clipboard = txt
            self.report({'INFO'}, "Sample code was copied to Clipboard.")
        else:
            sd = context.space_data
            if not sd.text:
                sd.text = bpy.data.texts.new('SnippetText')
            sd.text.write(txt)
            self.report({'INFO'}, "Sample code insertion was done.")
            
        return {'FINISHED'}
      

    #---- 
    def getPanelPlace(self, context):
        pps = context.scene.chichige_add_snippet_props
                
        # below is True only when called when "CodeSamples > PanelClass"
        # because 'SEPARATOR' is blocked in PanelPlace section by ".enabled = False".
        if pps.panelSpace.startswith('SEPA'):
            return "bl_space_type = 'VIEW_3D'\n    bl_region_type = 'TOOLS'\n"
        
        txt = ""
        txt_space = "bl_space_type = '%s'" % pps.panelSpace
        if pps.panelSpace == 'VIEW_3D' or pps.panelSpace == 'CLIP_EDITOR':
            txt_region = pps.panelRegion_view3d_clip
        elif pps.panelSpace == 'PROPERTIES' or pps.panelSpace == 'USER_PREFERENCES':
            txt_region = 'WINDOW'
        elif pps.panelSpace == 'FILE_BROWSER':
            txt_region = 'CHANNELS'
        elif pps.panelSpace == 'IMAGE_EDITOR' or pps.panelSpace == 'NODE_EDITOR':
            txt_region = pps.panelRegion_image_node
        else:
            txt_region = 'UI'
        txt_region = "bl_region_type = '%s'" % txt_region
        
        txt_context = ""
        txt_category = ""
        if pps.panelSpace == 'VIEW_3D':
            if pps.panelContext_view3d != 'NO':
                txt_context = "bl_context = '%s'" % pps.panelContext_view3d
            
            if pps.panelRegion_view3d_clip == 'TOOLS':
                if pps.panelContext_view3d == 'objectmode':
                    txt_category = pps.panelCategory_objectmode
                elif pps.panelContext_view3d == 'mesh_edit':
                    txt_category = pps.panelCategory_editmode
                else:
                    txt_category = pps.panelCategory_others
                
                if txt_category == 'NO':
                    txt_category = "" 
                else:
                    txt_category = "bl_category = '%s'" % txt_category                  
        
        elif pps.panelSpace == 'IMAGE_EDITOR' and pps.panelRegion_image_node == 'TOOLS':
            if pps.panelCategory_imageeditor != 'NO':
                txt_category = "bl_category = '%s'" % pps.panelCategory_imageeditor
                
        elif pps.panelSpace == 'PROPERTIES':
            txt_context = "bl_context = '%s'" % pps.panelContext_properties
        
        txt += "    %s\n    %s\n    " % (txt_space, txt_region)
        txt += "" if not txt_context else ("%s\n    " % txt_context)
        txt += "" if not txt_category else ("%s\n    " % txt_category)
         
        return txt
    
    #-----
    def getAddonParts(self, context):
        pps = context.scene.chichige_add_snippet_props
        
        txt_name = pps.overallName.strip()#re.sub('[\W]', '_', txt_name)
        txt_name = txt_name if txt_name != '' else 'Hello World'
        txt_name_class = txt_name.replace(" ", "") 
        txt_name_id = txt_name.replace(" ", "_").lower()

        txt = ""
        if pps.addonParts == "OperatorClass":
            #txt_operator % (className, "ToolTip", bl_idname, bl_label, \t(bl_options)\n\n, (props)) 
            txt = txt_operator % (txt_name_class + "Operator", '"ToolTip of %sOperator"' % txt_name_class, "addongen.%s_operator" % txt_name_id, "%s Operator" % txt_name, "    bl_options = {'REGISTER'}\n\n", "")
            
        elif pps.addonParts  == "PanelClass":
            if pps.panelSpace.startswith("SEPA"):
                temp = 'VIEW3D'
            elif pps.panelSpace == "PROPERTIES":
                temp = pps.panelContext_properties.replace("_", "").upper()
            else:
                temp = pps.panelSpace.replace("_", "")
            txt_blIdname_p = temp + '_PT_%s_panel' % txt_name_id
            txt_blOptions_p = "#bl_options =  {'DEFAULT_CLOSED'}\n"
            
            txt_panelPlace = self.getPanelPlace(context)[4:]
            #txt_panel % (ClassName, "ToolTip", bl_idname, bl_label, SpaceRegion, bl_context, OperatorClassName, ButtonLabel)                    
            txt = txt_panel % (txt_name_class + "Panel", '"Docstring of %sPanel"' % txt_name_class, txt_blIdname_p, txt_name + " Panel", txt_blOptions_p, txt_panelPlace, txt_name_class + "Operator", txt_name)
        
        elif pps.addonParts  == "MenuClass":
            #txt_menu % (ClassName, bl_idname, bl_label, OperatorClassName)
            txt = txt_menu % (txt_name_class + "Menu", "VIEW3D_MT_" + txt_name_id,  txt_name + " Menu", txt_name_class + "Operator")
        
        elif pps.addonParts  == "Props(Operator)":
            txt = txt_props
        
        elif pps.addonParts  == "PropGroup":
            txt = ("class %sProps(bpy.types.PropertyGroup):\n" % txt_name_class) + txt_props
            txt += "bpy.utils.register_class(%sProps)\n" % txt_name_class
            txt += "bpy.types.Scene.addongen_%s_props = PointerProperty(type = %sProps)\n" % (txt_name_id, txt_name_class)
        
        elif pps.addonParts  == "CollectProp":
            #txt_collectionProp % (ClassName, ClassName, idname, ClassName, id_name, id_name)
            txt = txt_collectionProp % (txt_name_class, txt_name_class, txt_name_id, txt_name_class, txt_name_id, txt_name_id)
            
        elif pps.addonParts == "bl_info":
            txt = txt_blInfo % txt_name
        
        elif pps.addonParts == "MenuFunc":
            txt += "def menu_func(self, context):\n"
            txt += "    self.layout.operator(%sOperator.bl_idname, icon = 'PLUGIN')\n" % txt_name_class
            txt += "#bpy.types.VIEW3D_MT_object.append(menu_func) #put in register()\n"
            txt += "#bpy.types.VIEW3D_MT_object.remove(menu_func) #put in unregister()\n"

        elif pps.addonParts  == "Register" or pps.addonParts == "RegKeymap":
            temp1 = "bpy.utils.register_class(%sOperator)" % txt_name_class
            temp1 += "\n    #bpy.utils.register_class(%sPanel)" % txt_name_class
            temp1 += "\n    #bpy.utils.register_class(%sMenu)" % txt_name_class
            temp1 += "\n    #bpy.types.VIEW3D_MT_object.append(menu_func)"
            temp2 = "bpy.utils.unregister_class(%sOperator)" % txt_name_class
            temp2 += "\n    #bpy.utils.unregister_class(%sPanel)" % txt_name_class
            temp2 += "\n    #bpy.utils.unregister_class(%sMenu)" % txt_name_class
            temp2 += "\n    #bpy.types.VIEW3D_MT_object.remove(menu_func)"
            
            if pps.addonParts == "Register":
                txt += txt_reg % (temp1, temp2)
            else:
                if not pps.isKmiCallMenu:
                    #txt_reg_keymap % (bpy.utils.register(), keymap_items.new(%s,,,,) ,assign prop to kmi, bpy.utils.unregister())    
                    txt += txt_reg_keymap % (temp1, txt_name_class + "Operator.bl_idname", "#kmi.properties.prop1 = 'some'", temp2)
                else:
                    txt += txt_reg_keymap % (temp1, "wm.call_menu", "kmi.properties.name = %sMenu.bl_idname" % txt_name_class, temp2)
            
        elif pps.addonParts == "GPL":
            txt = txt_GPL
        
        return txt
    
    #---- 
    def getUILayoutMembers(self, context):
        pps = context.scene.chichige_add_snippet_props
        
        txt = pps.uiLayoutMembers
        if pps.isAddUILayoutParams:
            txt = self.uiLayoutParamDic[txt] + "\n"
        elif not txt.endswith('()'):
            txt += " = "
        return txt

            
    #-----
    def getKeymap(self, context):
        pps = context.scene.chichige_add_snippet_props

        txt_name = pps.overallName.strip()#re.sub('[\W]', '_', txt_name)
        txt_name = txt_name if txt_name != '' else 'Hello World'
        txt_name_class = txt_name.replace(" ", "") 

        txt = ""
        txt += "#addon_keymaps = [] #put on out of register()\n"

        txt += "    wm = bpy.context.window_manager\n"
        txt += "    km = wm.keyconfigs.addon.keymaps.new(name = '%s', space_type = '%s'%s%s)\n" % (pps.kmName, pps.kmSpaceType, ("" if pps.kmRegionType == "WINDOW" else ", region_type = '%s'" % pps.kmRegionType), (", modal = True" if pps.kmIsModal else ""))
        txtKeys = (", any=True" if pps.kmiKeysBit & 1 else "") + (", shift=True" if pps.kmiKeysBit & 2 else "") + (", ctrl=True" if pps.kmiKeysBit & 4 else "") + (", alt=True" if pps.kmiKeysBit & 8 else "") + (", oskey=True" if pps.kmiKeysBit & 16 else "")
        if not pps.kmIsModal:
            txt += "    kmi = km.keymap_items.new(%s" % ('"wm.call_menu"' if pps.isKmiCallMenu else (txt_name_class + "Operator.bl_idname"))
        else:
            txt += "    kmi = km.keymap_items.new_modal('CONFIRM'"    
        txt += ", '%s', '%s'%s%s)\n" % (('TEXTINPUT' if pps.kmiMapType == 'TEXTINPUT' else pps.kmiType), ('NOTHING' if pps.kmiMapType in {'TEXTINPUT', 'TIMER'} else pps.kmiValue), txtKeys, ("" if pps.kmiKeyMod == 'NONE' else ", key_modifier = '%s'" % pps.kmiKeyMod))
        if pps.isKmiCallMenu:
            txt += "    kmi.properties.name = %sMenu.bl_idname\n" % txt_name_class
        else:
            txt += "    #kmi.properties.my_prop = 'some'\n"
        txt += "    addon_keymaps.append((km, kmi))\n"
        return txt

            
    def checkKeymapConflicts(self, context):
        pps = context.scene.chichige_add_snippet_props
        keys = []
        keys.append('Any') if pps.kmiKeysBit & 1 else None
        keys.append('Shift') if pps.kmiKeysBit & 2 else None
        keys.append('Ctrl') if pps.kmiKeysBit & 4 else None
        keys.append('Alt') if pps.kmiKeysBit & 8 else None
        keys.append('Oskey') if pps.kmiKeysBit & 16 else None

        text = ""
        text += "####################################################\n"
        text += "######### KEYMAP CONFLICTS CHECKER #################\n"
        text += "####################################################\n"
        text += " Mark as 'Similar' If map_type and type are equal but other props \n"
        text += " Note :I couldn't understand keymap well. This checker is unreliable.\n\n"
        text += "====================================================\n"
        text += " Haystack : keyconfigs.user.keymaps\n"
        text += " Subject  : "
        if pps.kmiMapType in {'TEXTINPUT', 'TIMER'}:
            text += "%s%s\n" % (pps.kmiMapType, (", " + pps.kmiType if pps.kmiMapType == 'TIMER' else ""))
        else:
            text += "%s, %s, %s, %s, mod: %s\n" % (pps.kmiMapType, pps.kmiType, pps.kmiValue, keys, pps.kmiKeyMod)
        text += "====================================================\n"

        kc = context.window_manager.keyconfigs.user
        for km in kc.keymaps:
            if km.name == pps.kmName:
                break
        text += self.getKeymapConflicts_km(context, km)
        
        for km in kc.keymaps:
            if km.name != pps.kmName:
                text+= self.getKeymapConflicts_km(context, km)
                
        print(text)
        
    def getKeymapConflicts_km(self, context, km):
        pps = context.scene.chichige_add_snippet_props
        text = "\n"
        
        matchText = ""
        similarText = ""
        matchTitle =   " < MATCH > : "
        similarTitle = "  Similar  : "
        
        text += "-- %s %s\n" % (km.name, "-" * (60 - len(km.name)) )
        for kmi in km.keymap_items:
            if kmi.map_type == pps.kmiMapType and (kmi.map_type == 'TEXTINPUT' or (kmi.map_type != 'TEXTINPUT' and kmi.type == pps.kmiType)):
                
                tempText = kmi.propvalue if km.is_modal else kmi.name
                
                if kmi.map_type in {'TEXTINPUT', 'TIMER'}:
                    matchText += matchTitle + tempText + "\n"
                else:
                    keys = []
                    keys.append('Any') if kmi.any else None
                    keys.append('Shift') if kmi.shift else None
                    keys.append('Ctrl') if kmi.ctrl else None
                    keys.append('Alt') if kmi.alt else None
                    keys.append('Oskey') if kmi.oskey else None
                    tempText += " (%s, %s, mod: %s)\n" % (kmi.value, str(keys).replace("'", ""), kmi.key_modifier)
                    if kmi.name == "Call Menu":
                        tempText += (" " * 23) + ("(menu: %s)\n" % kmi.properties['name'])

                    
                    keysBit = (2 if kmi.shift else 0) | (4 if kmi.ctrl else 0) | (8 if kmi.alt else 0) | (16 if kmi.oskey else 0)                    
                    if kmi.value == pps.kmiValue and keysBit == (pps.kmiKeysBit & 30) and kmi.key_modifier == pps.kmiKeyMod:
                        matchText += matchTitle + tempText
                    else:                    
                        similarText += similarTitle + tempText
        
        if km.name == pps.kmName:
            text += matchText if matchText else matchTitle + " (Not found)\n"
            text += similarText if similarText else similarTitle + " (Not found)\n"
        else:
            if not matchText and not similarText:
                text = ""
            else:
                text += matchText if matchText else ""
                text += similarText if similarText else ""
        
        return text
        

####################################################################################

class GeneratorButtonsPanel:
    bl_space_type = 'TEXT_EDITOR'
    bl_region_type = 'UI'


class AddSnippetPanel(GeneratorButtonsPanel, bpy.types.Panel):
    """Addon Template Generator Panel"""
    bl_idname = "TEXTEDITOR_PT_add_snippet_panel"
    bl_label = "Generator"
    bl_category = "Generator"    
    bl_space_type = 'TEXT_EDITOR'
    bl_region_type = 'UI'
    
    def draw(self, context):
        layout = self.layout
        pps = context.scene.chichige_add_snippet_props
        
        layout.prop(pps, 'isClipboard')
        layout.prop(pps, 'overallName')


class TEXT_PT_generator_properties(GeneratorButtonsPanel, bpy.types.Panel):
    bl_parent_id = "TEXTEDITOR_PT_add_snippet_panel"
    bl_label = "Properties"
    bl_options = {'DEFAULT_CLOSED'}
    bl_space_type = 'TEXT_EDITOR'   

    
    def draw(self, context):
        layout = self.layout
        pps = context.scene.chichige_add_snippet_props        
        row = layout.row(align = True)
        row.operator(AddSnippetOp_Props.bl_idname, text = "ClearAll").type = "CHECK_CLEAR"
        row.operator(AddSnippetOp_Props.bl_idname, text = "AddonDefault").type = "CHECK_DEFAULT"
        row.operator(AddSnippetOp_Props.bl_idname, text = "SelectAll").type = "CHECK_ALL"
        
        col = layout.column(align = True)
        box = col.box()
        row = box.row()
        row.prop(pps, 'isAddRefComment')
        row.prop(pps, 'isAddPrefix')
        row.prop(pps, 'isAddName')
        row = box.row()
        row.prop(pps, 'isAddDesc')
        row.prop(pps, 'isAddDefault')
        row.prop(pps, 'isAddUpdate')
        
        row = col.box().row()
        row.prop(pps, 'isAddMinMax')
        row.prop(pps, 'isAddSoftMinMax')
        row.prop(pps, 'isAddStep')
        row.prop(pps, 'isAddSize')
        
        box = col.box()
        split = box.split(factor=0.18)
        split.label(text='Options')   
        row = split.row()
        row.prop(pps, 'propOptions')
        split = box.split(factor=0.18)
        split.label(text='Subtype')   
        row = split.row()
        row.prop(pps, 'propSubtype', text="")
        row.prop(pps, 'propVecSubtype', text="")
        
        #--------
        split = layout.split()
        row = split.row(align = True)
        row.operator(AddSnippetOp_Props.bl_idname, text = "Bool").type = 'Bool'
        row.operator(AddSnippetOp_Props.bl_idname, text = "BoolVec").type = 'BoolVector'
        row = split.row(align = True)
        row.operator(AddSnippetOp_Props.bl_idname, text = "Int").type = 'Int'
        row.operator(AddSnippetOp_Props.bl_idname, text = "IntVec").type = 'IntVector'
        row = layout.row(align = True)
        row.prop(pps, 'isAddFloatPrec')     
        row.prop(pps, 'floatUnit', text = "")
        row.operator(AddSnippetOp_Props.bl_idname, text = "Float").type = 'Float'
        row.operator(AddSnippetOp_Props.bl_idname, text = "FloatVec").type = 'FloatVector'
        row = layout.row(align = True)
        row.prop(pps, 'stringSubtype', text = "")
        row.operator(AddSnippetOp_Props.bl_idname, text = "String").type = 'String'
        split = layout.split(factor=0.5)
        row = split.row(align = True)
        row.prop(pps, 'isAddEnumFlag')
        row.operator(AddSnippetOp_Props.bl_idname, text = "Enum").type = 'Enum'
        split.operator(AddSnippetOp_Props.bl_idname, text = "Collection").type = 'Collection'
        split.operator(AddSnippetOp_Props.bl_idname, text = "Pointer").type = 'Pointer'
        layout.separator()


class TEXT_PT_generator_panel_place(GeneratorButtonsPanel, bpy.types.Panel):
    bl_parent_id = "TEXTEDITOR_PT_add_snippet_panel"
    bl_label = "Panel Place"
    bl_options = {'DEFAULT_CLOSED'}
    bl_space_type = 'TEXT_EDITOR'  
    
    def draw(self, context):
        layout = self.layout
        pps = context.scene.chichige_add_snippet_props 
           
        row = layout.row(align = True)
        split = layout.split(factor=0.25)
        colLabel = split.column()
        subSplit = split.split(factor=0.85)
        colCombo = subSplit.column()
        colButton = subSplit.column()

        colLabel.label(text='Space:')
        colCombo.prop(pps, "panelSpace", text = '')
        colButton.label(text='')
        
        colLabel.label(text='Region:')
        if pps.panelSpace.startswith('SEPA'):
            colCombo.label(text='')
        else:
            if pps.panelSpace == 'VIEW_3D' or pps.panelSpace == 'CLIP_EDITOR':
                colCombo.prop(pps, "panelRegion_view3d_clip", text = "")
            elif pps.panelSpace == 'PROPERTIES' or pps.panelSpace == 'USER_PREFERENCES':
                colCombo.label(text="WINDOW")
            elif pps.panelSpace == 'FILE_BROWSER':
                colCombo.label(text="CHANNELS")
            elif pps.panelSpace == 'IMAGE_EDITOR' or pps.panelSpace == 'NODE_EDITOR':
                colCombo.prop(pps, "panelRegion_image_node", text = "")
            else:
                colCombo.label(text="UI")

            if pps.panelSpace == 'VIEW_3D':
                colLabel.label(text="Context:")
                colCombo.prop(pps, "panelContext_view3d", text = "")
                if pps.panelRegion_view3d_clip == 'TOOLS':
                    colLabel.label(text="Tab:")
                    if pps.panelContext_view3d == 'objectmode':
                        colCombo.prop(pps, "panelCategory_objectmode", text = "")
                    elif pps.panelContext_view3d == 'mesh_edit':
                        colCombo.prop(pps, "panelCategory_editmode", text = "")
                    else:
                        colCombo.prop(pps, "panelCategory_others", text = "")                        
            
            elif pps.panelSpace == 'PROPERTIES':
                colLabel.label(text="Context:")
                colCombo.prop(pps, "panelContext_properties", text = "")
            
            elif pps.panelSpace == 'IMAGE_EDITOR' and pps.panelRegion_image_node == 'TOOLS':
                colLabel.label(text="Tab:")
                colCombo.prop(pps, "panelCategory_imageeditor", text = "")
            
        # determine button position
        if pps.panelSpace == 'VIEW_3D':
            colButton.label(text='') #region row
            if pps.panelRegion_view3d_clip == 'TOOLS':
                colButton.label(text='')
        elif pps.panelSpace == 'PROPERTIES' or (pps.panelSpace == 'IMAGE_EDITOR' and pps.panelRegion_image_node == 'TOOLS'):
            colButton.label(text='') #region row

        row = colButton.row() 
        row.enabled = not pps.panelSpace.startswith('SEPA')
        row.operator(AddSnippetOp_Samples.bl_idname, text = "", icon="COPYDOWN" if pps.isClipboard else "FORWARD").type = "PanelPlace"
        layout.separator()
        

class TEXT_PT_generator_code_samples(GeneratorButtonsPanel, bpy.types.Panel):
    bl_parent_id = "TEXTEDITOR_PT_add_snippet_panel"
    bl_label = "Code Samples"
    bl_options = {'DEFAULT_CLOSED'}
    bl_space_type = 'TEXT_EDITOR'  
    
    def draw(self, context):
        layout = self.layout
        pps = context.scene.chichige_add_snippet_props 
        row = layout.row(align = True)
        col = layout.column(align = True)
        col.label(text="Addon Parts", icon = 'PLUGIN')
        #row = row.row() #I want the button to be sticked to enum list. This way slightly separates. 
        #row.enabled = not pps.uiLayoutMembers.startswith('SEPA')
        row = col.row(align = True)
        row.prop(pps, 'addonParts', text="")            
        if not pps.addonParts.startswith('SEPA'):
            row.operator(AddSnippetOp_Samples.bl_idname, text = "", icon="COPYDOWN" if pps.isClipboard else "FORWARD").type = "AddonParts"
        else:
            row.operator(AddSnippetOp_Samples.bl_idname, text="", icon ="LIBRARY_DATA_INDIRECT").type = "INEFFECTIVE"

        layout.separator()
        col = layout.column(align = True)
        col.label(text="Hint Snippets", icon = 'OUTLINER_OB_LIGHT') 
        row = col.row(align = True)
        row.prop(pps, 'hintSnippets', text = "")
        if not pps.hintSnippets.startswith('SEPA'):
            row.operator(AddSnippetOp_Samples.bl_idname, text = "", icon="COPYDOWN" if pps.isClipboard else "FORWARD").type = "HintSnippets"
        else:
            row.operator(AddSnippetOp_Samples.bl_idname, text="", icon ="LIBRARY_DATA_INDIRECT").type = "INEFFECTIVE"
        
        layout.separator()
        col = layout.column(align = True)
        row = col.row(align = True)
        row.label(text="UILayout Members", icon = 'MENU_PANEL')
        row.prop(pps, "isAddUILayoutParams", text = "Include All Params")
        row = col.row(align = True)
        row.prop(pps, 'uiLayoutMembers', text="")
        if not pps.uiLayoutMembers.startswith('SEPA'):
            row.operator(AddSnippetOp_Samples.bl_idname, text = "", icon="COPYDOWN" if pps.isClipboard else "FORWARD").type = "UILayoutMembers"
        else:
            row.operator(AddSnippetOp_Samples.bl_idname, text="", icon ="LIBRARY_DATA_INDIRECT").type = "INEFFECTIVE"
        
        layout.separator()


class TEXT_PT_generator_keymapping(GeneratorButtonsPanel, bpy.types.Panel):
    bl_parent_id = "TEXTEDITOR_PT_add_snippet_panel"
    bl_label = "Keymapping"
    bl_options = {'DEFAULT_CLOSED'}
    bl_space_type = 'TEXT_EDITOR'  
    
    def draw(self, context):
        layout = self.layout
        pps = context.scene.chichige_add_snippet_props 
        # prop(full_event = True) not worked despite effort with various EnumProperty settings.
        # propvalue (used when km.is_modal is true) can't be filtered out the value. so, just hide it.
        row = layout.row(align = True)
#        row.prop(pps, "isToolbarKeymapClosed", text = "", emboss = False, icon = "TRIA_RIGHT" if pps.isToolbarKeymapClosed else "TRIA_DOWN")
#        row.label(text='Keymapping ' + '-' * (110 - len('Keymaping ')))
#        if not pps.isToolbarKeymapClosed:
        split = layout.split(factor=0.9)
        colLeft = split.column()
        colButton = split.column()
        
        colLeft.prop(pps, "kmName", text = "")
        colLeft.label(text="(%s, %s, Modal: %s)" % (pps.kmSpaceType, pps.kmRegionType, pps.kmIsModal))
        #if not pps.kmIsModal:
        #    layout.prop(pps, "kmiIdName", text = "idname")
        #else:
        #    layout.prop(pps, "kmiPropVal", text = "PropVal")
        colLeft.prop(pps, "kmiMapType", text = "MapType")
        if pps.kmiMapType != 'TEXTINPUT':
            if pps.kmiMapType == 'TIMER':
                colLeft.prop(pps, "kmiType", text = "Type")
            else:
                row = colLeft.row(align = True)
                row.prop(pps, "kmiType", text = "")
                row.prop(pps, "kmiValue", text = "")
                
                row = colLeft.row(align = True)
                row.prop(pps, "isKmiAny")                
                row.prop(pps, "isKmiShift")                
                row.prop(pps, "isKmiCtrl")                
                row.prop(pps, "isKmiAlt")                
                row.prop(pps, "isKmiOskey")
                
                row = colLeft.row()
                subRow = row.row()
                subRow.enabled = not pps.kmIsModal
                subRow.prop(pps, "isKmiCallMenu", text="(Call Menu)")            
                row.prop(pps, "kmiKeyMod", text = "Mod")
        
        # determine button position
        colButton.label(text="")
        colButton.label(text="")
        if pps.kmiMapType != 'TEXTINPUT':
            colButton.label(text="")
            if pps.kmiMapType != 'TIMER':
                colButton.label(text="")
                colButton.label(text="")
                
        row = colButton.row()
        row.operator(AddSnippetOp_Samples.bl_idname, text = "", icon="COPYDOWN" if pps.isClipboard else "FORWARD").type = "Keymap"
        
        colLeft.separator()
        colLeft.operator(AddSnippetOp_Samples.bl_idname, text="Check Confilicts to Console").type = 'CheckKeymapConflicts'
        
        layout.separator()
            
            
####################################################################################
# Scene item funcs, props ----

def getItems_propOptions(self, context):
    return convertToItems_prop(['HIDDEN', 'SKIP_SAVE', 'ANIMATABLE', 'LIBRARY_EDITABLE'])   

def getItems_propSubtype(self, context):
    return convertToItems_prop(['-- Subtype --', 'UNSIGNED', 'PERCENTAGE', 'FACTOR', 'ANGLE', 'TIME', 'DISTANCE', 'NONE'])   

def getItems_propVecSubtype(self, context):
    return convertToItems_prop(['-- VecSub --', 'COLOR', 'TRANSLATION', 'DIRECTION', 'VELOCITY', 'ACCELERATION', 'MATRIX', 'EULER', 'QUATERNION', 'AXISANGLE', 'XYZ', 'COLOR_GAMMA', 'LAYER', 'NONE'])

def getItems_floatUnit(self, context):
    return convertToItems_prop(['-- Unit --', 'NONE', 'LENGTH', 'AREA', 'VOLUME', 'ROTATION', 'TIME', 'VELOCITY', 'ACCELERATION'])
 
def getItems_stringSubtype(self, context):
    return convertToItems_prop(['-- Subtype --', 'FILE_PATH', 'DIR_PATH', 'FILENAME', 'NONE'])

def convertToItems_prop(itemsList):
    retVal = []
    for item in itemsList:
        if item.startswith("-"):
            retVal.append(('NO', item, ""))
        else: 
            retVal.append((item, item.replace("_", " ").title().replace(" ", ""), ""))
    return retVal

#----------
def getPanelCategoryItems_objectmode(self, context):
    return convertToItems_panelCategory(['Tools', 'Create', 'Basic', 'Animation', 'Physics', 'History'], isOmitOptions = True)

def getPanelCategoryItems_editmode(self, context):
    return convertToItems_panelCategory(['Tools', 'Create', 'Basic', 'Shading / UVs'])

def getPanelCategoryItems_others(self, context):#header only
    return convertToItems_panelCategory(['Tools'])

def convertToItems_panelCategory(itemsList = None, isOmitOptions = False):
    if not itemsList:
        itemsList = []
    if not isOmitOptions:
        itemsList.append('Options')
    itemsList.append('Grease Pencil')
    itemsList.append('Relations')
    retVal = [('NO', '-- none --', '')]
    for item in itemsList:
        retVal.append((item, item, ""))
    return retVal

#-----
def getUILayoutMemberItems(self, context):
    items = ['row()', 'column()', 'column_flow()', 'box()', 'split()',
             'SEPARATOR1', 'label()', 'menu()', 'separator()', 
             'SEPARATOR2', 'prop()', 'prop_menu_enum()', 'prop_enum()', 'prop_search()', 'props_enum()',
             'SEPARATOR3', 'operator()', 'operator_enum()', 'operator_menu_enum()',
             'SEPARATOR4', 'active', 'alert', 'alignment', 'enabled', 'scale_x', 'scale_y', 'operator_context']
    retVal = []
    for item in items:
        if item.startswith('SEPA'):
            retVal.append((item, '-' * 30, ""))
        else:
            retVal.append((item, item, ""))
    return retVal
   
#------keymapping-------
def update_kmName(self, context):
    pps = context.scene.chichige_add_snippet_props
    kc = context.window_manager.keyconfigs.user
    
    for km in kc.keymaps:
        if km.name == pps.kmName:
            pps.kmSpaceType = km.space_type
            pps.kmRegionType = km.region_type
            pps.kmIsModal = km.is_modal

def get_kmiAny(self):
    pps = bpy.context.scene.chichige_add_snippet_props
    return pps.kmiKeysBit & 1
def set_kmiAny(self, value):
    pps = bpy.context.scene.chichige_add_snippet_props
    pps.kmiKeysBit = 31 if value else 0

def get_kmiShift(self):
    pps = bpy.context.scene.chichige_add_snippet_props
    return pps.kmiKeysBit & 2
def set_kmiShift(self, value):
    setBitToKmiKeysBit(value, 2)


def get_kmiCtrl(self):
    pps = bpy.context.scene.chichige_add_snippet_props
    return pps.kmiKeysBit & 4
def set_kmiCtrl(self, value):
    setBitToKmiKeysBit(value, 4)

def get_kmiAlt(self):
    pps = bpy.context.scene.chichige_add_snippet_props
    return pps.kmiKeysBit & 8
def set_kmiAlt(self, value):
    setBitToKmiKeysBit(value, 8)

def get_kmiOskey(self):
    pps = bpy.context.scene.chichige_add_snippet_props
    return pps.kmiKeysBit & 16
def set_kmiOskey(self, value):
    setBitToKmiKeysBit(value, 16)
    
def setBitToKmiKeysBit(value, bit):
    pps = bpy.context.scene.chichige_add_snippet_props
    pps.kmiKeysBit
    if value and (pps.kmiKeysBit | bit) & 30 == 30 : #30 = all but Any. 2+4+8+16=30
        pps.kmiKeysBit = 31
    else:
        if value:
            pps.kmiKeysBit = ((pps.kmiKeysBit | bit) & 30)
        else:
            pps.kmiKeysBit = (pps.kmiKeysBit & (30 - bit))

        
#--EnumItem-------
def getKmiMapType(self, context):
    items = bpy.types.KeyMapItem.bl_rna.properties["map_type"].enum_items.values()
    retVal = []
    for item in items:
        retVal.append((item.identifier, item.name, item.description, item.icon, item.value))
    return retVal

def getKmName(self, context):
    kc = context.window_manager.keyconfigs.user
    retVal = []
    for km in kc.keymaps:
        retVal.append((km.name, km.name, km.name))
    return retVal

def getKmiType(self, context):
    pps = context.scene.chichige_add_snippet_props
    items = bpy.types.KeyMapItem.bl_rna.properties["type"].enum_items.values()
             
    if pps.kmiMapType == "TEXTINPUT":
        return (['TEXTINPUT', 'Text Input', '', '', -2])           
    else:
        retVal = []
        if pps.kmiMapType == 'KEYBOARD':
            for item in items:
                if (item.value >= 97 and item.value <= 259) or (item.value >= 280 and item.value <=399):
                    retVal.append((item.identifier, item.name, item.description, item.icon, item.value))
            return retVal
        elif pps.kmiMapType == 'TWEAK':
            min, max = 20482, 20486   
        elif pps.kmiMapType == 'MOUSE':
            min, max = 1, 17
        elif pps.kmiMapType == 'NDOF':
            min, max = 400, 450
        elif pps.kmiMapType == 'TIMER':
            min, max = 272, 279
        else:
            min, max = 0, 0
            
        for item in items:
            if item.value >= min and item.value <= max:
                retVal.append((item.identifier, item.name, item.description, item.icon, item.value))
        return retVal
    
def getKmiValue(self, context):
    pps = context.scene.chichige_add_snippet_props
    items = bpy.types.KeyMapItem.bl_rna.properties["value"].enum_items.values()
             
    if pps.kmiMapType in {'TIMER', 'TEXTINPUT'}:
        return ['ANY', 'Any', '', '', -1]          
    else:
        retVal = []
        if pps.kmiMapType == 'KEYBOARD':
            for item in items:
                if item.identifier in ['ANY', 'PRESS', 'RELEASE']:
                    retVal.append((item.identifier, item.name, item.description, item.icon, item.value))
        elif pps.kmiMapType == 'TWEAK':
            for item in items:
                if not item.identifier in ['NOTHING', 'PRESS', 'RELEASE', 'CLICK', 'DOUBLE_CLICK']:
                    retVal.append((item.identifier, item.name, item.description, item.icon, item.value))            
        else: # pps.kmiMapType in {'MOUSE', 'NDOF'}:
            for item in items:
                if item.identifier in ['ANY', 'PRESS', 'RELEASE', 'CLICK', 'DOUBLE_CLICK']:
                    retVal.append((item.identifier, item.name, item.description, item.icon, item.value))            
        return retVal
    
def getKmiKeyMod(self, context):
    pps = context.scene.chichige_add_snippet_props
    items = bpy.types.KeyMapItem.bl_rna.properties["type"].enum_items.values()
       
    retVal = [('NONE', '', '', '', 0)]
    for item in items:
        if (item.value >= 97 and item.value <= 259) or (item.value >= 280 and item.value <=399):
            retVal.append((item.identifier, item.name, item.description, item.icon, item.value))
    return retVal

#-----
class AddSnippetProps(bpy.types.PropertyGroup):
    isClipboard: BoolProperty(name = "Copy to Clipboard instead of Insertion")
    overallName: StringProperty(name = "Overall Name", description = "Used for class name of sample codes", default = "Hello World")

    isAddRefComment: BoolProperty(name = "#Ref",         description = "Add reference line as comment", default = False)
    isAddPrefix:     BoolProperty(name = "prefix",       description = "Add bpy.props at first",        default = True)
    isAddName:       BoolProperty(name = "name",         description = "Add name",                      default = True)
    isAddDesc:       BoolProperty(name = "desc",         description = "Add description",               default = True)
    isAddDefault:    BoolProperty(name = "default",      description = "Add default",                   default = True)
    isAddMinMax:     BoolProperty(name = "min,max",      description = "Add min and max (maxlen for String)", default = True)
    isAddSoftMinMax: BoolProperty(name = "soft_min,max", description = "Add soft_min and soft_max",     default = False)
    isAddStep:       BoolProperty(name = "step",         description = "Add step",                      default = False)
    isAddSize:       BoolProperty(name = "size",         description = "Add size",                      default = False)
    isAddUpdate:     BoolProperty(name = "update",       description = "Add update",                    default = False)
    
    propOptions:    EnumProperty(items = getItems_propOptions,     name = "PropOptions",       description = "options of Property", options = {'ENUM_FLAG'})
    propSubtype:    EnumProperty(items = getItems_propSubtype,     name = "PropSubtype",       description = "subtype of Property")
    propVecSubtype: EnumProperty(items = getItems_propVecSubtype,  name = "PropVecSubtype",    description = "subtype of VectorProperty")

    isAddFloatPrec: BoolProperty(name = "precision", description = "Add precision to FloatProperty",   default = False)
    floatUnit:      EnumProperty(items = getItems_floatUnit,       name = "unit",    description = "unit of FloatProperty")
    stringSubtype:  EnumProperty(items = getItems_stringSubtype,   name = "subtype",     description = "subtype of StringProperty")
    isAddEnumFlag:  BoolProperty(name = "ENUM_FLAG", description = "Add ENUM_FLAG to options", default = False)
    
    #-----
    panelSpace: EnumProperty(items = [('VIEW_3D',          '3D View',               '', 'VIEW3D',      0),
                                       ('GRAPH_EDITOR',     'Graph Editor',          '', 'IPO',         1), 
                                       ('NLA_EDITOR',       'NLA Editor',            '', 'NLA',         2), 
                                       ('SEPARATOR1',       '-' * 40,                '', '',            3), 
                                       ('IMAGE_EDITOR',     'UV/Image Editor',       '', 'IMAGE_COL',   4), 
                                       ('SEQUENCE_EDITOR',  'Video Sequence Editor', '', 'SEQUENCE',    5), 
                                       ('CLIP_EDITOR',      'Movie Clip Editor',     '', 'CLIP',        6), 
                                       ('TEXT_EDITOR',      'Text Editor',           '', 'TEXT',        7), 
                                       ('NODE_EDITOR',      'Node Editor',           '', 'NODETREE',    8), 
                                       ('LOGIC_EDITOR',     'Logic Editor',          '', 'LOGIC',       9), 
                                       ('SEPARATOR2',       '-' * 40,                '', '',            10), 
                                       ('PROPERTIES',       'Properties',            '', 'BUTS',        11), 
                                       ('USER_PREFERENCES', 'User Preferences',      '', 'PREFERENCES', 12), 
                                       ('FILE_BROWSER',     'File Browser',          '', 'FILESEL',     13)],
                              name = "Space",
                              description = "bl_space_type of Panel class")
    
    panelRegion_view3d_clip: EnumProperty(items = [('TOOLS', 'TOOLS', ''), ('TOOL_PROPS', 'TOOL_PROPS', ''), ('UI', 'UI', '')] , name = "Region", description = "bl_region_type of Panel class")
    panelRegion_image_node: EnumProperty(items = [('TOOLS', 'TOOLS', ''), ('UI', 'UI', '')] , name = "Region", description = "bl_region_type of Panel class")

    panelContext_view3d: EnumProperty(items = [('NO',             '-- none --',   '', '', 0),
                                                ('objectmode',     'Object Mode',  '', 'OBJECT_DATA', 1),
                                                ('posemode',       'Pose Mode',    '', 'POSE_HLT', 2),
                                                ('SEPARATOR',      '-' * 20,       '', '', 3),
                                                ('mesh_edit',     'Edit Mesh',     '', 'OUTLINER_OB_MESH', 4),
                                                ('armature_edit', 'Edit Armature', '', 'OUTLINER_OB_ARMATURE', 5),
                                                ('curve_edit',    'Edit Curve',    '', 'OUTLINER_OB_CURVE', 6),
                                                ('text_edit',     'Edit Text',     '', 'OUTLINER_OB_FONT', 7),
                                                ('SEPARATOR',     '-' * 20,        '', '', 8),
                                                ('lattice_edit',  'Edit Lattice',  '', 'OUTLINER_OB_LATTICE', 9),
                                                ('surface_edit',  'Edit Surface',  '', 'OUTLINER_OB_SURFACE', 10),
                                                ('mball_edit',    'Edit MBall',    '', 'OUTLINER_OB_META', 11),
                                                ('SEPARATOR',     '-' * 20,        '', '', 12),
                                                ('imagepaint',    'Image Paint',   '', 'TPAINT_HLT', 13),
                                                ('weightpaint',   'Weight Paint',  '', 'WPAINT_HLT', 14),
                                                ('vertexpaint',   'Vertex Paint',  '', 'VPAINT_HLT', 15),
                                                ('particlemode',  'Particle Mode', '', 'PARTICLEMODE', 16)],
                                        name = "Context", 
                                        description = "bl_context of Panel class")
    panelContext_properties: EnumProperty(items = [('render',       'Render',      '', 'SCENE', 3),
                                                   ('render_layer', 'RenderLayer', '', 'RENDERLAYERS', 4),
                                                   ('scene',        'Scene',       '', 'SCENE_DATA', 5),
                                                   ('world',        'World',       '', 'WORLD_DATA', 6),
                                                   ('object',       'Object',      '', 'OBJECT_DATA', 7),
                                                   ('constraint',   'Constraint',  '', 'CONSTRAINT', 8),
                                                   ('modifier',     'Modifier',    '', 'MODIFIER', 9),
                                                   ('data',         'Data',        '', 'MESH_DATA', 10),
                                                   ('material',     'Material',    '', 'MATERIAL', 11),
                                                   ('texture',      'Texture',     '', 'TEXTURE', 12),
                                                   ('particles',    'Particles',   '', 'PARTICLES', 13),
                                                   ('physics',      'Physics',     '', 'PHYSICS', 14)],
                                        name = "Context", 
                                        description = "bl_context of Panel class")

    panelCategory_objectmode:  EnumProperty(items = getPanelCategoryItems_objectmode, name = "Tab", description = "bl_category of Panel class")
    panelCategory_editmode:    EnumProperty(items = getPanelCategoryItems_editmode,   name = "Tab", description = "bl_category of Panel class")
    panelCategory_others:      EnumProperty(items = getPanelCategoryItems_others,     name = "Tab", description = "bl_category of Panel class")
    panelCategory_imageeditor: EnumProperty(items = [('NO', '-- none --', ''), ('Tools', 'Tools', ''), ('Scopes', 'Scopes', ''), ('Grease Pencil', 'Grease Pencil', '')],     name = "Tab", description = "bl_category of Panel class")
    
    addonParts: EnumProperty(items = [('OperatorClass',   'Operator Class', ''),
                                       ('PanelClass',      'Panel Class', ''),
                                       ('MenuClass',       'Menu Class', ''),
                                       ('Props(Operator)', 'Properties (Operator)', ''),
                                       ('PropGroup',       'PropertyGroup (Scene)', ''),
                                       ('CollectProp',     'CollectionProp (Scene)', ''),
                                       ('SEPARATOR',       '-' * 30, ''),
                                       ('bl_info',         'bl_info', ''),
                                       ('MenuFunc',        'Menu Function', ''),
                                       ('Register',        'Register', ''),
                                       ('RegKeymap',       'Reg with Keymap', ''),
                                       ('GPL',             'GPL Block', '')],
                                 name = "Addon Parts")

    hintSnippets: EnumProperty(items = [('Basic',                 'Basic', ''),
                                         ('BasicForLoop',          'Basic For Loop', ''),
                                         ('DuplicateObject',       'Duplicate Object', ''),
                                         ('SEPARATOR',             '-' * 30, ''),
                                         ('CreateNewMesh',         'Create New Mesh', ''),
                                         ('AddNewMaterial',        'Add New Material', ''),
                                         ('AddNewTexture',         'Add New Texture', ''),
                                         ('SEPARATOR',             '-' * 30, ''),
                                         ('AddNewUVMap',           'Add New UVMap', ''),
                                         ('AddAndApplyModifier',   'Add and Apply Modifier', ''),
                                         ('AddConstraint',         'Add Constraint', ''),
                                         ('SEPARATOR',             '-' * 30, ''),
                                         ('CreateNewArmature',     'Create New Armature', ''),
                                         ('ManipulatePoseBones',   'Manipulate Pose Bones', ''),
                                         ('SEPARATOR',             '-' * 30, ''),
                                         ('AddNewNodes_Material',  'Add New Nodes (Material)', ''),
                                         ('AddNewNodes_Composite', 'Add New Nodes (Composite)', ''),
                                         ('AddFCurve',             'Add FCurve', ''),
                                         ('CreateTextBlock',       'Create TextBlock', '')],
                                 name = "Hint Snippets")
        
    isAddUILayoutParams: BoolProperty(name = "Add All Parameters", description = "Includes all parameters if checked")
    uiLayoutMembers: EnumProperty(items = getUILayoutMemberItems, name = "Members of UILayout", description = "Reminder purpose")
                                  
    #---- keymapping -------
    kmName: EnumProperty(items = getKmName, name = "Keymap Name", update = update_kmName)
    kmSpaceType: StringProperty(default = 'EMPTY') #set by update_kmName() to reduce overhead
    kmRegionType: StringProperty(default = 'WINDOW') #set by update_kmName()
    kmIsModal: BoolProperty(default = False) #set by update_kmName()
    
    #kmiIdName = StringProperty()
    #kmiPropVal =  StringProperty()
    kmiMapType:  EnumProperty(items = getKmiMapType, name = "KeymapItem MapType")
    kmiType: EnumProperty(items = getKmiType, name = "KeymapItem Type")
    kmiValue: EnumProperty(items = getKmiValue, name = "KeymapItem Value")
    kmiKeyMod: EnumProperty(items = getKmiKeyMod, name = "KeymapItem KeyModifier")
    
    isKmiAny:   BoolProperty(name = "Any",   set = set_kmiAny,   get = get_kmiAny) 
    isKmiShift: BoolProperty(name = "Shift", set = set_kmiShift, get = get_kmiShift)
    isKmiCtrl:  BoolProperty(name = "Ctrl",  set = set_kmiCtrl,  get = get_kmiCtrl)
    isKmiAlt:   BoolProperty(name = "Alt",   set = set_kmiAlt,   get = get_kmiAlt)
    isKmiOskey: BoolProperty(name = "Cmd",   set = set_kmiOskey, get = get_kmiOskey)
    kmiKeysBit: IntProperty() #Any : 1, Shift : 2, Ctrl : 4, Alt : 8, Oskey : 16
    isKmiCallMenu: BoolProperty(description = "Check if you want to use the keymap to pop up a menu")
    
    #------ Collapse toolbar ---------
    isToolbarPropsClosed: BoolProperty()
    isToolbarPanelPlaceClosed: BoolProperty(default = True)
    isToolbarCodeSamplesClosed: BoolProperty(default = True)
    isToolbarKeymapClosed: BoolProperty(default = True)
    
    
####################################################################################        

def menu_func(self, context):
    self.layout.operator(AddonTemplateGeneratorOp.bl_idname)

# Registration---_------------------------------------------
def register():
    bpy.utils.register_class(AddSnippetProps)
    bpy.types.Scene.chichige_add_snippet_props = PointerProperty(type = AddSnippetProps)
    bpy.utils.register_class(AddSnippetPanel) 
    bpy.utils.register_class(TEXT_PT_generator_properties)
    bpy.utils.register_class(TEXT_PT_generator_panel_place)
    bpy.utils.register_class(TEXT_PT_generator_code_samples)
    bpy.utils.register_class(TEXT_PT_generator_keymapping)
    bpy.utils.register_class(AddonTemplateGeneratorOp)
    bpy.utils.register_class(AddSnippetOp_Props)
    bpy.utils.register_class(AddSnippetOp_Samples)
    bpy.types.TEXT_MT_templates.append(menu_func)

def unregister():
    bpy.utils.unregister_class(AddSnippetProps)
    #del bpy.types.Scene.chichige_add_snippet_props
    bpy.utils.unregister_class(TEXT_PT_generator_properties)
    bpy.utils.unregister_class(TEXT_PT_generator_panel_place)
    bpy.utils.register_class(TEXT_PT_generator_code_samples)
    bpy.utils.register_class(TEXT_PT_generator_keymapping)
    bpy.utils.unregister_class(AddonTemplateGeneratorOp)
    bpy.utils.unregister_class(AddSnippetOp_Props)
    bpy.utils.unregister_class(AddSnippetOp_Samples)
    bpy.utils.unregister_class(AddSnippetPanel)
    bpy.types.TEXT_MT_templates.remove(menu_func)
    
if __name__ == "__main__":
    register()
    
    
####################################################################################        
# belows are used from both TemplateGeneratorOp and CodeSamplesOp
####################################################################################        
#Text blocks at last ===


txt_GPL = """\
# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

"""


txt_blInfo = """\
bl_info = {
    "name": "%s",
    "author": "Your Name Here",
    "version": (1, 0),
    "blender": (2, 70, 0),
    "location": "View3D > Object > ",
    "description": "Adds a new Mesh Object",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Add Mesh"}

"""
txt_props = """\
    my_bool:     BoolProperty(name="", description="", default=False)
    my_boolVec:  BoolVectorProperty(name="", description="", default=(False, False, False))
    my_float:    FloatProperty(name="", description="", default=0.0)
    my_floatVec: FloatVectorProperty(name="", description="", default=(0.0, 0.0, 0.0)) 
    my_int:      IntProperty(name="", description="", default=0)  
    my_intVec:   IntVectorProperty(name="", description="", default=(0, 0, 0))
    my_string:   StringProperty(name="String Value", description="", default="", maxlen=0)
    my_enum:     EnumProperty(items = [('ENUM1', 'Enum1', 'enum prop 1'), 
                                        ('ENUM2', 'Enum2', 'enum prop 2')],
                               name="",
                               description="",
                               default="ENUM1")
"""
#txt_operator % (className, "ToolTip", bl_idname, bl_label, \t(bl_options)\n\n, (props)) 
txt_operator = """\
class %s(bpy.types.Operator):
    ""%s""
    bl_idname = "%s"
    bl_label = "%s"
%s%s
    #@classmethod
    #def poll(cls, context):
    #    return context.object is not None
    
    def execute(self, context):
        self.report({'INFO'}, "Hello World!")
        return {'FINISHED'}
    
    #def invoke(self, context, event):
    #    wm.modal_handler_add(self)
    #    return {'RUNNING_MODAL'}  
    #    return wm.invoke_porps_dialog(self)
    #def modal(self, context, event):
    #def draw(self, context):

"""

#txt_panel % (ClassName, "ToolTip", bl_idname, bl_label, SpaceRegion, bl_context, OperatorClassName, ButtonLabel)
txt_panel = """\
class %s(bpy.types.Panel):
    ""%s""
    bl_idname = "%s"
    bl_label = "%s"
    %s
    %s
    
    #Panels in ImageEditor are using .poll() instead of bl_context.
    #@classmethod
    #def poll(cls, context):
    #    return context.space_data.show_paint
    
    def draw(self, context):
        layout = self.layout
        layout.operator(%s.bl_idname, text = "%s", icon = 'BLENDER')

"""

#txt_menu % (ClassName, bl_idname, bl_label, OperatorClassName)
txt_menu = """\
class %s(bpy.types.Menu):
    bl_idname = "%s"
    bl_label = "%s"

    def draw(self, context):
        layout = self.layout
        layout.operator(%s.bl_idname)
        layout.separator()
        layout.menu("VIEW3D_MT_transform")
        layout.operator_menu_enum("object.select_by_type", "type", text="Select All by Type...")

"""

txt_reg = """\
def register():
    %s

def unregister():
    %s
    
if __name__ == "__main__":
    register()
"""

#txt_reg_keymap % (bpy.utils.register(), keymap_items.new(%s,,,,) ,assign prop to kmi, bpy.utils.unregister())    
txt_reg_keymap = """\
# store keymaps here to access after registration
addon_keymaps = []

def register():
    %s
    
    # handle the keymap
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
    kmi = km.keymap_items.new(%s, 'SPACE', 'PRESS', ctrl=True, shift=True)
    %s
    addon_keymaps.append((km, kmi))

def unregister():
    %s
    
    # handle the keymap
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    
if __name__ == "__main__":
    register()
"""

#txt_collectionProp % (ClassName, ClassName, idname, ClassName, id_name, id_name)
txt_collectionProp = """\
class %sCollection(bpy.types.PropertyGroup):
    name = bpy.props.StringProperty(name="Test Prop Name", default="Unknown")
    value = bpy.props.IntProperty(name="Test Prop Value",  default=22)

bpy.utils.register_class(%sCollection)
bpy.types.Scene.addongen_%s_collection = bpy.props.CollectionProperty(type = %sCollection)

my_item = bpy.context.scene.addongen_%s_collection.add()
my_item.name = "Spam"
my_item.value = 1000

my_item = bpy.context.scene.addongen_%s_collection.add()
my_item.name = "Eggs"
my_item.value = 30
"""

#---------------------------------
# variable name should match the enum value

txt_hint_Basic = """\
        #INFO, WARNING, ERROR  
        self.report({'INFO'}, "Hello World!") 
        
        #Python: True if A == B else False (Non-Python: A == B ? true : false)
        print("Identical" if context.object == context.active_object else "Different")#True
        
        print("%s has %d objects" % (context.scene.name, len(context.scene.objects)))
        
        print(context.scene.cursor_location)
        print(context.scene.frame_current)
        
        #CYCLES, BLENDER_RENDER
        print(context.scene.render.engine) 
        
        #MESH, CURVE, SURFACE, META, FONT, ARMATURE, LATTICE, EMPTY, CAMERA, LAMP, SPEAKER
        print(context.object.type)
        
        #OBJECT, EDIT, POSE, SCULPT, VERTEX_PAINT, WEIGHT_PAINT, TEXTURE_PAINT, PARTICLE_EDIT    
        bpy.ops.object.mode_set(mode = 'OBJECT')  
        
        #select an object only
        obj = context.scene.objects[0]
        context.scene.objects.active = obj
        bpy.ops.object.select_all(action='DESELECT')
        obj.select = True

        #set layers
        obj.layers = [i in [0, 19] for i in range(20)] # Base 0
        obj.layers = [True for i in range(20)] # all
        
        #FINISHED, CANCELLED, RUNNING_MODAL, PASS_THROUGH
        return {'FINISHED'}
"""        

txt_hint_BasicForLoop = """\
        #for selection
        for obj in context.selected_objects:
            obj.show_name = not obj.show_name #toggle
        
        #for objects in a group
        groupName = "GroupName"
        if not groupName in bpy.data.groups:
            self.report({'WARNING'}, "%s was not found" % groupName)
            return {'CANCELLED'}
        else:
            for obj in bpy.data.groups[groupName].objects:
                obj.show_axis = not obj.show_axis
            
        return {'FINISHED'}
"""

txt_hint_DuplicateObject = """\
        scene = context.scene
        
        obj_alt = context.object.copy()
        scene.objects.link(obj_alt)
        obj_alt.location = scene.cursor_location
        obj_alt.location.x += 1
        
        obj_shift = context.object.copy()
        obj_shift.data = obj_shift.data.copy()
        scene.objects.link(obj_shift)
        obj_shift.location = scene.cursor_location
        obj_shift.location.x -= 1
"""

txt_hint_AddNewMaterial = """\
        obj = context.object
        if len(obj.material_slots) == 0:
            print("No material found.")
        else:
            print("material_slots[0].link = %s" % obj.material_slots[0].link)
            if not obj.material_slots[0].material:
                print("material_slots[0] exists but empty.")
        
        print("active : %s, %d" % (obj.active_material, obj.active_material_index))
            
        mat = bpy.data.materials.new("Yellow")
        mat.diffuse_color = (1, 1, 0)
        mat.specular_intensity = 0.2
        obj.data.materials.append(mat)
"""
txt_hint_AddNewTexture = """\
        mat = context.object.active_material        
        if len(mat.texture_slots) == 0:
            print("No texture found.")
        else:
            #texture_slots[0] can be None
            for slot in mat.texture_slots:
                if slot and slot.texture:
                    print("tex.type = %s" % slot.texture.type)
                    break
        
        print("active : %s, %d" % (mat.active_texture, mat.active_texture_index))
            
        tex = bpy.data.textures.new("MyClouds", type = 'CLOUDS')
        tex.noise_basis = 'ORIGINAL_PERLIN'
        slot = mat.texture_slots.add()
        slot.texture = tex
        slot.use_map_normal = True
        slot.normal_factor = 0.1
"""

txt_hint_AddNewUVMap = """\
        #prepare images to be assigned to faces
        img1 = bpy.data.images.new('Grid', 300, 300)
        img1.generated_type = 'UV_GRID'
        img2 = bpy.data.images.new('ColorGrid', 300, 300)
        img2.generated_type = 'COLOR_GRID'       

        #.data is accessible only in ObjectMode. 
        # It's better to do this early.
        #http://www.blender.org/documentation/blender_python_api_2_69_release/info_gotcha.html#edit-mode-memory-access
        bpy.ops.object.mode_set(mode = 'OBJECT')

        mesh = context.object.data
        if len(mesh.uv_textures) == 8:
            uvTex = mesh.uv_textures[mesh.uv_textures.active_index]
            uvLayer = mesh.uv_layers[mesh.uv_textures.active_index]
        else:
            uvTex = mesh.uv_textures.new("UVMap")
            for i in range(len(mesh.uv_textures)):
                if mesh.uv_textures[i] == uvTex:
                    uvLayer = mesh.uv_layers[i]
                    break
        
        for i, poly in enumerate(mesh.polygons):
            print(i, poly)
            for j in poly.loop_indices:
                uv = uvLayer.data[j].uv
                uvLayer.data[j].uv = (uv[0] + (i / 10), uv[1])
            uvTex.data[i].image = img1 if i % 3 != 0 else img2
        
        print("\\n" + "-" * 30)
        print("len(mesh.loops) = %d" % len(mesh.loops))
        print("len(uvLayer.data) = %d" % len(uvLayer.data))
        print("len(mesh.polygons) = %d" % len(mesh.polygons))
        print("len(uvTex.data) = %d" % len(uvTex.data))
        
        poly = mesh.polygons[-1]
        print("\\nlen(mesh.polygons[0].vertices) = %d" % len(poly.vertices))
        print("mesh.polygons[-1].loop_indices = %s" % poly.loop_indices)
        print("mesh.polygons[-1].loop_start = %d" % poly.loop_start)
        print("mesh.polygons[-1].loop_total = %d" % poly.loop_total)
        print("mesh.polygons[-1].material_index = %d" % poly.material_index)             
            
        bpy.ops.object.mode_set(mode = 'EDIT')
"""

txt_hint_CreateNewMesh = """\
        verts = [(-1, 1, 0),
                 (1, 1, 0),
                 (1, -1, 0),
                 (-1, -1, 0)
                ]
        edges = []
        faces = [[0, 1, 2, 3]]
        
        mesh = bpy.data.meshes.new(name="ObjectDataName")
        obj = bpy.data.objects.new("ObjectName", mesh)

        scene = context.scene
        scene.objects.link(obj)        
        scene.objects.active = obj
        obj.location = scene.cursor_location
        bpy.ops.object.select_all(action='DESELECT') 
        obj.select = True

        mesh.from_pydata(verts, edges, faces)
        mesh.update(calc_edges=True)
"""

txt_hint_CreateNewArmature = """\
        scene = context.scene
        
        arma = bpy.data.armatures.new("ArmatureDataName")
        obj = bpy.data.objects.new("AramatureObjectName", arma)
        obj.location = scene.cursor_location

        scene.objects.link(obj)
        scene.objects.active = obj
        bpy.ops.object.select_all(action='DESELECT')
        obj.select = True
        
        bpy.ops.object.mode_set(mode='EDIT')
        bone1 = arma.edit_bones.new('Bone')
        bone1.head = (0,0,0)
        bone1.tail = (0,0,1)
        bone2 = arma.edit_bones.new('Bone.001')
        bone2.head = bone1.tail
        bone2.tail = (0,0,2)
        bone2.parent = bone1
        bone2.use_connect = True
        bpy.ops.object.mode_set(mode='OBJECT')
"""

txt_hint_ManipulatePoseBones = """\
        import math
        bpy.ops.object.mode_set(mode='POSE')
        
        bone1 = context.object.pose.bones[0]
        bone1.rotation_mode = 'XYZ'
        bone1.rotation_euler.x = math.radians(90)
        bone1.lock_location = [True, True, True]
        
        bone2 = context.object.pose.bones[1]
        bone2.rotation_quaternion.x = -1
        cnst = bone2.constraints.new('LIMIT_ROTATION')
        cnst.name = "Constraint Name"
        cnst.use_limit_y = True
        cnst.owner_space = 'LOCAL'
        
        bpy.ops.object.mode_set(mode='OBJECT')
"""

txt_hint_AddAndApplyModifier = """\
        mod = context.object.modifiers.new("ModName", 'ARRAY')
        mod.count = 3
        mod.relative_offset_displace = (1.2, 0, 0)
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier = mod.name)
"""

txt_hint_AddConstraint = """\
        cnst = context.object.constraints.new('LIMIT_LOCATION')
        cnst.name = 'ConstraintName'
        cnst.use_min_x = True
        cnst.min_x = 0
        cnst.use_transform_limit = True
"""

txt_hint_AddNewNodes_Material= """\
        #context.active_node #available only in Node context
        #context.object.active_material.node_tree.nodes.active 
        #.node_tree is None until .use_nodes becomes True
        #context.space_data.tree_type == 'ShaderNodeTree'
        
        mat = context.object.active_material
        if not mat:
            return {'CANCELLED'}
        
        mat.use_nodes = True
        rgbNode = mat.node_tree.nodes.new(type = 'ShaderNodeRGB')
        rgbNode.outputs['Color'].default_value = (1.0, 1.0, 0, 1) #Yellow
        rgbNode.location.x = -300 
        
        #for cycles
        difNode = mat.node_tree.nodes.new(type = 'ShaderNodeBsdfDiffuse')
        outNode = mat.node_tree.nodes.new(type = 'ShaderNodeOutputMaterial')
        difNode.location.y = 150
        outNode.location = (300, 150)
        mat.node_tree.links.new(rgbNode.outputs['Color'], difNode.inputs['Color'])
        mat.node_tree.links.new(difNode.outputs['BSDF'], outNode.inputs['Surface'])
                
        #for internal
        difNode = mat.node_tree.nodes.new(type = 'ShaderNodeMaterial')
        difNode.material = bpy.data.materials.new(name = "TestMaterial")
        outNode = mat.node_tree.nodes.new(type = 'ShaderNodeOutput')
        difNode.location.y = -150
        outNode.location = (300, -150)
        mat.node_tree.links.new(rgbNode.outputs['Color'], difNode.inputs['Color'])
        mat.node_tree.links.new(difNode.outputs['Color'], outNode.inputs['Color'])
"""

txt_hint_AddNewNodes_Composite = """\
        #context.active_node #available only in Node context
        #context.scene.node_tree.nodes.active 
        #context.space_data.tree_type == 'CompositorNodeTree'
        
        tree = context.scene.node_tree
        node1 = tree.nodes.new(type = 'CompositorNodeRLayers')
        node2 = tree.nodes.new(type = 'CompositorNodeBrightContrast')
        node2.inputs['Bright'].default_value = 0.2
        node2.inputs['Contrast'].default_value = 0.2
        node3 = tree.nodes.new(type = 'CompositorNodeComposite')
        node1.location.x = -250
        node3.location.x = 250 
        tree.links.new(node1.outputs['Image'], node2.inputs['Image'])
        tree.links.new(node2.outputs['Image'], node3.inputs['Image'])
"""

txt_hint_AddFCurve = """\
        #new() : data_path and index decide the prop. (eg "location" & [2] points loc z')
        #to existance : fcurve.data_path and .array_index decide the prop.
        #obj.animation_data also holds .drivers and .nla_tracks
    
        obj = context.object
        obj.animation_data_create()
        obj.animation_data.action = bpy.data.actions.new(name="MyAction")
        fc_z = obj.animation_data.action.fcurves.new(data_path='location', index=2)
        fc_z.keyframe_points.add(2)
        fc_z.keyframe_points[0].co = (10.0, 1.0)
        fc_z.keyframe_points[1].co = (20.0, 3.0)
        
        euler = []
        for i in range(3):
            euler.append(obj.animation_data.action.fcurves.new(data_path = 'rotation_euler', index = i, action_group = "Rotation"))
            euler[-1].keyframe_points.add(1)
            euler[-1].keyframe_points[0].co = (30.0, 3.1 * (i + 1))
        
        #overwrite immediately to demo    
        for fc in obj.animation_data.action.fcurves:
            if fc.data_path == 'rotation_euler' and fc.array_index == 1: # y
                fc.keyframe_points[0].co = (context.scene.frame_current, 3.1416 * 2)
"""

txt_hint_CreateTextBlock = """\
        text = "Hello world! My chichige is bobo!"
        textObj = bpy.data.texts.new('Hello_World')       
        textObj.write(text) #insert to cursor location
        #textObj.from_string(text)#replace all
        context.space_data.text = textObj #available only in TextEditor context
"""
