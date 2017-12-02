import subprocess
from datetime import datetime
import os

startTime = datetime.now()

if not os.path.exists('./images/'):
    os.makedirs('./images/')

os.system('python collect-png.py --bounds 54.1933181 -3.4956715 54.7636043 -2.5820556 --zoom 14 --mapzen_api_key XXXXXXX ./images/')

if not os.path.exists('./images/converted'):
    os.makedirs('./images/converted')

os.system('for i in ./images/*.png; do echo $i; gdal_translate -ot UInt16 -of PNG -scale 0 8900 0 65536 -co worldfile=no --config GDAL_PAM_ENABLED NO $i ./images/converted/$(basename $i).png; done;')

# os.system('for i in ./images/*.png; do echo $i; python ../landgrab/convert-terrain.py -- $i; done;')

# os.system('/Applications/Blender.app/Contents/MacOS/blender --python dir_to_blender2.py -- ./images/converted 100')
os.system('"C:\Program Files\Blender Foundation\Blender\blender.exe" --python dir_to_blender-win.py -- ./images/converted 100')


print("\nTime:")
print(datetime.now() - startTime)