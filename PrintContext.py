bl_info = {
    "name": "Print Context",
    "author": "chichige-bobo",
    "version": (1, 0),
    "blender": (2, 69, 0),
    "location": "SpaceBar > 'Print Context', PythonConsole > Console > Print Context, TextEditor > View > Print Context",
    "description": "Print Context Info to the System Console",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Development"}
    
##########################################################################
# Have you ever annoyed that C.area always shows context of PythonConsole? This addon for you. 
# Print Context - Area : Prints area specific context info where mouse hovered when space bar pressed)  
# Print Context - General : This info can be retrieved from PythonConsole.
#
# Spacebar not worked on PythonConsole and TextEditor. So, use menu (Console and View)
# to access this operator. 
#
# Note about Area.spaces : if user changes area type, it is appended to the spaces.
# e.g. If user changes 3DView to Outliner, the spaces become [0] = Outliner, [1] = 3DView.
# So, this addon doesn't care it
###########################################################################

import bpy

class PrintContextOperator_Base(bpy.types.Operator):
    
    def refine(self, data):
        txt = str(data)
        return txt.replace('<bpy_struct, ', '').split(' at ')[0].replace('>', '').replace('<class ', '')
    
    def len(self, data):
        if data is None:
            return 'None'
        else:
            return len(data)

#######################################    
class PrintContextOperator_General(PrintContextOperator_Base):
    """Print Context Info to the Console"""
    bl_idname = "object.print_context_operator_general"
    bl_label = "Print Context - General"
        
    def execute(self, context):
        print('\n--------------- Context Info - General ---------------------')
        print(' len(C.window_manager.windows) = ', len(context.window_manager.windows))
        print(' C.window_manager = ', self.refine(context.window_manager))
        print(' C.window =       ' , self.refine(context.window))
        print(' C.window.id_data=' , context.window.id_data)
        print(' C.window.screen =' , self.refine(context.window.screen))
        print(' C.screen =       ' , self.refine(context.screen))
        print(' C.scene =        ' , self.refine(context.scene))
        print(' C.mode =         ' , context.mode)
        self.printScreenAreas(context.screen.areas)
        print('--------------')
        print(' C.object =         ', self.refine(context.object))
        print(' C.active_object =  ', self.refine(context.active_object))
        print(' C.active_base =    ', self.refine(context.active_base))
        print(' C.active_bone =    ', self.refine(context.active_bone))
        print(' C.active_operator =', self.refine(context.active_operator))
        print(' C.active_pose_bone=', self.refine(context.active_pose_bone))
        print(' C.edit_object =    ', self.refine(context.edit_object))
        print(' C.sculpt_object =  ', self.refine(context.sculpt_object))
        print(' C.image_paint_object =  ', self.refine(context.image_paint_object))
        print(' C.weight_paint_object = ', self.refine(context.weight_paint_object))
        print(' C.particle_edit_object =', self.refine(context.particle_edit_object))
        print('---------------')
        print(' len(C.selectable_bases) =       ', self.len(context.selectable_bases))
        print(' len(C.selectable_objects) =     ', self.len(context.selectable_objects))
        print(' len(C.selected_bases) =         ', self.len(context.selected_bases))
        print(' len(C.selected_bones) =         ', self.len(context.selected_bones))
        print(' len(C.selected_editable_bases) =   ', self.len(context.selected_editable_bases))
        print(' len(C.selected_editable_bones) =   ', self.len(context.selected_editable_bones))
        print(' len(C.selected_editable_objects) = ', self.len(context.selected_editable_objects))
        print(' len(C.selected_editable_sequences)=', self.len(context.selected_editable_sequences))
        print(' len(C.selected_objects) =       ', self.len(context.selected_objects))
        print(' len(C.selected_pose_bones) =    ', self.len(context.selected_pose_bones))
        print(' len(C.selected_sequences) =     ', self.len(context.selected_bones))
        print('---------------')
        print(' len(C.sequences) =              ', self.len(context.sequences))
        print(' len(C.visible_bases) =     ', self.len(context.visible_bases))
        print(' len(C.visible_bones) =     ', self.len(context.visible_bones))
        print(' len(C.visible_objects) =   ', self.len(context.visible_objects))
        print(' len(C.visible_pose_bones) =', self.len(context.visible_pose_bones))
        print(' len(C.visible_bones) =     ', self.len(context.visible_bones))

        #print('C.blend_data = ', context.blend_data) #C.blend_data == D
        return {'FINISHED'}

    def printScreenAreas(self, areas):
        if areas is None:
            print(' C.screen.areas = None')
        else:
            print(' C.screen.areas = ')
            for i in range(len(areas)):
                print('\tareas[' + str(i) + '].type = ', areas[i].type) 

############################################    
class PrintContextOperator_Area(PrintContextOperator_Base):
    """Print Area Dependent Context Info to the Console"""
    bl_idname = "object.print_context_operator_area"
    bl_label = "Print Context - Area"

    def execute(self, context):
        print('\n--------------- Context Info - Area ---------------------')
        print(' (Below is just a bit of props. See the reference to explore more.)')
        print('')
        print(' C.mode =          ', self.refine(context.mode))
        print(' C.space_data =    ', self.refine(context.space_data))
        print(' C.space_data.type=', self.refine(context.space_data.type))
        sd = context.space_data
        if sd.type == 'SEQUENCE_EDITOR':
            print(' | C.space_data.display_mode = ', sd.display_mode)
            print(' | C.space_data.overlay_type = ', sd.overlay_type) 
            print(' | C.space_data.proxy_render_size=', sd.proxy_render_size) 
            print(' | C.space_data.view_type =    ', sd.view_type) 
        elif sd.type == 'OUTLINER':
            print(' | C.space_data.display_mode = ', sd.display_mode)
        elif sd.type == 'NLA_EDITOR':
            print(' | C.space_data.auto_snap = ', sd.auto_snap)
        elif sd.type == 'CONSOLE':
            print(' | C.space_data.font_size = ', sd.font_size)
            print(' | C.space_data.language = ', sd.language)
        elif sd.type == 'TEXT_EDITOR':
            print(' | C.space_data.text =              ', self.refine(sd.text))
            print(' | C.space_data.show_line_numbers = ', sd.show_line_numbers)
            print(' | C.space_data.show_word_wrap =    ', sd.show_word_wrap)
            print(' | C.space_data.show_syntax_highlight=', sd.show_syntax_highlight)
        elif sd.type == 'PROPERTIES':
            print(' | C.space_data.context =       ', sd.context)
            print(' | C.space_data.texture_context=', sd.texture_context)
        elif sd.type == 'VIEW_3D':
            print(' | C.space_data.local_view =     ', self.refine(sd.local_view))
            print(' | C.space_data.pivot_point=     ', sd.pivot_point)
            print(' | C.space_data.show_manipulator=', sd.show_manipulator)
            print(' | C.space_data.transform_orientation=', sd.transform_orientation)
            print(' | C.space_data.viewport_shade = ', sd.viewport_shade)
            print(' | C.space_data.region_quadview =', self.refine(sd.region_quadview))
            print(' | C.space_data.region_3d =      ', self.refine(sd.region_3d))
            print(' | | C.space_data.region_3d.is_perspective = ', sd.region_3d.is_perspective)
            print(' | | C.space_data.region_3d.view_perspective=', sd.region_3d.view_perspective)
        elif sd.type == 'CLIP_EDITOR':
            print(' | C.space_data.clip =         ', self.refine(sd.clip))
            print(' | C.space_data.mask_draw_type=', sd.mask_draw_type)
            print(' | C.space_data.mode =         ', sd.mode)
            print(' | C.space_data.pivot_point =  ', sd.pivot_point)
            print(' | C.space_data.show_names =   ', sd.show_names)
            print(' | C.space_data.view =         ', sd.view)
        elif sd.type == 'GRAPH_EDITOR':
            print(' | C.space_data.auto_snap = ', sd.auto_snap)
            print(' | C.space_data.mode =      ', sd.mode)
            print(' | C.space_data.dopesheet = ', self.refine(sd.dopesheet))
            print(' | | C.space_data.dopesheet.show_only_selected=', sd.dopesheet.show_only_selected)            
            print(' | | C.space_data.dopesheet.show_hidden =      ', sd.dopesheet.show_hidden)
            print(' | | C.space_data.dopesheet.show_materials =   ', sd.dopesheet.show_materials)
            print(' | | C.space_data.dopesheet.show_textures =    ', sd.dopesheet.show_textures)
        elif sd.type == 'INFO':
            print(' | C.space_data.show_report_info =     ', sd.show_report_info)
            print(' | C.space_data.show_report_operator = ', sd.show_report_operator)
        elif sd.type == 'LOGIC_EDITOR':
            print(' | C.space_data.show_actuators_active_object = ', sd.show_actuators_active_object)
            print(' | C.space_data.show_sensors_active_object   = ', sd.show_sensors_active_object)
        elif sd.type == 'TIMELINE':
            print(' | C.space_data.show_cache = ', sd.show_cache)
            print(' | C.space_data.cache_particles = ', sd.cache_particles)
        elif sd.type == 'IMAGE_EDITOR':
            print(' | C.space_data.draw_channels = ', sd.draw_channels)
            print(' | C.space_data.image =         ', self.refine(sd.image))
            print(' | C.space_data.mask =          ', self.refine(sd.mask))
            print(' | C.space_data.mask_draw_type =', sd.mask_draw_type)
            print(' | C.space_data.mode =          ', sd.mode)
            print(' | C.space_data.pivot_point =   ', sd.pivot_point)
            print(' | C.space_data.show_render =   ', sd.show_render)
            print(' | C.space_data.show_paint =    ', sd.show_paint)
            print(' | C.space_data.show_uvedit =   ', sd.show_uvedit)
            print(' | C.space_data.image_user =    ', self.refine(sd.image_user))
            print(' | | C.space_data.image_user.frame_offset = ', sd.image_user.frame_offset)
            print(' | | C.space_data.image_user.use_cyclic = ', sd.image_user.use_cyclic)
            print(' | C.space_data.uv_editor =     ', self.refine(sd.uv_editor))
            print(' | | C.space_data.uv_editor.edge_draw_type = ', sd.uv_editor.edge_draw_type)
            print(' | | C.space_data.uv_editor.show_other_objects = ', sd.uv_editor.show_other_objects)
            print(' | | C.space_data.uv_editor.sticky_select_mode = ', sd.uv_editor.sticky_select_mode)
            print(' | | C.space_data.uv_editor.use_snap_to_pixels = ', sd.uv_editor.use_snap_to_pixels)
        elif sd.type == 'FILE_BROWSER':
            print(' | C.space_data.active_operator=', sd.active_operator)
            print(' | C.space_data.operator       = ', sd.operator)
            print(' | C.space_data.params         = ', self.refine(sd.params))
            print(' | | C.space_data.params.display_type = ', sd.params.display_type)
            print(' | | C.space_data.params.filename =     ', sd.params.filename)
            print(' | | C.space_data.params.sort_method =  ', sd.params.sort_method)
        elif sd.type == 'USER_PREFERENCES':
            print(' | C.space_data.filter_text =      ', sd.filter_text)
            print(' | C.window_manager.addon_search = ', context.window_manager.addon_search)
        elif sd.type == 'DOPESHEET_EDITOR':
            print(' | C.space_data.action =    ', self.refine(sd.action))
            print(' | C.space_data.auto_snap = ', sd.auto_snap)
            print(' | C.space_data.mode =      ', sd.mode)
            print(' | C.space_data.dopesheet = ', self.refine(sd.dopesheet))
            print(' | | C.space_data.dopesheet.show_only_selected=', sd.dopesheet.show_only_selected)            
            print(' | | C.space_data.dopesheet.show_hidden =      ', sd.dopesheet.show_hidden)
            print(' | | C.space_data.dopesheet.show_materials =   ', sd.dopesheet.show_materials)
            print(' | | C.space_data.dopesheet.show_textures =    ', sd.dopesheet.show_textures)
        elif sd.type == 'NODE_EDITOR':
            print(' | C.space_data.backdrop_zoom = ', sd.backdrop_zoom)
            print(' | C.space_data.edit_tree =     ', self.refine(sd.edit_tree))
            print(' | C.space_data.node_tree =     ', self.refine(sd.node_tree))
            print(' | C.space_data.shader_type =   ', sd.shader_type)
            print(' | C.space_data.texture_type =  ', sd.texture_type)
            print(' | C.space_data.tree_type =     ', sd.tree_type)
       
        print('')
        print(' C.region =      ', self.refine(context.region))
        print(' C.region.id =   ', self.refine(context.region.id))
        print(' C.region.type = ', self.refine(context.region.type))
        print(' C.region_data = ', self.refine(context.region_data))
        print('')
        print(' C.area =         ', self.refine(context.area))
        print(' C.area.type =    ', self.refine(context.area.type))
        self.printAreaRegions(context.area.regions)
        print('')
        self.printConsoleCompatibleAreaIndex(context)
        return {'FINISHED'}
    
    def printAreaRegions(self, regions):
        if regions is None:
            print(' C.area.regions = None')
        else:
            print(' C.area.regions = ')
            for r in regions:
                print('\t[id =' + (' ' if r.id < 10 else ''), r.id, ', type =', r.type, ']') 

    def printConsoleCompatibleAreaIndex(self, context):
        areas = context.screen.areas
        if areas is not None: 
            for i in range(len(areas)):
                if areas[i] == context.area:
                    break
            consoleText = 'C.screen.areas[' + str(i) + '].spaces.active.' 
            print(" Use '" + consoleText + "' to test props at Console")
         
        context.window_manager.clipboard = consoleText
        self.report({'INFO'}, "Text has been copied to clipboard.")

###################################################

def menu_func(self, context):
    self.layout.separator()
    self.layout.operator(PrintContextOperator_Area.bl_idname, icon = 'WORDWRAP_ON')
       
def register():
    bpy.utils.register_class(PrintContextOperator_General)
    bpy.utils.register_class(PrintContextOperator_Area)
    bpy.types.CONSOLE_MT_console.append(menu_func)
    bpy.types.TEXT_MT_view.append(menu_func)
    
    #below were always be 'WINDOW'. never be 'HEADER' or 'UI' in my experiment
    #bpy.types.CONSOLE_HT_header.append(menu_func)
    #bpy.types.TEXT_HT_header.append(menu_func)
    #bpy.types.TEXT_PT_properties.append(menu_func)
    
def unregister():
    bpy.utils.unregister_class(PrintContextOperator_General)
    bpy.utils.unregister_class(PrintContextOperator_Area)
    bpy.types.CONSOLE_MT_console.remove(menu_func)
    bpy.types.TEXT_MT_view.remove(menu_func)
    
if __name__ == "__main__":
    register() 
