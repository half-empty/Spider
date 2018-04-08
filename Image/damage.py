# 遍历文件，判断图片是否损坏
from os import listdir
from PIL import Image
for filename in listdir('/home/sunweifeng/Picture/pexels/image/'):
	if filename.endswith('.jpeg'):
		try:
			img = Image.open('/home/sunweifeng/Picture/pexels/image/'+filename) # open the image file
			#img.verify() # verify that it is, in fact an image
		except (IOError, SyntaxError) as e:
			print('Bad file:', filename) # print out the names of corrupt files
