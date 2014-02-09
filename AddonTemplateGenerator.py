#top
bl_info = {
    "name": "Addon Template Generator",
    "author": "chichige-bobo",
    "version": (0, 8, 5),
    "blender": (2, 69, 0),
    "location": "TextEditor > Templates > AddonTemplateGenerator, TextEditor > PropertiesBar > AddSnippet",
    "description": "Generate empty addon template. Add snippet of propertes and samples",
    "warning": "not much tested yet",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Development"}

# LET USERS TO MANIPULATE AFTER GENERATED, NOT COMPLETE AT DIALOG
import bpy
from bpy.props import *

#####################################################################################

def getSpaceRegionItems(self, context):
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
             ('PROPERTIES-WINDOW-texture',      'Props-Window-Texture',     '', 'TEXTURE', 12),
             ('PROPERTIES-WINDOW-particles',    'Props-Window-Particles',   '', 'PARTICLES', 13),
             ('PROPERTIES-WINDOW-physics',      'Props-Window-Physics',     '', 'PHYSICS', 14),
             ('FILE_BROWSER-CHANNELS', 'FileBrowser-Channels',     '',  'FILESEL', 15)]
    return items
    
###############################################################################################
class AddonTemplateGeneratorOp(bpy.types.Operator):
    """ToolTip"""
    bl_idname = "chichige.addon_template_generator_operator"
    bl_label = "Addon Template Generator"
    bl_options = {'PRESET', 'INTERNAL'}
    
    # name for label, desc for tooltip in Operator Panel
    # options = Enumerator in ['HIDDEN', 'SKIP_SAVE', 'ANIMATABLE', 'LIBRARY_EDITABLE'] (and 'ENUM_FLAG' for EnumProp)
    
    p_name = StringProperty(name = "Overall Name", description="Used for various places", default="Addon Template")
    p_opOptions = EnumProperty(items = [('REGISTER', 'Register', 'Display in the info window and support the redo toolbar panel.'), 
                                      ('UNDO',     'Undo', 'Push an undo event (needed for operator redo)'),
                                      ('BLOCKING', 'Blocking', 'Block anything else from using the cursor'),
                                      ('MACRO',    'Macro', 'Use to check if an operator is a macro'),
                                      ('GRAB_POINTER', 'GrabPointer', 'Use so the operator grabs the mouse focus, enables wrapping when continuous grab is enabled'),
                                      ('PRESET', 'Preset', 'Display a preset button with the operators settings'),
                                      ('INTERNAL', 'Internal', 'Removes the operator from search results')],
                              name="bl_options", 
                              description="Options for this operator type", 
                              default={'REGISTER'}, 
                              options = {'ENUM_FLAG'})
    
    isUseOpProps = BoolProperty(name='Add Operator Properties', default = False )
    # put all method. it's not so bothering to delete unwanted methods.
    
    isUsePanel = BoolProperty(name='Add Panel Class', default = True )
    p_panelOptions = EnumProperty(items = [('DEFAULT_CLOSED', 'DefaultClosed', 'Defines if the panel has to be open or collapsed at the time of its creation'), 
                                           ('HIDE_HEADER', 'HideHeader', 'If set to False, the panel shows a header, which contains a clickable arrow to collapse the panel and the label')],
                                  name="PanelOptions",
                                  description="Options for Panel",
                                  default = set(),
                                  options = {'ENUM_FLAG'})
    
    p_panelSpaceRegion = EnumProperty(items = getSpaceRegionItems ,
                                      name="SpaceRegionType", 
                                      description="Panel's bl_space_type, bl_region_type and bl_context")                                

    isUseGPLNotice = BoolProperty(name='Add GPL Notification', default = False)
    isUseSceneProps = BoolProperty(name='Add Scene Properties', default = False )
    isUseMenuFunc = BoolProperty(name = 'Add Menu Function', default = False)
    isUseKeymap = BoolProperty(name='Add Keymapping', default = False )
    
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
        txt_name = txt_name if txt_name != '' else 'Addon Template'
        txt_className = txt_name.replace(" ", "") + "Operator" 
        txt_blIdname = 'addongen.' + txt_name.replace(" ", "_").lower() + '_operator'
        txt_blLabel = txt_name + " Operator"
        
        txt_blOptions = ""
        if len(self.p_opOptions) > 0:
            temp = list(self.p_opOptions)[::-1]
            for t in temp:
                txt_blOptions += "," if txt_blOptions != "" else ""
                txt_blOptions += "'%s'" % t
            txt_blOptions = "    bl_options = {%s}\n\n" % txt_blOptions
        
        temp = "" if not self.isUseOpProps else txt_props
        txt += txt_operator % (txt_className, '"ToolTip of ' + txt_className + '"', txt_blIdname, txt_blLabel, txt_blOptions, temp)
        
        #-----panel
        txt_className_p = txt_name.replace(" ", "") + "Panel"
        if self.p_panelSpaceRegion.startswith("PROP"):
            temp = self.p_panelSpaceRegion.split("-")[2].replace("_", "").upper()
        else:
            temp = self.p_panelSpaceRegion.split("-")[0].replace("_", "")
        txt_blIdname_p = temp + '_PT_' + txt_name.replace(" ", "_").lower()
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
        txt += "" if not self.isUsePanel else txt_panel % (txt_className_p, '"ToolTip of ' + txt_className_p + '"', 
                                                            txt_blIdname_p, txt_blLabel_p, txt_blOptions_p, 
                                                            txt_space_p + txt_region_p + txt_context_p, txt_className)
        
        #-----
        if self.isUseSceneProps:
            txt += "class MySceneProps(bpy.types.PropertyGroup):\n" + txt_props
            txt += "bpy.utils.register_class(MySceneProps)\n"
            txt += "bpy.types.Scene.%s_props = PointerProperty(type = MySceneProps)\n\n" % txt_blIdname.replace(".", "_")
           
        #-----
        if self.isUseMenuFunc:
            txt += "def menu_func(self, context):\n"
            txt += "    self.layout.operator(%s.bl_idname, icon = 'PLUGIN')\n\n" % txt_className
        
        #-----
        temp1 = "bpy.utils.register_class(%s)" % txt_className
        temp1 += "" if not self.isUsePanel else "\n    bpy.utils.register_class(%s)" % txt_className_p
        temp1 += "" if not self.isUseMenuFunc else "\n    bpy.types.VIEW3D_MT_object.append(menu_func)"
        temp2 = "bpy.utils.unregister_class(%s)" % txt_className
        temp2 += "" if not self.isUsePanel else "\n    bpy.utils.unregister_class(%s)" % txt_className_p
        temp2 += "" if not self.isUseMenuFunc else "\n    bpy.types.VIEW3D_MT_object.remove(menu_func)"
        if not self.isUseKeymap:
            txt += txt_reg % (temp1, temp2)
        else:
            txt += txt_reg_keymap % (temp1, txt_className, temp2)
        
        #-----
        textObj = bpy.data.texts.new('z_AddonTemplate')
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
        row.label('(Some options can be multi-selected with Shift-Click)')
        
        layout.separator()
        layout.prop(self, 'p_name')
        row = layout.row(align = True)
        #row.alignment = 'CENTER'
        col = row.column(align = True)
        col.label("            When above name is 'Addon Template'...")
        col.label("                ClassName = 'AddonTemplateOperator'")
        col.label("                bl_idname = 'addongen.addon_template_operator'")
        
        layout.label('Operator ' + ('-' * 300))
        split = layout.split(0.2)
        col_L = split.column()
        col_L.alignment = 'RIGHT'
        col_L.label('bl_options')
        col_L.label('Use Operator Props')
        col_R = split.column()
        col_R.row().prop(self, 'p_opOptions')
        col_R.prop(self, 'isUseOpProps')
        
        layout.separator()
        layout.label('Panel ' + ('-' * 300))
        split = layout.split(0.2)
        col_L = split.column()
        col_L.alignment = 'RIGHT'
        col_L.label('UsePanel')
        col_L.label('Place')
        col_L.label('bl_options') 
        col_R = split.column()
        col_R.prop(self, 'isUsePanel')
        col_R.prop(self, 'p_panelSpaceRegion', text = '')
        row = col_R.split(0.6).row().prop(self, 'p_panelOptions')

        layout.separator()
        layout.label('Misc ' + ('-' * 300))
        split = layout.split(0.2)
        col_L = split.column()
        col_L.alignment = 'RIGHT'
        col_L.label('GPL Notice')
        col_L.label('Scene Props')
        col_L.label('Menu Func')
        col_L.label('Keymap')
        col_R = split.column()
        col_R.prop(self, 'isUseGPLNotice')
        col_R.prop(self, 'isUseSceneProps')
        col_R.prop(self, 'isUseMenuFunc')
        col_R.prop(self, 'isUseKeymap')
        #---
        layout.separator()
    
        
        
####################################################################################
class AddSnippetOp_Props(bpy.types.Operator):
    """Add property line to current cursor"""
    bl_idname = "chichige.add_snippet_operator_props"
    bl_label = "Add Snippet Operator - Props"
    bl_options = {'INTERNAL', 'UNDO'}
    
    type = StringProperty(name="OperatorType")
    
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
        
        subText += "" if not pps.isAddName    else (", " if subText else "") + 'name = ""'
        subText += "" if not pps.isAddDesc    else (", " if subText else "") + 'description = ""'
    
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

####################################################################################        
class AddSnippetOp_Samples(bpy.types.Operator):
    """Add sample code to current cursor"""
    bl_idname = "chichige.add_snippet_operator_samples"
    bl_label = "Add Snippet Operator - Samples"
    bl_options = {'INTERNAL', 'UNDO'}
        
    def execute(self, context):
        pps = context.scene.chichige_add_snippet_props
        
        txt = ""
        if pps.snippetSample == "OperatorClass":
            #txt_operator % (className, "ToolTip", bl_idname, bl_label, \t(bl_options)\n\n, (props)) 
            txt = txt_operator % ("SampleOperator", '"ToolTip"', "addongen.sample_operator", "Sample Operator", "    bl_options = {'REGISTER'}\n\n", "")
            
        elif pps.snippetSample == "PanelClass":
            #txt_panel % (ClassName, "ToolTip", bl_idname, bl_label, SpaceRegion, bl_context, OperatorClassName)                    
            if pps.panelSpaceRegion.startswith("PROP"):
                temp = pps.panelSpaceRegion.split("-")[2].replace("_", "").upper()
            else:
                temp = pps.panelSpaceRegion.split("-")[0].replace("_", "")
            txt_blIdname_p = temp + '_PT_sample_operator'
            txt_blOptions_p = "#bl_options =  {'DEFAULT_CLOSED'}\n"
            
            temp = pps.panelSpaceRegion.split("-")
            txt_space_p = "bl_space_type = '%s'\n" % temp[0]
            txt_region_p = "    bl_region_type = '%s'" % temp[1]
            txt_context_p = "" if len(temp) < 3 else "\n    bl_context = '%s'" % temp[2]
            txt = txt_panel % ("SamplePanel", '"ToolTip"', txt_blIdname_p, "Sample Panel", txt_blOptions_p, 
                                                                txt_space_p + txt_region_p + txt_context_p, "SampleOperator")
        elif pps.snippetSample == "Props(Operator)":
            txt = txt_props
        
        elif pps.snippetSample == "PropGroup":
            txt = "class MySceneProps(bpy.types.PropertyGroup):\n" + txt_props
            txt += "bpy.utils.register_class(MySceneProps)\n"
            txt += "bpy.types.Scene.sample_code_props = PointerProperty(type = MySceneProps)\n"
        
        elif pps.snippetSample == "CollectProp":
            txt = txt_collectionProp
            
        elif pps.snippetSample == "bl_info":
            txt = txt_blInfo % "Sample Addon"
        
        elif pps.snippetSample == "MenuFunc":
            txt += "def menu_func(self, context):\n"
            txt += "    self.layout.operator(SampleOperator.bl_idname, icon = 'PLUGIN')\n"
            txt += "#bpy.types.VIEW3D_MT_object.append(menu_func) #put in register()\n"
            txt += "#bpy.types.VIEW3D_MT_object.remove(menu_func) #put in unregister()\n"

        elif pps.snippetSample == "Register" or pps.snippetSample == "RegKeymap":
            temp1 = "bpy.utils.register_class(SampleOperator)"
            temp1 += "\n    #bpy.utils.register_class(SamplePanel)"
            temp1 += "\n    #bpy.types.VIEW3D_MT_object.append(menu_func)"
            temp2 = "bpy.utils.unregister_class(SampleOperator)"
            temp2 += "\n    #bpy.utils.unregister_class(SamplePanel)"
            temp2 += "\n    #bpy.types.VIEW3D_MT_object.remove(menu_func)"
            
            if pps.snippetSample == "Register":
                txt += txt_reg % (temp1, temp2)
            else:
                txt += txt_reg_keymap % (temp1, 'SampleOperator', temp2)
            
        elif pps.snippetSample == "GPL":
            txt = txt_GPL
        
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


####################################################################################        
#TODO: UILayout method sample
#TODO : Clear all, def, full Button
class BookmarkOp(bpy.types.Operator):
    """ToolTip"""
    bl_idname = "addongen.sample_operator"
    bl_label = "Sample Operator"
    bl_options = {'REGISTER'}

    type = StringProperty()
    bmText = StringProperty()
    removeID = IntProperty()
    
    def execute(self, context):
        pps = context.scene.chichige_add_snippet_props
        
        if self.type == "ADD":
            pps.bookmarks.add()
        elif self.type == "REMOVE":
            pps.bookmarks.remove(self.removeID)
        elif self.type == "GO":
            sd = context.space_data
            findText= sd.find_text
            matchCase = sd.use_match_case
            findAll = sd.use_find_all
            findWrap = sd.use_find_wrap
            
            sd.find_text = self.bmText
            sd.use_match_case = False
            sd.use_find_all = False
            sd.use_find_wrap = True
            try:           
                bpy.ops.text.find()
            except RuntimeError as e:
                if not str(e).startswith("Error: Text not found:"):
                    raise e
                else:
                    self.report({'WARNING'}, "Bookmark text not found")
            finally:
                sd.find_text = findText
                sd.use_match_case = matchCase
                sd.use_find_all = findAll
                sd.use_find_wrap = findWrap          
        
        return {'FINISHED'}
    

####################################################################################
class AddSnippetPanel(bpy.types.Panel):
    """ToolTip of AddonTemplatePanel"""
    bl_idname = "TEXTEDITOR_PT_add_snippet_panel"
    bl_label = "Add Snippets"
    
    bl_space_type = 'TEXT_EDITOR'
    bl_region_type = 'UI'
    
    def draw(self, context):
        layout = self.layout
        pps = context.scene.chichige_add_snippet_props
        
        layout.prop(pps, 'isClipboard')
        layout.label('Properties' + '-' * 80)
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
        split = box.split(0.18)
        split.label('options')   
        row = split.row()
        row.prop(pps, 'propOptions')
        split = box.split(0.18)
        split.label('subtype')   
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
        split = layout.split(0.5)
        row = split.row(align = True)
        row.prop(pps, 'isAddEnumFlag')
        row.operator(AddSnippetOp_Props.bl_idname, text = "Enum").type = 'Enum'
        split.operator(AddSnippetOp_Props.bl_idname, text = "Collection").type = 'Collection'
        split.operator(AddSnippetOp_Props.bl_idname, text = "Pointer").type = 'Pointer'
        
        #-----------
        layout.label('CodeSamples' + '-' * 80)
        split = layout.split(0.85)
        split.prop(pps, 'snippetSample', text="")
        row = split.row()
        row.enabled = pps.snippetSample != 'SEPARATOR'
        row.operator(AddSnippetOp_Samples.bl_idname, text = ">>")
        split = layout.split(0.8)
        row = split.row()
        row.enabled = pps.snippetSample == 'PanelClass'
        row.prop(pps, "panelSpaceRegion", text = "PanelSpace")
 
        #-------------
        layout.separator()
        box = layout.box()
        headRow = box.row(align = True)
        if not pps.isUseBookmark:
            headRow.prop(pps, "isUseBookmark", text = "", icon = 'TRIA_RIGHT', emboss = False)
            headRow.label('Bookmarks' + '-' * 50) 
        else:
            headRow.prop(pps, "isUseBookmark", text = "", icon = 'TRIA_DOWN', emboss = False)
            headRow.label('Bookmarks' + '-' * 40)
            row = headRow.row() 
            row.enabled = len(pps.bookmarks) < 20
            row.operator(BookmarkOp.bl_idname, text = "", icon = "ZOOMIN").type = "ADD"
            
            col = box.column(align = True)
            for i in range(len(pps.bookmarks)):
                bm = pps.bookmarks[i]
                
                if i % 5 == 0 and i != 0:
                    col.separator()
                row = col.row(align = True)
                                
                opProps = row.operator(BookmarkOp.bl_idname, text = "", icon = 'PANEL_CLOSE', emboss = False)
                opProps.type = "REMOVE"
                opProps.removeID = i
 
                row.prop(bm, "bmText", text = "")
                
                row = row.row()
                row.enabled = bm.bmText.strip() != ""
                opProps = row.operator(BookmarkOp.bl_idname, text = "", icon = 'VIEWZOOM')
                opProps.type = 'GO'
                opProps.bmText = bm.bmText
                
       

####################################################################################
# Scene item funcs, props ----

def getItems_propOptions(self, context):
    return convertToItems(['HIDDEN', 'SKIP_SAVE', 'ANIMATABLE', 'LIBRARY_EDITABLE'])   

def getItems_propSubtype(self, context):
    return convertToItems(['-- Subtype --', 'UNSIGNED', 'PERCENTAGE', 'FACTOR', 'ANGLE', 'TIME', 'DISTANCE', 'NONE'])   

def getItems_propVecSubtype(self, context):
    return convertToItems(['-- VecSub --', 'COLOR', 'TRANSLATION', 'DIRECTION', 'VELOCITY', 'ACCELERATION', 'MATRIX', 'EULER', 'QUATERNION', 'AXISANGLE', 'XYZ', 'COLOR_GAMMA', 'LAYER', 'NONE'])

def getItems_floatUnit(self, context):
    return convertToItems(['-- Unit --', 'NONE', 'LENGTH', 'AREA', 'VOLUME', 'ROTATION', 'TIME', 'VELOCITY', 'ACCELERATION'])
 
def getItems_stringSubtype(self, context):
    return convertToItems(['-- Subtype --', 'FILE_PATH', 'DIR_PATH', 'FILENAME', 'NONE'])

def convertToItems(itemsList):
    retVal = []
    for itm in itemsList:
        if itm.startswith("-"):
            retVal.append(('NO', itm, ""))
        else: 
            retVal.append((itm, itm.replace("_", " ").title().replace(" ", ""), ""))
    return retVal

class BookmarkCollection(bpy.types.PropertyGroup):
    bmText = bpy.props.StringProperty(name="Test Prop")
    
class AddSnippetProps(bpy.types.PropertyGroup):
    isAddRefComment = BoolProperty(name = "#Ref",       description = "Add reference line as comment", default = False)
    isAddPrefix =     BoolProperty(name = "prefix",     description="Add bpy.props at first",      default = True)
    isAddName =       BoolProperty(name = "name",       description = "Add name",                  default = True)
    isAddDesc =       BoolProperty(name = "desc",       description = "Add description",           default = True)
    isAddDefault =    BoolProperty(name = "default",    description = "Add default",               default = True)
    isAddMinMax =     BoolProperty(name = "min,max",     description = "Add min and max (maxlen for string)", default = True)
    isAddSoftMinMax = BoolProperty(name = "soft_min,max", description = "Add soft_min and soft_max", default = False)
    isAddStep =       BoolProperty(name = "step",       description = "Add step",                  default = False)
    isAddSize =       BoolProperty(name = "size",       description = "Add size",                  default = False)
    isAddUpdate =     BoolProperty(name = "update",     description = "Add update",                default = False)
    
    propOptions =    EnumProperty(items = getItems_propOptions,     name = "PropOptions",       description = "", options = {'ENUM_FLAG'})
    propSubtype =    EnumProperty(items = getItems_propSubtype,     name = "PropSubtype",       description = "")
    propVecSubtype = EnumProperty(items = getItems_propVecSubtype,  name = "PropVecSubtype",    description = "")

    isAddFloatPrec = BoolProperty(name = "precision", description = "Add precision", default = False)
    floatUnit =      EnumProperty(items = getItems_floatUnit,       name = "FloatUnit",         description = "")
    stringSubtype =  EnumProperty(items = getItems_stringSubtype,   name = "StringSubtype",     description = "")
    isAddEnumFlag =  BoolProperty(name = "ENUM_FLAG", description = "Add ENUM_FLAG to options", default = False)
    
    isClipboard = BoolProperty(name = "Copy to Clipboard instead of Insertion")
    snippetSample = EnumProperty(items = [('OperatorClass',   'Operator Class', ''),
                                          ('PanelClass',      'Panel Class', ''),
                                          ('Props(Operator)', 'Properties (Operator)', ''),
                                          ('PropGroup',       'PropertyGroup (Scene)', ''),
                                          ('CollectProp',     'CollectionProp (Scene)', ''),
                                          ('SEPARATOR',       '-' * 30, ''),
                                          ('bl_info',         'bl_info', ''),
                                          ('MenuFunc',        'Menu Function', ''),
                                          ('Register',        'Register', ''),
                                          ('RegKeymap',       'Reg with Keymap', ''),
                                          ('GPL',             'GPL Block', '')],
                                 name = "Snippet Code Samples")
    panelSpaceRegion = EnumProperty(items = getSpaceRegionItems,
                                      name="Panel's SpaceRegion", 
                                      description="Panel's bl_space_type, bl_region_type and bl_context")
    isUseBookmark = BoolProperty()                             
    bookmarks = CollectionProperty(type = BookmarkCollection)

bpy.utils.register_class(BookmarkCollection)
bpy.utils.register_class(AddSnippetProps)
bpy.types.Scene.chichige_add_snippet_props = PointerProperty(type = AddSnippetProps)


####################################################################################        

def menu_func(self, context):
    self.layout.operator(AddonTemplateGeneratorOp.bl_idname, icon = 'PLUGIN')

# Registration---_------------------------------------------
def register():
    bpy.utils.register_class(AddonTemplateGeneratorOp)
    bpy.utils.register_class(AddSnippetOp_Props)
    bpy.utils.register_class(AddSnippetOp_Samples)
    bpy.utils.register_class(BookmarkOp)
    bpy.utils.register_class(AddSnippetPanel)
    bpy.types.TEXT_MT_templates.append(menu_func)

def unregister():
    bpy.utils.unregister_class(AddonTemplateGeneratorOp)
    bpy.utils.unregister_class(AddSnippetOp_Props)
    bpy.utils.unregister_class(AddSnippetOp_Samples)
    bpy.utils.unregister_class(BookmarkOp)
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
    my_bool =     BoolProperty(name="", description="", default=False)
    my_boolVec =  BoolVectorProperty(name="", description="", default=(False, False, False))
    my_float =    FloatProperty(name="", description="", default=0.0)
    my_floatVec = FloatVectorProperty(name="", description="", default=(0.0, 0.0, 0.0)) 
    my_int =      IntProperty(name="", description="", default=0)  
    my_intVec =   IntVectorProperty(name="", description="", default=(0, 0, 0))
    my_string =   StringProperty(name="String Value", description="", default="", maxlen=0)
    my_enum =     EnumProperty(items = [('ENUM1', 'Enum1', 'enum prop 1'), 
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
        self.report({'INFO'}, "Test Operator")
        return {'FINISHED'}
    
    #def invoke(self, context, event):
    #    wm.modal_handler_add(self)
    #    return {'RUNNING_MODAL'}  
    #    return wm.invoke_porps_dialog(self)
    #def modal(self, context, event):
    #def draw(self, context, event):

"""
#txt_panel % (ClassName, "ToolTip", bl_idname, bl_label, SpaceRegion, bl_context, OperatorClassName)
txt_panel = """\
class %s(bpy.types.Panel):
    ""%s""
    bl_idname = "%s"
    bl_label = "%s"
    %s
    %s
    
    def draw(self, context):
        layout = self.layout
        layout.operator(%s.bl_idname, text = "Test", icon = 'BLENDER')

"""

txt_reg = """\
def register():
    %s

def unregister():
    %s
    
if __name__ == "__main__":
    register()
"""

txt_reg_keymap = """\
# store keymaps here to access after registration
addon_keymaps = []

def register():
    %s
    
    # handle the keymap
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
    kmi = km.keymap_items.new(%s.bl_idname, 'SPACE', 'PRESS', ctrl=True, shift=True)
    #kmi.properties.prop1 = 'some'
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


txt_collectionProp = """\
class MySceneItems(bpy.types.PropertyGroup):
    name = bpy.props.StringProperty(name="Test Prop", default="Unknown")
    value = bpy.props.IntProperty(name="Test Prop", default=22)

bpy.utils.register_class(MySceneItems)
bpy.types.Scene.sample_code_items = bpy.props.CollectionProperty(type = MySceneItems)

my_item = bpy.context.scene.sample_code_items.add()
my_item.name = "Spam"
my_item.value = 1000

my_item = bpy.context.scene.sample_code_items.add()
my_item.name = "Eggs"
my_item.value = 30
"""
