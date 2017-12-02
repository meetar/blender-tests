import bpy

def updateViewport():
	bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)

dir="/Users/peter/Downloads/"
name="heightmapper-1507306626578.png"
path=dir+name
bpy.ops.image.open(filepath=path, directory=dir, relative_path=True)
# bpy.ops.image.open(directory=dir, files=[{"name":name}], relative_path=True)
# bpy.ops.image.open(filepath=path, directory=dir, files=[{"name":name}], relative_path=True)

texture=bpy.data.textures.new('my_texture', 'IMAGE')
texture.image = bpy.data.images[0]

w=texture.image.size[0]
h=texture.image.size[1]

bpy.ops.object.delete(use_global=False)
bpy.ops.mesh.primitive_grid_add(x_subdivisions=w, y_subdivisions=h, location=(0,0,0))
grid=bpy.context.selected_objects[0]
grid.name = "grid1"

updateViewport()

grid.scale[0] = w/100
grid.scale[1] = h/100

updateViewport()

bpy.ops.object.modifier_add(type='DISPLACE')


updateViewport()

grid.modifiers["Displace"].texture = texture

updateViewport()

grid.modifiers["Displace"].mid_level = 0
#grid.modifiers["Displace"].strength = 0.005
