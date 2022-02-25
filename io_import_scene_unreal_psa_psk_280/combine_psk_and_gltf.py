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

def get_armature(armature_name):
    #search "armature"
    armature=None
    for obj in bpy.context.scene.objects:
        if obj.name==armature_name:
            armature=obj
            break
    if armature is None:
        raise RuntimeError('"armature" Not Found.')

    #get armature's mesh
    mesh=get_mesh(armature)

    #get materials and the names of uv maps
    materials=mesh.data.materials
    uv_names=[]
    for uvmap in  mesh.data.uv_layers :
            uv_names.append(uvmap.name)
            
    return armature, mesh, materials, uv_names

def replace_materials_and_uvnames(mesh, new_materials, new_uv_names):

    materials=mesh.data.materials
    if len(materials)>len(new_materials):
        raise RuntimeError('The number of materials is too large')
    for i in range(len(materials)):
        materials[i]=new_materials[i]
        
    uv_maps=mesh.data.uv_layers
    if len(uv_maps)>len(new_uv_names):
        raise RuntimeError('The number of UV maps is too large')
    for i in range(len(uv_maps)):
        uv_maps[i].name=new_uv_names[i]
        
def remove_vertices(mesh, vertex_group):
    me = mesh.to_mesh()
    bpy.context.view_layer.objects.active = mesh
    vg = mesh.vertex_groups
    
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action = 'DESELECT')
    bpy.ops.object.mode_set(mode="OBJECT")
    
    
    for v in bpy.data.meshes[me.name].vertices:
        v.select = False
        for g in v.groups:
            if vertex_group.name==vg[g.group].name:
                v.select = True 

    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    bpy.ops.mesh.delete(type='VERT')
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    
        
def combine_psk_and_gltf(psk_name, gltf_name):
    mode = bpy.context.object.mode
    bpy.ops.object.mode_set(mode='OBJECT')
    
    #deselect all
    for obj in bpy.context.scene.objects:
        obj.select_set(False)
    
    #get objects
    _, psk_mesh, psk_materials, psk_uv_names = get_armature(psk_name)
    _, gltf_mesh, _, _ = get_armature(gltf_name)
    
    psk_vert_num = len(psk_mesh.data.vertices)
  
    replace_materials_and_uvnames(gltf_mesh, psk_materials, psk_uv_names)
    
    #make vertex group for remove psk vertices
    psk_group = psk_mesh.vertex_groups.new(name='psk')
    psk_group.add([i for i in range(psk_vert_num)], 1, 'ADD')

    #select meshes    
    psk_mesh.select_set(True)
    gltf_mesh.select_set(True)    
    bpy.context.view_layer.objects.active=psk_mesh
    meshes={}
    meshes['active_object']=psk_mesh
    meshes['selected_editable_objects']=[psk_mesh, gltf_mesh]

    #join meshes
    bpy.ops.object.join(meshes)
    
    psk_mesh.select_set(False)

    #remove psk vertices
    psk_group = psk_mesh.vertex_groups.get('psk')
    remove_vertices(psk_mesh, psk_group)

    #remove vertex group
    psk_mesh.vertex_groups.remove(psk_group)
    
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
            if len(selected)==0:
                raise RuntimeError('Select gltf armature.')
            gltf=selected[0]
            if gltf.type!='ARMATURE':
                raise RuntimeError('Select gltf armature.')
            gltf_name=gltf.name

            #main
            combine_psk_and_gltf(psk_name, gltf_name)
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
        layout.label(text='3. Select gltf armature')
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