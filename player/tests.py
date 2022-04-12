from django.test import TestCase
from django.test import tests2

# Create your tests here.


from lib2to3 import pytree
import cv2
import pytesseract
import matplotlib.pyplot as plt
import sys
import io


# for encoding langs
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8') 
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"
config = ('-l eng+kor --oem 3 --psm 4')
img = cv2.imread("C:\\Users\\hansung\\Desktop\\Capstone\\github\\Capstone_frontend\\player\\media\\frame21.jpg", cv2.IMREAD_COLOR)
# print(pytesseract.image_to_string(img,config=config))


def gray_scale(image):
    result = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    return result

def image_threshold(image):
    ret, result = cv2.threshold(image, 172 ,255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # ret, result = cv2.threshold(image, 172 ,255, cv2.THRESH_BINARY )
    dst = cv2.resize(result, dsize=(1080, 720), interpolation=cv2.INTER_AREA)
    return dst

def save_file(text):
    myText = open("C:\\Users\\hansung\\Desktop\\Capstone\\github\\Capstone_frontend\\player\\mytxt.txt",'w')
    myText.write(text)
    myText.close()

#test code
img_gray = gray_scale(img)
img_threshold = image_threshold(img_gray)

#cv2.imread("threshold", img_threshold)

print(pytesseract.image_to_string(img_threshold,config=config))

#cv2.waitKey(0)
cv2.destroyAllWindows()