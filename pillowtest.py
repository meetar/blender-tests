from PIL import Image

def unpack(h):
    # unpack data to range [-32768, 32768], the range in the raw data
    v = (h[0] * 256 + h[1] + h[2] / 256) - 32768;
    return (v, v, v);

im = Image.open("test.png") #Can be many different formats.
pix = im.load()
# print im.size #Get the width and hight of the image for iterating over
# print pix[0,0] #Get the RGBA Value of the a pixel of an image
# pix[0,0] = (255,0,0) # Set the RGBA Value of the image (tuple)
minv=float('inf')
maxv=float('inf')*-1
print(unpack(pix[0,0]))

for x in range(0,im.size[0]):
	for y in range(0,im.size[1]):
		# print pix[0,0]
		pix[x,y] = unpack(pix[x,y])
		minv = min(minv, pix[x,y])
		maxv = max(maxv, pix[x,y])

im.save("out.png") # Save the modified pixels as png
# print(minv, maxv)