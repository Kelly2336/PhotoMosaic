# Photo Mosaic
## Overview
* 2019.1
* 計算機概論 final project
* Photomosaic
## Used
1. python3
2. OpenCV
3. face_recognition API
## Run
* Open the web
* Install
    * pip install numpy
    * pip install cmake
    * pip install dlib
    * pip install face_recognition
    * pip install opencv-python
    * pip install beautifulsoup4
* Prepare a photo
* Run the code
* Be patient (It will run around five minutes)

![](https://i.imgur.com/QbmRU0h.png)
## Detail
* User input, including file_path, folder_path, keywords.
* Ask the user if he want to crop the face or not.
* If yes, then use face_recognition API to detect the face’s location.
* Crop a rectangle of the face and save it as a new file.
* Build the dataset by using the keywords to google search image.
* Calculate the average RGB of the images in dataset.
* Combine the photo
    * Resize the height and width of original file to the integer times of pixel_size.
    * Divide the photo into pixels.
    * Match each pixel to the image in the dataset with the closest RGB_value.
* Save the photo file and output it though a window.
## Test Result
![](https://i.imgur.com/BhQfPxY.png)
![](https://i.imgur.com/P7wew00.jpg)
![](https://i.imgur.com/3UybkGw.png)
