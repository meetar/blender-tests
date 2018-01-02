/Applications/Blender.app/Contents/MacOS/blender --python ~/work/blender-tests/export_to_blender.py -- ~/downloads/heightmapper-1507306626578.png .000008993847

/Applications/Blender.app/Contents/MacOS/blender --python dir_to_blender.py -- ./images .000008993847

/Applications/Blender.app/Contents/MacOS/blender --python dir_to_blender.py -- ./images .000008993847

/Applications/Blender.app/Contents/MacOS/blender --python dir_to_blender.py -- /Users/peter/Downloads/example/ .000008993847

python dir_to_blender.py -- ./images 1



for file in /Users/peter/Downloads/example/*.png; do
    python convert-terrain.py -- $file;
done




for i in *.tif; do gdal_translate -of GTIFF -a_nodata 0 $i $i~new_ndata.tif; done;
for i in *.tif;  do gdal_translate -of PNG -scale -co worldfile=no $i $i.png; done;





python collect.py --bounds 37.8434 -122.3193 37.7517 -122.0927 --zoom 12 --mapzen_api_key mapzen-XXXXXXX directory/path/


python collect.py --bounds 41.991794 -124.703541 46.299099 -116.463504 --zoom 7 --mapzen_api_key XXXXX ./images/

/Applications/Blender.app/Contents/MacOS/blender --python dir_to_blender.py -- 


python collect.py --bounds 41.991794 -124.703541 46.299099 -116.463504 --zoom 12 --mapzen_api_key XXXXX ./images/

for i in *.tif; do gdal_translate -ot UInt16 -of PNG -scale 0 8900 0 65536 -co worldfile=no --config GDAL_PAM_ENABLED NO $i ./converted/$i.png; done;

/Applications/Blender.app/Contents/MacOS/blender --python ../../dir_to_blender.py -- ./converted 1







python collect.py --bounds 37.8434 -122.3193 37.7517 -122.0927 --zoom 12 --mapzen_api_key mapzen-XXXXXXX directory/path/


bpy.ops.object.select_pattern(pattern="Grid*")
for tile in bpy.context.selected_objects:
	# tile.modifiers["Displace"].strength = 25
	tile.scale[2] = 10