import bpy

#combine psk and gltf
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

def get_children(armature):
    #get armature's mesh
    mesh=get_mesh(armature)

    #get materials and the names of uv maps
    materials=mesh.data.materials
    uv_names=[]
    for uvmap in  mesh.data.uv_layers :
            uv_names.append(uvmap.name)
            
    return mesh, materials

def replace_materials(mesh, new_materials):
    materials=mesh.data.materials
    if len(materials)>len(new_materials):
        raise RuntimeError('The number of materials is too large')
    for i in range(len(materials)):
        materials[i]=new_materials[i]

def get_armature_modifier(mesh):
    armature_modifier=None
    for modifier in mesh.modifiers:
        if modifier.type=='ARMATURE':
            armature_modifier=modifier
    if armature_modifier is None:
        raise RuntimeError('Armature Modifier Not Found')
    return armature_modifier
        
def combine_psk_and_gltf(psk_armature, gltf_armature):
    bpy.context.view_layer.objects.active = psk_armature

    mode = bpy.context.object.mode
    bpy.ops.object.mode_set(mode='OBJECT')

    #deselect all
    for obj in bpy.context.scene.objects:
        obj.select_set(False)    
    
    #get objects
    psk_mesh, psk_materials = get_children(psk_armature)
    gltf_mesh, _ = get_children(gltf_armature)
    
    psk_collection=psk_armature.users_collection
    gltf_collection=gltf_armature.users_collection
    
    replace_materials(gltf_mesh, psk_materials)

    gltf_mesh.parent = psk_armature
    gltf_armature_modifier = get_armature_modifier(gltf_mesh)
    gltf_armature_modifier.object = psk_armature

    for col in gltf_collection:
        col.objects.unlink(gltf_mesh)
    for col in psk_collection:
        col.objects.link(gltf_mesh)

    gltf_armature.select_set(True)
    psk_mesh.select_set(True)
    bpy.ops.object.delete()
    
    bpy.ops.object.mode_set(mode=mode)
    

class Combine_OT_Run_Button(bpy.types.Operator):
    '''Combine psk skeleton and gltf mesh.'''
    bl_idname = "combine_psk_and_gltf.run_button"
    bl_label = "Combine psk and gltf"
    bl_options = {'REGISTER', 'UNDO'}
    #--- properties ---#
    success: bpy.props.StringProperty(default = "Success!", options = {'HIDDEN'})
    
    #--- execute ---#
    def execute(self, context):
        try:
            psk_name='Armature'

            #get gltf armature
            selected = bpy.context.selected_objects
            if len(selected)!=2:
                raise RuntimeError('Select 2 armatures.')
            psk = selected[0]
            gltf=selected[1]
            if psk.type!='ARMATURE' or gltf.type!='ARMATURE':
                raise RuntimeError('Select 2 armatures.')

            if 'Armature' in gltf.name:
                psk, gltf = gltf, psk

            if 'Armature' not in psk.name:
                raise RuntimeError('At least one of the armatures should be "Armature".')

            #main
            combine_psk_and_gltf(psk, gltf)
            self.report({'INFO'}, self.success)
        
        except Exception as e:
            self.report({'ERROR'}, str(e))
        
        return {'FINISHED'}
    
class Combine_PT_Panel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "PSK / PSA"
    bl_label = "Combine psk and gltf"

    #--- draw ---#
    def draw(self, context):
        layout = self.layout
        layout.label(text='How to Use')
        layout.label(text='1. Import psk')
        layout.label(text='2. Import gltf')
        layout.label(text='3. Select 2 armatures')
        layout.label(text='4. Click the button below')        
        layout.operator(Combine_OT_Run_Button.bl_idname, icon='MESH_DATA')

classes = (
        Combine_PT_Panel,
        Combine_OT_Run_Button
    )

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

def unregister():
    from bpy.utils import unregister_class
    for cls in classes:
        unregister_class(cls)