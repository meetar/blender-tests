import bpy
import sys
import os

try:
    args = list(reversed(sys.argv))
    idx = args.index("--")

except ValueError:
    params = []

else:
    params = args[:idx][::-1]

print("Script params:", params)

def updateViewport():
	bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)

def doit(path, offset = [0,0]):
	print('?', path, offset)
	# bpy.ops.image.open(filepath=path, relative_path=True)
	# bpy.ops.image.open(filepath=path)
	# bpy.ops.image.open(filepath='.')
	bpy.ops.image.open(filepath="/Users/peter/work/blender-tests/images/10-158-363.png", directory="/Users/peter/work/blender-tests/images/", files=[{"name":"10-158-363.png", "name":"10-158-363.png"}], relative_path=True, show_multiview=False)

	# name=os.path.basename(path)
	# texture=bpy.data.textures.new(name, 'IMAGE')
	# texture.image = bpy.data.images[name]
	# texture.extension = 'CLIP'

	# w=texture.image.size[0]
	# h=texture.image.size[1]

	# tilesize = w/100*2
	# # account for 2-px padding on all sides (might need 4)
	# tilesize -= 4/100*2;
	# location = (offset[0]*tilesize,offset[1]*tilesize,0)
	
	# bpy.ops.mesh.primitive_plane_add(location=location)
	# # bpy.ops.mesh.primitive_grid_add(x_subdivisions=w, y_subdivisions=h, location=location)
	# tile=bpy.context.selected_objects[0]

	# tile.scale[0] = w/100
	# tile.scale[1] = h/100
	# bpy.ops.object.modifier_add(type='SUBSURF')

	# tile.modifiers["Subsurf"].subdivision_type = 'SIMPLE'
	# tile.cycles.use_adaptive_subdivision = True
	# bpy.context.object.modifiers["Subsurf"].show_only_control_edges = True


	# bpy.ops.object.modifier_add(type='DISPLACE')

	# tile.modifiers["Displace"].texture = texture

	# tile.modifiers["Displace"].mid_level = 0
	# tile.modifiers["Displace"].strength = float(params[1])

path=params[0]
print("path: "+path)
abspath=os.path.abspath(path);
print(os.path.abspath(path))
print(os.path.exists(path))
if os.path.isfile(path):
	print("single file")
	doit(path)
elif os.path.isdir(path):
	print("directory")
	print(os.listdir(path))
	for file in os.listdir(path):
		print('abs: '+os.path.abspath(file))
	# set range vars
	minx = float('inf')
	maxx = -float('inf')
	miny = float('inf')
	maxy = -float('inf')
	files = []
	# get range
	for dirname, dirnames, filenames in os.walk(path):
		# get filenames
		print('dirnames:')
		print(dirnames)
		for file in filenames:
			if (file != ".DS_Store"):
				files.append(os.path.join(path, file))
	print('file list:')
	print(files)
	for file in files:
		print("file: "+file)
		name=os.path.basename(file).split('.')[0]
		print("filename:"+name)
		# use rangefinder to get min and max for x and y
		# get x and y from file
		pieces = [int(piece) for piece in name.split("-")[1:3]]
		# print('pieces:')
		# print(pieces)
		# check x and y against min/max
		minx = min(minx, int(pieces[0]))
		maxx = max(maxx, int(pieces[0]))
		miny = min(miny, int(pieces[1]))
		maxy = max(maxy, int(pieces[1]))

	print('x range: '+str(minx)+'-'+str(maxx))
	print('y range: '+str(miny)+'-'+str(maxy))

	# cleanup default object
	bpy.ops.object.delete(use_global=False)

	# get range
	for file in files:
		print('file:'+file)
		name=os.path.basename(file).split('.')[0]
		print("filename:"+name)
		pieces = [int(piece) for piece in os.path.basename(name).split("-")[1:3]]
		# locate based on rangefinder
		# convert file pieces to offsets based on min and max
		offset = [(pieces[0]-minx), (pieces[1]-miny)*-1]
		print("offset:", offset[0], offset[1])
		# then doit passing in offsets
		doit(file, offset)

	# set up rendering
	context = bpy.context
	scene = context.scene
	obj = scene.objects.get("Lamp")
	scene.objects.active = obj
	context.object.rotation_euler = [0,0,0]
	context.object.data.type = 'SUN'
	context.object.data.shadow_method = 'NOSHADOW'
	context.object.data.use_specular = False
	scene.render.engine = 'CYCLES'
	scene.cycles.feature_set = 'EXPERIMENTAL'
	
	scene.world.light_settings.gather_method = 'APPROXIMATE'
	scene.world.light_settings.use_ambient_occlusion = True
	scene.world.light_settings.ao_factor = .5
	scene.world.light_settings.ao_blend_type = 'MULTIPLY'
	scene.render.use_raytrace = False

else:
	print("don't see the path \""+path+"\"")
