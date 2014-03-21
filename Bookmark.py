bl_info = {
    "name": "Bookmark",
    "author": "chichige-bobo",
    "version": (1, 0, 0),
    "blender": (2, 70, 0),
    "location": "TextEditor > PropertiesBar > ookmarks",
    "description": "Jump to texts",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Development"}

import bpy
from bpy.props import BoolProperty, IntProperty, StringProperty, EnumProperty, PointerProperty, CollectionProperty

#################################################################################### 
class ChichigeBookmarkOp(bpy.types.Operator):
    """Jump to where the text is written"""
    bl_idname = "chichige.bookmark_operator"
    bl_label = "Bookmark Operator"
    bl_options = {'INTERNAL'}

    type = EnumProperty(items = [('ADD', 'Add', 'Add new bookmark'), 
                                 ('REMOVE', 'Remove', 'Remove a bookmark'),
                                 ('GO', 'Go', 'Find the text and go to there'),
                                 ('SHIFT_DOWN', 'SHiftDown', 'Move entire bookmarks down a row'),
                                 ('SHIFT_UP', 'ShiftUp', 'Move entrie bookmaks up a row')])
    bmText = StringProperty()
    removeID = IntProperty()
    
    def execute(self, context):
        pps = context.scene.chichige_bookmark_props
        
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
            sd.use_match_case = True
            sd.use_find_all = pps.isBookmarkFindAll
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
        
        elif self.type == "SHIFT_DOWN": 
            if len(pps.bookmarks) < 20 and (len(pps.bookmarks) > 0 and pps.bookmarks[-1].bmText != ""):
                pps.bookmarks.add()
                 
            for i in range(len(pps.bookmarks) - 1, -1, -1):
                if i != 0:
                    pps.bookmarks[i].bmText = pps.bookmarks[i - 1].bmText
                else:
                    pps.bookmarks[i].bmText = ""

        elif self.type == "SHIFT_UP":  
            for i in range(len(pps.bookmarks)):
                if i != len(pps.bookmarks) - 1:
                    pps.bookmarks[i].bmText = pps.bookmarks[i + 1].bmText
                else:
                    pps.bookmarks.remove(i)
                               
        return {'FINISHED'}
    
###########################################################                
class ChichigeBookmarkPanel(bpy.types.Panel):
    """Panel for Bookmarks"""
    bl_idname = "TEXTEDITOR_PT_chichige_bookmark_panel"
    bl_label = "Bookmarks"
    bl_options =  {'DEFAULT_CLOSED'}
    
    bl_space_type = 'TEXT_EDITOR'
    bl_region_type = 'UI'
    
    def draw(self, context):
        layout = self.layout
        pps = context.scene.chichige_bookmark_props

        col = layout.column(align = True)
        row = col.row()
        split = row.split(0.05)
        split.label("")
        row = split.split(0.9).row()
        row.prop(pps, "isBookmarkFindAll")
        row.operator(ChichigeBookmarkOp.bl_idname, text = "", icon = "MOVE_UP_VEC").type = "SHIFT_UP"
        row.operator(ChichigeBookmarkOp.bl_idname, text = "", icon = "MOVE_DOWN_VEC").type = "SHIFT_DOWN"
        row.separator()
        row = row.row()
        row.enabled = len(pps.bookmarks) < 20
        row.operator(ChichigeBookmarkOp.bl_idname, text = "New", icon = "ZOOMIN").type = "ADD"

        col.separator()
        for i in range(len(pps.bookmarks)):
            bm = pps.bookmarks[i]
            
            if i % 5 == 0 and i != 0:
                col.separator()
            row = col.row(align = True)
                            
            opProps = row.operator(ChichigeBookmarkOp.bl_idname, text = "", icon = 'PANEL_CLOSE', emboss = False)
            opProps.type = "REMOVE"
            opProps.removeID = i
 
            row.prop(bm, "bmText", text = "")
            
            row = row.row()
            row.enabled = bm.bmText.strip() != ""
            opProps = row.operator(ChichigeBookmarkOp.bl_idname, text = "", icon = 'VIEWZOOM')
            opProps.type = 'GO'
            opProps.bmText = bm.bmText
        
            
            
####################################################################################
class ChichigeBookmarkCollection(bpy.types.PropertyGroup):
    bmText = bpy.props.StringProperty(name="BookmarkText")
    
class ChichigeBookmarkProps(bpy.types.PropertyGroup):
    isBookmarkFindAll = BoolProperty(name = "Find All", description = "Search All Files for the Bookmark")                             
    bookmarks = CollectionProperty(type = ChichigeBookmarkCollection)

####################################################################################        

# Registration---_------------------------------------------
def register():
    bpy.utils.register_class(ChichigeBookmarkCollection)
    bpy.utils.register_class(ChichigeBookmarkProps)
    bpy.types.Scene.chichige_bookmark_props = PointerProperty(type = ChichigeBookmarkProps)
    bpy.utils.register_class(ChichigeBookmarkOp)
    bpy.utils.register_class(ChichigeBookmarkPanel)

def unregister():
    bpy.utils.unregister_class(ChichigeBookmarkCollection)
    bpy.utils.unregister_class(ChichigeBookmarkProps)
    bpy.utils.unregister_class(ChichigeBookmarkOp)
    bpy.utils.unregister_class(ChichigeBookmarkPanel)
    
if __name__ == "__main__":
    register()
