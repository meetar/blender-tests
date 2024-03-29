import subprocess
from datetime import datetime
import os, sys

startTime = datetime.now()

if os.path.exists('./images/'):
	os.system('rm -rf ./images/')

os.makedirs('./images/')

try:
	os.system('python collect-png-parallel.py --bounds 40.6997802 -74.0193432 40.877619 -73.9104387 --zoom 13 --mapzen_api_key XXXXXXX ./images/')
except:
	print("Error")
	sys.exit(0)

if not os.path.exists('./images/converted'):
    os.makedirs('./images/converted')

# os.system('for i in ./images/*.png; do echo $i; gdal_translate -ot UInt16 -of PNG -scale 0 8900 0 65536 -co worldfile=no --config GDAL_PAM_ENABLED NO $i ./images/converted/$(basename $i).png; done;')

os.system('for i in ./images/*.png; do echo $i; python ./convert-terrain.py -- $i; done;')

os.system('/Applications/Blender.app/Contents/MacOS/blender --python dir_to_blender2.py -- ./images/converted 100')

print("\nTime:")
print(datetime.now() - startTime)