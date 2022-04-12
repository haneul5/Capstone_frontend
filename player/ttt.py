from pykospacing import Spacing
from pyrsistent import CheckedKeyTypeError
from lib2to3 import pytree
import cv2
import pytesseract
import sys
import io
import math
import sceneCutter #프레임 값 읽어오기


# for encoding langs
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8') 
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"
config = ('-l eng+kor --oem 3 --psm 4')

dirpath = "C:\\Users\\hansung\\Desktop\\Capstone\\github\\Capstone_frontend\\player"
myText = ''
keyword_list = []

def gray_scale(image):
    result = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    return result

def image_threshold(image):
    ret, result = cv2.threshold(image,172 ,255, cv2.THRESH_BINARY)
    # dst = cv2.resize(result, dsize=(1080, 720), interpolation=cv2.INTER_AREA) # image size 조절
    # th2 = cv2.adaptiveThreshold(result, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\cv2.THRESH_BINARY, 9,5 )
    return result


def range_scale(image):
    h,w = image.shape
    result = image[0:140, 0:w]
    # cv2.rectangle(result, (0,0),(100-1,w-1),(0,255,0))
    # cv2.imshow("roi",result)
    # cv2.waitKey(0)
    return result
    

def save_file(text, path):
    fix_text = spaceText(text)
    myText = open(path,'a',encoding='UTF-8-sig')
    myText.write(fix_text+"\n")
    myText.close()

# 띄어쓰기 교정
def spaceText(text):
    fixed_text = text.replace(" ","") # 띄어쓰기가 없는 문장 임의로 만들기
    spacing = Spacing()
    kospacing_text = spacing(fixed_text) # 띄어쓰기 문법 수정
    return kospacing_text

# 시간 변환
def changeTime(time) :
    hours = time // 3600
    time = time - hours*3600
    mu = time // 60
    ss = time - mu*60
    result = str(math.trunc(hours))+':'+str(math.trunc(mu))+':'+str(math.trunc(ss))
    return result

# save_file_keyword

def save_file_2Line(text,path):
    global myText, keyword_list
    list=text.split('\n')
    if (len(list) < 3):
        myText = list[0]+'\n' + list[1]
    else:
        myText =  list[0]+'\n' + list[1] +'\n'+ list[2]

    fix_text = spaceText(myText)
    myTextFile = open(path,'a',encoding='UTF-8-sig')
    myTextFile.write(fix_text+"\n")
    keyword_list.append(fix_text)
    myTextFile.close()

def no_dup(my_dict):
    seen = []
    result = dict()
    for key, val in my_dict.items():
        if val not in seen:
            seen.append(val)
            result[key] = val
    return result


video_info = dict()
 
#test code
for i in range(len(sceneCutter.imgName)) :
    
    img = cv2.imread(sceneCutter.imgName[i], cv2.IMREAD_COLOR)
    img_gray = gray_scale(img)
    img_threshold = image_threshold(img_gray)
    img_range = range_scale(img_threshold)
    img_string = pytesseract.image_to_string(img_range,config=config)
    img_string2 = pytesseract.image_to_string(img_threshold,config=config)

    save_file_2Line(img_string, dirpath + "/mytxt.txt")
    save_file(img_string2, dirpath + "/mytxt2.txt")
    time = changeTime(sceneCutter.videoTime[i])
    # keyword_k = img_string.replace("\n", " ")
    # keyword = spaceText(keyword_k)
    
    video_info[time] = keyword_list[i]
    
    

dic = no_dup(video_info)   
print(dic)

# main
#compare =[] # 문자열 비교

# for i in range(len(tests2.imgName)) :
#     img = cv2.imread(tests2.imgName[i], cv2.IMREAD_COLOR)
#     img_gray = gray_scale(img)
#     img_threshold = image_threshold(img_gray)
#     img_range = range_scale(img_threshold)
#     img_string = pytesseract.image_to_string(img_range,config=config)
#     img_string2 = pytesseract.image_to_string(img_threshold,config=config)
# #    compare.append(img_string)

#     save_file_2Line(img_string, "C:\\Users\\hansung\\Desktop\\Capstone\\github\\Capstone_frontend\\player\\mytxt.txt")
#     save_file(img_string2, "C:\\Users\\hansung\\Desktop\\Capstone\\github\\Capstone_frontend\\player\\mytxt2.txt")
#     time = changeTime(tests2.videoTime[i])
#     # keyword_k = img_string.replace("\n", " ")
#     # keyword = spaceText(keyword_k)
#     video_info = {tests2.videoTime[i] : keyword_list[i]}
#     # print(video_info)

#     if i > 0 and video_info.get(tests2.videoTime[i]) != video_info.get(tests2.videoTime[i-1]) :
#         print( str(video_info.get(tests2.videoTime[i])+video_info.get(tests2.videoTime[i-1])) )
#         print(video_info)
#     elif i==0:
#         print(video_info)
#     else:
#         continue

#     # if i == 0:
#     #     save_file_2Line(img_string, "C:\\Users\\hansung\\Desktop\\Capstone\\github\\Capstone_frontend\\player\\mytxt.txt")
#     #     save_file(img_string2, "C:\\Users\\hansung\\Desktop\\Capstone\\github\\Capstone_frontend\\player\\mytxt2.txt")
#     #     time = changeTime(tests2.videoTime[i])
#     #     # keyword_k = img_string.replace("\n", " ")
#     #     # keyword = spaceText(keyword_k)
#     #     video_info = {time : keyword_list}
#     #     print(video_info)

#     # elif i>0 and compare[i] != compare[i-1] :
#     #     save_file_2Line(img_string, "C:\\Users\\hansung\\Desktop\\Capstone\\github\\Capstone_frontend\\player\\mytxt.txt")
#     #     save_file(img_string2, "C:\\Users\\hansung\\Desktop\\Capstone\\github\\Capstone_frontend\\player\\mytxt2.txt")
#     #     time = changeTime(tests2.videoTime[i])
#     #     # keyword_k = img_string.replace("\n", " ")
#     #     # keyword = spaceText(keyword_k)
#     #     video_info = {time : keyword_list}
#     #     print(video_info)
#     # else :
#     #     continue


# # cv2.imshow("threshold", img_range)
# # print(pytesseract.image_to_string(img_range,config=config))git 