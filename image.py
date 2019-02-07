#import PIL
#import Image
import cv2
import numpy as np
import os
import re
import urllib
import shutil
from bs4 import BeautifulSoup


folder_path = ""
file_path = ""
pixel_size = 16
keywords = []
SetSize = 0
RGBval = []

def UserInput():
	file_path = input("Which file do you want to use? Enter the path of the file:")
	while True:
		s = input("Enter the keyword you want to use? Or enter \"break\" to end input:")
		if s == 'break':
			break
		else:
			keywords.append(s)
	folder_path = input("Enter a path of a folder which can save the output:")


def ResizePicture():
	#將圖片裁剪為長寬皆為pixel_size的整數倍
	img = cv2.imread(file_path)
	height = np.size(img,0)
	width = np.size(img,1)
	crop_img = img[0:height//pixel_size*pixel_size,0:width//pixel_size*pixel_size]
	return img

'''
def CropFace():
'''

def PhotoDataset():
	#建立存放圖片的資料夾
	os.chdir(folder_path)
	os.mkdir(folder_path+"/Dataset")
	for keyword in keywords:
		#以不同顏色、關鍵字搜尋圖片
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
					SetSize += 1



def AverageRGB(img):
	R = int(np.mean(img[:,:,2]))
	G = int(np.mean(img[:,:,1]))
	B = int(np.mean(img[:,:,0]))
	return R,G,B
	
def SquarePixel(img):
	#將圖片裁減為方形（以中心為基準點）
	height = np.size(img,0)
	width = np.size(img,1)
	img = img[height/2-min(height,width)/2:height/2+min(height,width/2)
				,width/2-min(height,width)/2:width/2+min(height,width)/2]
	#將圖片縮放為pixel_size
	img = cv2.resize(img,pixel_size,pixel_size)
	return img


def ClassifyData():
	#建立以RGB為分類依據的子資料夾
	for i in range(16):
		for j in range(16):
			for k in range(16):
				os.mkdir(folder_path+"/Dataset/"+str(i*10000+j*100+k))
	#將所有圖片裁切並分類歸檔
	filenames = os.listdir(folder_path+"/Dataset")
	for i in range(SetSize):
		file_name = "%s.jpg"%i
		img = imread(ifolder_path+"/Dataset/"+file_name,1)#1彩色
		img = SquarePixel(img)
		R,G,B = AverageRGB(img)
		shutil.move( folder_path+"/Dataset/"+file_name , folder_path+"/Dataset/"+str(R//16*10000+G//16*100+B//16)+"/"+file_name )
		RGBval.append((R,G,B))#儲存RGB值



def MatchPixel(img):
	R,G,B = AverageRGB(img)
	full_path = folder_path+"/Dataset/"+str(R//16*10000+G//16*100+B//16)
	filenames = os.listdir(full_path)
	min_id = -1;
	min_diff_RGB = 1e9
	for file in filenames:
		file_id = int(file.replace(".jpg",""))
		r,g,b = RGBval[id]
		diff = (R-r)**2 + (G-r)**2 + (B-b)**2
		if diff<min_diff:
			min_diff = diff
			min_id = file_id
	pixel = cv2.imread(full_path+"/"+min_id+".jpg")
	return pixel


def CombinePhoto():
	img = ResizePicture()
	height = np.size(img,0)
	width = np.size(img,1)
	for i in range(0,height,pixel_size):
		for j in range(0,width,pixel_size):
			img[i:i+pixel_size,j:j+pixel_size] = MatchPixel(img[i:i+pixel_size,j:j+pixel_size])
	cv2.imwrite(folder_path+"output.jpg",img);


def DeleteData():
	shutil.rmtree(folder_path+"/Dataset")

def Output():
	img = cv2.imread(folder_path+"output.jpg")
	cv2.imshow("frame",crop_img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()



UserInput()
print("file_path="+file_path)
print("folder_path="+folder_path)
PhotoDataset()
ClassifyData()
CombinePhoto()
Output()












