#reference:https://www.geeksforgeeks.org/python-copy-and-paste-images-onto-other-image-using-pillow/
# import image module from pillow
from PIL import Image
 
# open the image
Image1 = Image.open('D:\cat.jpg')
 
# make a copy the image so that the
# original image does not get affected
Image1copy = Image1.copy()
Image2 = Image.open('D:\core.jpg')
Image2copy = Image2.copy()
 
# paste image giving dimensions
Image1copy.paste(Image2copy, (0, 0))
 
# save the image
Image1copy.save('D:\pasted2.png')