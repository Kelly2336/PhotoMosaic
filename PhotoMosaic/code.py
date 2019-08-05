import cv2
import numpy as np
import os
import re
import urllib
import shutil
from bs4 import BeautifulSoup
import face_recognition

SetSize = 0
RGBval = []
pixel_size = 16
keywords = []

def AverageRGB(img):
	R = int(np.mean(img[:,:,2]))
	G = int(np.mean(img[:,:,1]))
	B = int(np.mean(img[:,:,0]))
	return R,G,B

def SquarePixel(img,pixel_size):
	#將圖片裁減為正方形
	height = np.size(img,0)
	width = np.size(img,1)
	crop_img = img[0:min(height,width),0:min(height,width)]
	#將圖片縮放為pixel_size
	return cv2.resize(crop_img,(pixel_size,pixel_size))

def MatchPixel(img,folder_path,RGBval):
	R,G,B = AverageRGB(img)
	full_path = folder_path+"/Dataset/"+str(R//128*100+G//128*10+B//128)
	filenames = os.listdir(full_path)
	#找RGBval最接近的小圖
	min_id = -1
	min_diff = 1e9
	for file in filenames:
		file_id = int(file[:-4])
		r,g,b = RGBval[file_id]
		diff = (R-r)**2 + (G-r)**2 + (B-b)**2
		if diff < min_diff:
			min_diff = diff
			min_id = file_id
	return cv2.imread(full_path+"/"+str(min_id)+".jpg")

def ResizePicture(file_path,pixel_size):
	#將圖片裁剪為長寬皆為pixel_size的整數倍
	img = cv2.imread(file_path)
	height = np.size(img,0)
	width = np.size(img,1)
	img = img[0:height//pixel_size*pixel_size,0:width//pixel_size*pixel_size]
	return img

#input
file_path = input("Which file do you want to use? Enter the path of the file:")
while True:
	s = input("Enter the keyword you want to use? Or enter \"break\" to end input:")
	if s == 'break':
		break
	else:
		keywords.append(s)
folder_path = input("Enter a path of a folder which can save the output:")

crop_face = input("Do you want to crop the face from the image? Enter \"Y\"/\"N\":")

#將圖中的人臉定位，裁切出來，另存檔案
if crop_face == "Y":
	#image = face_recognition.load_image_file(file_path)
	image = cv2.imread(file_path,1)
	face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=1)
	if len(face_locations)>0:
		#有偵測到人臉
		top,right,bottom,left = face_locations[0] #只存取一張人臉
		image = image[top:bottom,left:right]
		file_path = file_path.replace(".","_1.")
		cv2.imwrite(file_path,image)

#create DataSet
os.mkdir(folder_path+"/Dataset")
for keyword in keywords:
	#以不同顏色、關鍵字google搜尋圖片
	for color in ["red","orange","yellow","green","teal","blue","purple","pink","white","gray","black","brown"]:
		url = "https://www.google.com/search?q="+keyword+"&source=lnms&tbm=isch&tbs=ic:specific,isc:"+color
		headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
		req = urllib.request.Request(url=url, headers=headers)
		html = urllib.request.urlopen(req).read()
		soup = BeautifulSoup(html,'html.parser')
		tags = soup('img')
		for tag in tags:
			img_url = re.findall("data-src=\"([^\"]+)\"",str(tag))
			if len(img_url):
				#將圖片存檔
				urllib.request.urlretrieve(img_url[0],folder_path+"/Dataset/"+"%s.jpg"%SetSize)
				SetSize += 1 #圖片編號

#建立以RGB為分類依據的子資料夾
for i in range(2):
	for j in range(2):
		for k in range(2):
			os.mkdir(folder_path+"/Dataset/"+str(i*100+j*10+k))

#將所有圖片裁切並分類歸檔
filenames = os.listdir(folder_path+"/Dataset")
for i in range(SetSize):
	file_name = "%s.jpg"%i
	img = cv2.imread(folder_path+"/Dataset/"+file_name,1)#1彩色
	img = SquarePixel(img,pixel_size)
	R,G,B = AverageRGB(img)
	cv2.imwrite(folder_path+"/Dataset/"+str(R//128*100+G//128*10+B//128)+"/"+file_name,img)
	RGBval.append((R,G,B))#儲存RGB值

#將圖組起來
img = ResizePicture(file_path,pixel_size)
height = np.size(img,0)
width = np.size(img,1)
for i in range(0,height,pixel_size):
	for j in range(0,width,pixel_size):
		img[i:i+pixel_size,j:j+pixel_size] = MatchPixel(img[i:i+pixel_size,j:j+pixel_size],folder_path,RGBval)

#delete dataset
shutil.rmtree(folder_path+"/Dataset")
#savefile
cv2.imwrite(folder_path+"/output.jpg",img)
#output
cv2.imshow("frame",img)
#按任意鍵結束視窗
cv2.waitKey(0)
cv2.destroyAllWindows()
