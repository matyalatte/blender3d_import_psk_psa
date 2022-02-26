import bpy
from bpy.props import BoolProperty, PointerProperty, StringProperty, FloatProperty, EnumProperty

def get_mesh(armature):
    if armature.type!='ARMATURE':
        raise RuntimeError('Not an armature.')
    mesh=None
    for child in armature.children:
        if child.type=='MESH':
            if mesh is not None:
                raise RuntimeError('"The armature should have only 1 mesh."')
            mesh=child
    if mesh is None:
        raise RuntimeError('Mesh Not Found')
    return mesh

def export_as_fbx(file, armature, global_scale, smooth_type, export_tangent):
    
    mode = bpy.context.object.mode
    bpy.ops.object.mode_set(mode='OBJECT')

    armature_name = armature.name
    try:
        true_armature = bpy.data.objects['Armature']
    except Exception as e:
        true_armature = None

    if true_armature is not None:
        true_armature.name = 'foobarfoobarfoobar'
    armature.name = 'Armature'
        
    #deselect all
    for obj in bpy.context.scene.objects:
        obj.select_set(False)

    mesh = get_mesh(armature)

    #select objects
    armature.select_set(True)
    mesh.select_set(True)

    #export as fbx
    bpy.ops.export_scene.fbx( \
        filepath=file,
        use_selection=True,
        use_active_collection=False,
        global_scale=global_scale,
        apply_unit_scale=True,
        apply_scale_options='FBX_SCALE_NONE',
        object_types=set(['ARMATURE','MESH']),
        use_mesh_modifiers=True,
        mesh_smooth_type=smooth_type,
        use_tspace=export_tangent,
        add_leaf_bones=False,
        primary_bone_axis='Y',
        secondary_bone_axis='X',
        armature_nodetype='NULL',
        bake_anim=False,
        axis_forward='-Z',
        axis_up='Y'
        )

    armature.name=armature_name
    if true_armature is not None:
        true_armature.name='Armature'

    bpy.ops.object.mode_set(mode=mode)


class Export_Inputs(bpy.types.PropertyGroup):
    fGlobalScale : FloatProperty(
        name = 'Scale',
        description = 'Scale all data',
        default = 1.0, min = 0.01, max = 100, step = 0.1, precision = 2,
    )
    bExportTangent: BoolProperty(
        name = 'Export tangent',
        description = 'Add binormal and tangent vectors.',
        default = False
    )
    smooth_type : EnumProperty(
        name = "Smoothing",
        description = 'Export smoothing information.',
        items = (('OFF', 'Normals Only','Export only normals'),
                ('FACE','Face','Write face smoothing'),
                ('EDGE','Edge','Write edge smoothing')),
        default='FACE'
    )

class Export_OT_Run_Button(bpy.types.Operator):
    '''Export an armature and its mesh as fbx.'''
    bl_idname = "export_as_fbx.run_button"
    bl_label = "Export as fbx"
    bl_options = {'REGISTER', 'UNDO'}
    #--- properties ---#
    success: StringProperty(default = "Success!", options = {'HIDDEN'})
    #--- execute ---#
    def execute(self, context):
        try:
            #check save status
            if not bpy.data.is_saved:
                raise RuntimeError('Save .blend first.')
            base_file_name=".".join(bpy.data.filepath.split('.')[:-1])

            #get armature
            selected = bpy.context.selected_objects
            if len(selected)==0:
                raise RuntimeError('Select an armature.')
            armature=selected[0]
            if armature.type!='ARMATURE':
                raise RuntimeError('Select an armature.')

            file = base_file_name + '_' + armature.name +'.fbx'
            global_scale = context.scene.fbx_export_options.fGlobalScale
            smooth_type = context.scene.fbx_export_options.smooth_type
            export_tangent = context.scene.fbx_export_options.bExportTangent
            #main
            export_as_fbx(file, armature, global_scale, smooth_type, export_tangent)
            self.report({'INFO'}, 'Success! {} has been generated.'.format(file))

        except Exception as e:
            self.report({'ERROR'}, str(e))
        
        return {'FINISHED'}
    
class Export_PT_Panel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "PSK / PSA"
    bl_label = "Export as fbx"

    #--- draw ---#
    def draw(self, context):
        layout = self.layout
        layout.label(text='How to Use')
        layout.label(text='1. Save .blend')
        layout.label(text='2. Select an armature')
        layout.label(text='3. Click the button below')
        layout.operator(Export_OT_Run_Button.bl_idname, icon='MESH_DATA')
        layout.label(text='Options')
        layout.prop(context.scene.fbx_export_options, 'fGlobalScale')
        layout.prop(context.scene.fbx_export_options, 'smooth_type')
        layout.prop(context.scene.fbx_export_options, 'bExportTangent')

classes = (
        Export_Inputs,
        Export_PT_Panel,
        Export_OT_Run_Button
    )

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.Scene.fbx_export_options = PointerProperty(type=Export_Inputs)

def unregister():
    from bpy.utils import unregister_class
    for cls in classes:
        unregister_class(cls)

    del bpy.types.Scene.fbx_export_options