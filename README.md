Blender3D Import psk psa addon (customized by matyalatte)
========================
I've customized the plugin for UE4 modding.<br>
You don't need to setup import options and rename objects.

### What's the difference with the original version?

- Rename armature to `Armature`
- Set false to `Scale down` as default
- Apply smooth shading
- Change unit scale to 0.01
- Add a UI panel to combine psk skeleton and gltf mesh
- Add a UI panel to export an armature and its mesh as fbx
- Split the script into some files

<img src="https://user-images.githubusercontent.com/69258547/154747400-be4235c6-319a-4ecd-865c-87892ac6d7b1.jpg" width=269></img>
![convine_psk_gltf](https://user-images.githubusercontent.com/69258547/155713407-ac41fcaf-786c-4300-a5a5-6514615a14b2.png)
![export_panel](https://user-images.githubusercontent.com/69258547/155806623-7fca602b-b24c-47c8-b67b-46bf8d79278f.png)
### Why should we set false to Scale down?
`Scale down` option will corrupt skeleton data.<br>
You can't make mods with this option.<br>
<br>
## Original description
<ul>
<li>This is an heavily edited version of original blender plugin by Darknet / Optimus_P-Fat / Active_Trash / Sinsoft / flufy3d: https://en.blender.org/index.php/Extensions:2.6/Py/Scripts/Import-Export/Unreal_psk_psa (<a href="https://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Import-Export/Unreal_psk_psa">old link</a>)
<li>Import mesh and skeleton from <b>.psk/.pskx</b></li>
<li>Import animation from <b>.psa</b></li>
<li>Game files can be exported to psk/psa by UModel: 
https://github.com/gildor2/UModel</li>
</ul>

<h5>Changes from original release</h5>
<ul>
<li>Blender 2.80+ support (check <a href="https://github.com/Befzz/blender3d_import_psk_psa/issues">issues</a> first!)</li>
<li>Fixed animation/skeleton import</li>
<li>Performance improvements</li>
<li>Panel UI updated</li>
<li>UI option: all actions to NLA track, one by one</li>
<li>UI option: mesh / skeleton or both import</li>
</ul>

<h3>Installation</h3>  

0. Download .py file:  

Current ( branch *latest* ):  
<a href ="https://github.com/Befzz/blender3d_import_psk_psa/raw/latest/addons/io_import_scene_unreal_psa_psk_270.py">270 direct link</a>  
<a href ="https://github.com/Befzz/blender3d_import_psk_psa/raw/latest/addons/io_import_scene_unreal_psa_psk_280.py">280 direct link</a>    
  
  
Stable ( branch *master* ):  
<a href ="https://github.com/Befzz/blender3d_import_psk_psa/raw/master/addons/io_import_scene_unreal_psa_psk_270.py">270 direct link</a>  
<a href ="https://github.com/Befzz/blender3d_import_psk_psa/raw/master/addons/io_import_scene_unreal_psa_psk_280.py">280 direct link</a>  


1. Add add-on:

* From Blender  
 
  2.79: File -> User preferences -> Add-ons -> Install Add-on from File...  
  2.80: Edit -> Preferences... -> Add-ons -> Install...

* Manually  

    Add .py file to the Blender's Add-ons search path:  
    * %APPDATA%\Blender Foundation\Blender\2.79\scripts\addons\  
    * %APPDATA%\Blender Foundation\Blender\2.80\scripts\addons\
    
2. Disable original add-on:  
`Import Unreal Skeleton Mesh (.psk)/Animation Set (.psa)`
3. Enable this one:  
`Import Unreal Skeleton Mesh (.psk)/Animation Set (.psa) (280)`
<h3>Usage</h3>  
<table><tbody>
<tr><th> Panel in 3DView (270) </th><th> Panel in 3DView (280) </th></tr>
<tr><td valign="top" align="center"><img src="https://github.com/Befzz/blender3d_import_psk_psa/blob/latest/imgs/270_psk.jpg"/></td>
<td valign="top" align="center"><img src="https://github.com/Befzz/blender3d_import_psk_psa/blob/latest/imgs/280_psk.jpg"/></td>
</tr></tbody></table>
