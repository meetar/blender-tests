import subprocess
from datetime import datetime
import os

startTime = datetime.now()

# os.system('python collect-png.py --bounds 45.773097 -124.1536 46.299099 -123.358251 --zoom 14 --mapzen_api_key XXXXXX ./images/')

if not os.path.exists('./images/converted'):
    os.makedirs('./images/converted')

# os.system('for i in ./images/*.png; do echo $i; gdal_translate -ot UInt16 -of PNG -scale 0 8900 0 65536 -co worldfile=no --config GDAL_PAM_ENABLED NO $i ./images/converted/$(basename $i).png; done;')

os.system('for i in ./images/*.png; do echo $i; python ../landgrab/convert-terrain.py -- $i; done;')

os.system('/Applications/Blender.app/Contents/MacOS/blender --python dir_to_blender2.py -- ./images/converted 100')

print("\nTime:")
print(datetime.now() - startTime)