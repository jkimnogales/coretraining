# Import the PIL library
from PIL import Image,ImageFilter


#Open the file.  Note, this is gif which has 255,255,255
img=Image.open('our-world.gif')


# To edit the image pixel by pixel, we need to get the image map out.
rgb_im = img.convert('RGB')     # For gif files, we need to do this to get rgb values
pixels=rgb_im.load()            # This grabs the pixels so we can edit
row,col=rgb_im.size



#Convert half the image so colors are switched
for i in range(col):    # for every col:
    for j in range(row/2):    # For every row
        (r,g,b)=pixels[i,j]
        if (r==g) and (r==b):
            pixels[i,j] = (183, 209, 226)
        else:
            pixels[i,j]=(255,255,255)



# Show this image
rgb_im.show()

#turn it upside down
rgb_im_02=rgb_im.transpose(Image.ROTATE_180)

rgb_im_02.show()

# Edge detect
rgb_im_03 = rgb_im.filter(ImageFilter.EDGE_ENHANCE_MORE)
rgb_im_03.show()



