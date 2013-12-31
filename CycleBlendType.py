bl_info = {
    "name": "CycleBlendType",
    "author": "chichige-bobo",
    "version": (1, 0),
    "blender": (2, 69, 0),
    "location": "NodeEditor > Shift+PLUS/MINUS , (InternalRenderer) Properties > Texture > Shift+PLUS/MINUS",
    "description": "Cycle through blend type (and other properties)",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Node"}

###############################################################################
# Change blend type (blend mode) of MixRGB Node like Photoshop and AfterEffects!
# In addition, cycle through properties of various nodes.
# Traditional texture's blend type is also supported (in limited situation) 
##############################################################################

import bpy

class NodeAttendant:
    def __init__(self, attrName1, items1, attrName2 = None, items2 = None):
        self.attrName1 = attrName1
        self.items1 = items1
        self.attrName2 = attrName2
        self.items2 = items2
        
    #little bit complicate to deal with nodes those have two lisings. (e.g. ImageTexture, VectorTransform)
    def cycleItems(self, node, isForward):
        if not self.attrName2:
            attrName = self.attrName1  
            items = self.items1
        else:
            attrName = self.attrName1 if isForward else self.attrName2
            items = self.items1 if isForward else self.items2
            isForward = True #use backward key to forward second prop
        
        #-----------
        curIndex = -1
        curAttr = getattr(node, attrName) 
 
        for i in range(len(items)):
            if items[i] == curAttr:
                curIndex = i
                break
        
        if curIndex == -1 :
            tempStr = attrName.replace('_', ' ').title()
            self.report({'WARNING'}, 'UnexpectedError: Current ' + tempStr + ' is Unknown for Addon \'CycleBlendType\'. Operation was Aborted')
            return {'CANCELLED'}
    
        #-----------    
        if isForward:
            curIndex = curIndex + 1 if curIndex + 1 < len(items) else 0
        else:
            curIndex = curIndex - 1 if curIndex - 1 >= 0 else len(items) - 1
        setattr(node, attrName, items[curIndex])
        return {'FINISHED'}   

class NodeAttendantsManager:
    # I think items should be consistant with nodes' listing order
    _attendantsDict = {
        #Material
        'TANGENT' :         NodeAttendant('direction_type', ('UV_MAP', 'RADIAL')),
        'BSDF_GLOSSY' :     NodeAttendant('distribution',   ('GGX', 'BECKMANN', 'SHARP')),
        'BSDF_REFRACTION' : NodeAttendant('distribution',   ('GGX', 'BECKMANN', 'SHARP')),
        'BSDF_GLASS' :      NodeAttendant('distribution',   ('GGX', 'BECKMANN', 'SHARP')),
        'BSDF_TOON' :       NodeAttendant('component',      ('GLOSSY', 'DIFFUSE')),
        'SUBSURFACE_SCATTERING' : NodeAttendant('falloff',  ('GAUSSIAN', 'CUBIC', 'COMPATIBLE')),
        'BSDF_HAIR' :       NodeAttendant('component',      ('Transmission', 'Reflection')),
        'TEX_IMAGE' :       NodeAttendant('color_space',    ('NONE', 'COLOR'),
                                          'projection',     ('BOX', 'FLAT')),
        'TEX_ENVIRONMENT' : NodeAttendant('color_space',    ('NONE', 'COLOR'),
                                          'projection',     ('EQUIRECTANGULAR', 'MIRROR_BALL')),
        'TEX_SKY' :         NodeAttendant('sky_type',       ('HOSEK_WILKIE', 'PREETHAM')),
        'TEX_WAVE' :        NodeAttendant('wave_type',      ('RINGS', 'BANDS')),
        'TEX_VORONOI' :     NodeAttendant('coloring',       ('CELLS', 'INTENSITY')),
        'TEX_MUSGRAVE' :    NodeAttendant('musgrave_type',  ('HETERO_TERRAIN', 'FBM', 'HYBRID_MULTIFRACTAL', 'RIDGED_MULTIFRACTAL', 'MULTIFRACTAL')),
        'TEX_GRADIENT' :    NodeAttendant('gradient_type',  ('RADIAL', 'QUADRATIC_SPHERE', 'SPHERICAL', 'DIAGONAL', 'EASING', 'QUADRATIC', 'LINEAR')),
        'MIX_RGB' :         NodeAttendant('blend_type',     ('MIX', 'ADD', 'MULTIPLY', 'SUBTRACT', 'SCREEN', 'DIVIDE', 'DIFFERENCE', 'DARKEN', 'LIGHTEN', 'OVERLAY', 'DODGE', 'BURN', 'HUE', 'SATURATION', 'VALUE', 'COLOR', 'SOFT_LIGHT', 'LINEAR_LIGHT')),
        'MAPPING' :         NodeAttendant('vector_type',    ('TEXTURE', 'POINT', 'VECTOR', 'NORMAL')),
        'NORMAL_MAP' :      NodeAttendant('space',          ('BLENDER_WORLD', 'BLENDER_OBJECT', 'WORLD', 'OBJECT', 'TANGENT')),
        'VECT_TRANSFORM' :  NodeAttendant('convert_from',   ('CAMERA', 'OBJECT', 'WORLD'),
                                          'convert_to',     ('CAMERA', 'OBJECT', 'WORLD')),
        'MATH' :            NodeAttendant('operation',      ('ADD', 'SUBTRACT', 'MULTIPLY', 'DIVIDE', 'SINE', 'COSINE', 'TANGENT', 'ARCSINE', 'ARCTANGENT', 'POWER', 'LOGARITHM', 'MINIMUM', 'MAXIMUM', 'ROUND', 'LESS_THAN', 'GREATER_THAN', 'MODULO')),
        'VALTORGB' :        NodeAttendant('interpolation',  ('CONSTANT', 'B_SPLINE', 'LINEAR', 'CARDINAL', 'EASE')),
        'VECT_MATH' :       NodeAttendant('operation',      ('NORMALIZE', 'CROSS_PRODUCT', 'DOT_PRODUCT', 'AVERAGE', 'SUBTRACT', 'ADD')),
        'SCRIPT' :          NodeAttendant('mode',           ('INTERNAL', 'EXTERNAL')),
        
        #Composite (except above)
        'IMAGE' :           NodeAttendant('source',         ('GENERATED', 'MOVIE', 'SEQUENCE', 'FILE')),
        'MASK' :            NodeAttendant('size_source',    ('FIXED_SCENE', 'FIXED', 'SCENE')),
        'TRACKPOS' :        NodeAttendant('position',       ('ABSOLUTE_FRAME', 'RELATIVE_FRAME', 'RELATIVE_START', 'ABSOLUTE')),
        'SPLITVIEWER' :     NodeAttendant('axis',           ('X', 'Y')),
        'LEVELS' :          NodeAttendant('channel',        ('COMBINED_RGB', 'RED', 'GREEN', 'BLUE', 'LUMINANCE')),
        'COLORBALANCE' :    NodeAttendant('correction_method',('OFFSET_POWER_SLOPE', 'LIFT_GAMMA_GAIN')),
        'TONEMAP' :         NodeAttendant('tonemap_type',   ('RH_SIMPLE', 'RD_PHOTORECEPTOR')),
        'PREMULKEY' :       NodeAttendant('mapping',        ('PREMUL_TO_STRAIGHT', 'STRAIGHT_TO_PREMUL')),
        'SEPYCCA' :         NodeAttendant('mode',           ('JFIF', 'ITUBT709', 'ITUBT601')),
        'COMBYCCA' :        NodeAttendant('mode',           ('JFIF', 'ITUBT709', 'ITUBT601')),
        'BLUR' :            NodeAttendant('filter_type',    ('MITCH', 'CATROM', 'FAST_GAUSS', 'GAUSS', 'CUBIC', 'QUAD', 'TENT', 'FLAT')),
        'DILATEERODE' :     NodeAttendant('mode',           ('FEATHER', 'DISTANCE', 'THRESHOLD', 'STEP')),
        'FILTER' :          NodeAttendant('filter_type',    ('SHADOW', 'KIRSCH', 'PREWITT', 'SOBEL', 'LAPLACE', 'SHARPEN', 'SOFTEN')),
        'DEFOCUS' :         NodeAttendant('bokeh',          ('CIRCLE', 'TRIANGLE', 'SQUARE', 'PENTAGON', 'HEXAGON', 'HEPTAGON', 'OCTAGON')),
        'GLARE' :           NodeAttendant('glare_type',     ('SIMPLE_STAR', 'FOG_GLOW', 'STREAKS', 'GHOSTS'),
                                          'quality',        ('LOW', 'MEDIUM', 'HIGH')),
        'KEYING' :          NodeAttendant('feather_falloff',('LINEAR', 'SHARP', 'ROOT', 'SPHERE', 'SMOOTH')),
        'CHANNEL_MATTE' :   NodeAttendant('color_space',    ('RGB', 'HSV', 'YUV', 'YCC'),
                                          'limit_method',   ('MAX', 'SINGLE')),
        'COLOR_SPILL' :     NodeAttendant('channel',        ('R', 'G', 'B'),
                                          'limit_channel',  ('R', 'G', 'B')),
        'BOXMASK' :         NodeAttendant('mask_type',      ('NOT', 'MULTIPLY', 'SUBTRACT', 'ADD')),
        'ELLIPSEMASK' :     NodeAttendant('mask_type',      ('NOT', 'MULTIPLY', 'SUBTRACT', 'ADD')),
        'DISTANCE_MATTE' :  NodeAttendant('channel',        ('RGB', 'YCC')),
        'DOUBLEEDGEMASK' :  NodeAttendant('inner_mode',     ('ADJACENT_ONLY', 'ALL'),
                                          'edge_mode',       ('KEEP_IN', 'BLEED_OUT')),
        'SCALE' :           NodeAttendant('space',          ('RENDER_SIZE', 'SCENE_SIZE', 'ABSOLUTE', 'RELATIVE')),
        'MOVIEDISTORTION' : NodeAttendant('distortion_type',('DISTORT', 'UNDISTORT')),
        'TRANSLATE' :       NodeAttendant('wrap_axis',      ('BOTH', 'YAXIS', 'XAXIS', 'NONE')),
        'ROTATE' :          NodeAttendant('filter_type',    ('BICUBIC', 'BILINEAR', 'NEAREST')),
        'FLIP' :            NodeAttendant('axis',           ('XY', 'Y', 'X')),
        'TRANSFORM' :       NodeAttendant('filter_type',    ('BICUBIC', 'BILINEAR', 'NEAREST')),
        'STABILIZE2D' :     NodeAttendant('filter_type',    ('BICUBIC', 'BILINEAR', 'NEAREST'))
        
        #TEXTURE (I couln't find a way to manipulate texture node...)
        #'' : NodeAttendant('',()),
    }
    
    @classmethod
    def cycleItems(self, node, isForward):
        
        nodeAttendant = self._attendantsDict.get(node.type, None)
        
        #deal with some exceptional nodes
        passingNode = node
        if node.type == 'VALTORGB':
            passingNode = node.color_ramp
        elif node.type == 'IMAGE':
            if node.image:
                passingNode = node.image
            else:
                return {'CANCELLED'}
        
        if nodeAttendant:
            return nodeAttendant.cycleItems(passingNode, isForward)
        else:
            return {'CANCELLED'}


######################################################################
class CycleBlendTypeOperator_NodeEditor(bpy.types.Operator):
    """Cycle Through BlendType (and other props) in NodeEditor """
    bl_idname = "object.cycle_blend_type_operator_node_editor"
    bl_label = "Cycle Blend Type Operator - NodeEditor"
    bl_options = {'UNDO'}
        
    isForward = bpy.props.BoolProperty(name="CycleForward", description="True If Cycle Forward", default=True, subtype='NONE')

    @classmethod
    def poll(cls, context):
        #should not be accessed via spacebar from other space
        if context.area.type == 'NODE_EDITOR':
            activeSpace = context.area.spaces.active
            if activeSpace.tree_type == 'TextureNodeTree':
                return False
            elif not activeSpace.node_tree or not activeSpace.node_tree.nodes.active:
                return False
            else:
                return True
        else:
            return False
    
    def execute(self, context):
        activeNode = context.area.spaces.active.node_tree.nodes.active
        return NodeAttendantsManager.cycleItems(activeNode, self.isForward)
   
#########################################################    
class CycleBlendTypeOperator_InternalTexture(bpy.types.Operator):
    """Cycle Through BlendType of Texture of Internal Renderer"""
    bl_idname = "object.cycle_blend_type_operator_internal_texture"
    bl_label = "Cycle Blend Type Operator - InternalTexture"
    bl_options = {'UNDO'}
        
    isForward = bpy.props.BoolProperty(name="CycleForward", description="True If Cycle Forward", default=True, subtype='NONE')

    @classmethod
    def poll(cls, context):
        #should not be accessed via spacebar from other space
        if context.scene.render.engine == 'BLENDER_RENDER' and context.area.type == 'PROPERTIES':
            actSpace = context.area.spaces.active
            actObj = context.active_object
            
            if actSpace.context != 'TEXTURE':
                return False
            elif actSpace.texture_context == 'WORLD' and context.scene.world.active_texture:
                return True
            elif actSpace.texture_context == 'MATERIAL' and actObj.active_material.active_texture and not actObj.active_material.use_nodes:
                #I assume both active_object and active_material are not None when tex_context is 'MATERIAL'.
                return True                
            elif actSpace.texture_context == 'LAMP' and actObj.data.active_texture:
                return True
            else: return False
        else:
            return False
    
    def execute(self, context):
        actSpace = context.area.spaces.active
        actObj = context.active_object

        if actSpace.texture_context == 'WORLD':
            slotsHolder = context.scene.world
        elif actSpace.texture_context == 'MATERIAL':
            slotsHolder = actObj.active_material
        elif actSpace.texture_context == 'LAMP':
            slotsHolder = actObj.data
        
        texSlot = slotsHolder.texture_slots[slotsHolder.active_texture_index]
        items = ('LINEAR_LIGHT', 'SOFT_LIGHT', 'COLOR', 'VALUE', 'SATURATION', 'HUE', 'LIGHTEN', 'DARKEN', 'DIVIDE', 'DIFFERENCE', 'OVERLAY', 'SCREEN', 'MULTIPLY', 'SUBTRACT', 'ADD', 'MIX')
        #---------
        curIndex = -1
        curType = texSlot.blend_type 
 
        for i in range(len(items)):
            if items[i] == texSlot.blend_type:
                curIndex = i
                break
        
        if curIndex == -1 :
            self.report({'WARNING'}, 'UnexpectedError: Current ' + texSlot.blend_type + ' is Unknown for Addon \'CycleBlendType\'. Operation was Aborted')
            return {'CANCELLED'}
    
        #-----------    
        if self.isForward:
            curIndex = curIndex + 1 if curIndex + 1 < len(items) else 0
        else:
            curIndex = curIndex - 1 if curIndex - 1 >= 0 else len(items) - 1
        texSlot.blend_type = items[curIndex]
        return {'FINISHED'} 
        
    
###########################################################################

# store keymaps here to access after registration
addon_keymaps = []

def register():
    bpy.utils.register_class(CycleBlendTypeOperator_NodeEditor)
    bpy.utils.register_class(CycleBlendTypeOperator_InternalTexture)
    
    # handle the keymap
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Node Editor', space_type='NODE_EDITOR')
    kmi = km.keymap_items.new(CycleBlendTypeOperator_NodeEditor.bl_idname, 'MINUS', 'PRESS', shift=True)
    kmi.properties.isForward = False
    kmi = km.keymap_items.new(CycleBlendTypeOperator_NodeEditor.bl_idname, 'EQUAL', 'PRESS', shift=True)
    kmi.properties.isForward = True
    addon_keymaps.append(km)
    
    km = wm.keyconfigs.addon.keymaps.new(name='Property Editor', space_type='PROPERTIES')
    kmi = km.keymap_items.new(CycleBlendTypeOperator_InternalTexture.bl_idname, 'MINUS', 'PRESS', shift=True)
    kmi.properties.isForward = False
    kmi = km.keymap_items.new(CycleBlendTypeOperator_InternalTexture.bl_idname, 'EQUAL', 'PRESS', shift=True)
    kmi.properties.isForward = True
    addon_keymaps.append(km)

    
def unregister():
    bpy.utils.unregister_class(CycleBlendTypeOperator_NodeEditor)
    bpy.utils.unregister_class(CycleBlendTypeOperator_InternalTexture)

    # handle the keymap
    wm = bpy.context.window_manager
    for km in addon_keymaps:
        wm.keyconfigs.addon.keymaps.remove(km)
    # clear the list
    addon_keymaps.clear()


if __name__ == "__main__":
    register()
