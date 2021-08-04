import re
from pathlib import Path
import os
import cv2
file_path = os.getcwd() + '/map/'  # 在当前目录下新建map文件夹，用于存储map中间结果图
if not os.path.exists(file_path):
    os.mkdir(file_path)

import argparse

parser = argparse.ArgumentParser()
## 从命令行指定kjdz文件夹
'''目录树如下
|- KJDZ
|--  IMAGES
|----    *.jpg
|--  ANNOTATIONS
|----    *.txt
'''
parser.add_argument("--data",
                    default=None,
                    type=str,
                    required=True,
                    help="The input data dir. Should contain all the images")
                    
parser.add_argument("--output",
                    default=None,
                    type=str,
                    required=True,
                    help="The output data dir. will contain all the labels")

args = parser.parse_args()

IMAGE_DIR = Path(args.data)
LABEL_DIR = Path(args.output)


def random_color(class_id):
    '''预定义12种颜色，基本涵盖kjdz所有label类型
    颜色对照网址：https://tool.oschina.net/commons?type=3'''
    colorArr = [(255,0,0), # 红色
                (255,255,0), # 黄色
                (0, 255, 0), # 绿色
                (0,0,255), # 蓝色
                (160, 32, 240), # 紫色
                (165, 42, 42), # 棕色
                (238, 201, 0), # gold
                (255, 110, 180), # HotPink1
                (139, 0 ,0), #DarkRed
                (0 ,139 ,139),#DarkCyan
                (139, 0 ,139),#	DarkMagenta
                (0 ,0 ,139) # dark blue
                ]
    if class_id < 11:
        return colorArr[class_id]
    else: # 如有特殊情况，类别数超过12，则随机返回一个颜色
        rm_col = (randint(0,255),randint(0,255),randint(0,255))
        return rm_col
        


# 获取 bounding-box， segmentation 信息
# 输入：image path
# 返回：
#   bounding box
#   four locations        
def get_info(im_file):
    
    img_name = str(im_file)
    
    img = cv2.imread(img_name)
    sp = img.shape
    height = sp[0]
    width = sp[1]
    print ('height: ', height)
    print ('width: ', width)
    
    dw = 1.0 / (width  )
    dh = 1.0 / (height )
   
    
    point = os.path.basename(img_name).split(".")[0]  
    #print ('get_info ', point )
    
    num  = re.findall('\d+\d*',point)  #  正则表达式 从字符串中提取数值 
    #print (num)   
    
    Xmin = min(num[3], num[5])
    Ymin = min(num[4], num[6])
    Xmax = max(num[3], num[5])
    Ymax = max(num[4], num[6])
    #print(Xmin,Ymin, Xmax,Ymax, "\n" ) 
    centerx = ((int(Xmin) + int(Xmax)) /2.0)
    centery = ((int(Ymin) + int(Ymax)) /2.0)
    width   = (int(Xmax)- int(Xmin)) 
    height  = (int(Ymax)- int(Ymin))
    
    print ('label width: ' , (int(Xmax)- int(Xmin)))
    print ("label  height:  ", (int(Ymax)- int(Ymin)))
    
    normalized_cx = centerx *dw
    normalized_cy = centery *dh
    normalized_w = width *dw
    normalized_h = height *dh
    

    
    #025-95_113-154&383_386&473-386&473_177&454_154&383_363&402-0_0_22_27_27_33_16-37-15.jpg
    #num[0] --- Area: Area ratio of license plate area to the entire picture area.  --025
    
    ## Tilt degree
    #num[1] --- Horizontal tilt degree  --95
    #num[2] --- Vertical tilt degree    -113
    
    ##Four vertices locations: The exact (x, y) coordinates of the four vertices of LP in the whole image. These coordinates start from the right-bottom vertex.
    #num[3] --- Left Up  X              -154
    #num[4] --- Left Up  Y              -383    
    #num[5] --- Right Down X            -386
    #num[6] --- Right Down Y            -473
    
    
    #num[7] --- right down coner x   
    #num[8] --- right down coner y
    #num[9] --- left down coner x    
    #num[10] --- left down coner y
    #num[11] --- left up coner x
    #num[12] --- left up coner y
    #num[13] --- right up coner x    
    #num[14] --- right up coner x

    ##License plate number
    #num[15] --- provinces index
        #provinces = ["皖", "沪", "津", "渝", "冀", "晋", "蒙", "辽", "吉", "黑", "苏", "浙", "京", "闽", "赣", "鲁", "豫", "鄂", "湘", "粤", "桂", "琼", "川", "贵", "云", "藏", "陕", "甘", "青", "宁", "新", "警", "学", "O"]
    #num[16] --- alphabets character index
        # A valid Chinese license plate consists of seven characters: province (1 character), alphabets (1 character), alphabets+digits (5 characters)
        #ads = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X','Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'O']
    #num[17] --- alphabets+digits  #1    
    #num[18] --- alphabets+digits  #2
    #num[19] --- alphabets+digits  #3
    #num[20] --- alphabets+digits  #4
    #num[21] --- alphabets+digits  #5
    
    #Brightness: The brightness of the license plate region.
    #num[22] --- Brightness
    
    #Blurriness: The Blurriness of the license plate region.
    #num[23] --- Blurriness   
    
    #lbl   = img_name.split('/')[-1].rsplit('.', 1)[0].split('-')[-3] # label: '16_2_32_30_25_29_6'
    #iname = img_name.rsplit('/', 1)[-1].rsplit('.', 1)[0].split('-')
    #[leftUp, rightDown] = [[float(eel) for eel in el.split('&')] for el in iname[2].split('_')] # bounding box
    #height = rightDown[1]-leftUp[1]
    #width = rightDown[0]-leftUp[0]
    #left = leftUp[0]
    #top = leftUp[1]
    # segmentation = [[float(eel) for eel in el.split('&')] for el in iname[3].split('_')] # four vertices locations

    #return [left, top, width, height], segmentation
    
    return [normalized_cx, normalized_cy, normalized_w, normalized_h]
    
   
    
    
def main():   
 # 初始化id（以后依次加一）
    image_id = 0
    
    print ('images folder: ', IMAGE_DIR)
    print ('labels folder: ', LABEL_DIR)

    # 加载图片信息
    im_files = [f for f in IMAGE_DIR.iterdir()]
    im_files.sort(key=lambda f: f.stem,reverse=True)  # 排序，防止顺序错乱、数据和标签不对应
    # print("im-length:",len(im_files),"\n im_files：",im_files)

    
    for im_file in im_files:
        # 写入图片信息（id、图片名、图片大小）,其中id从1开始
        segmentation = get_info(im_file)
        class_id = 1  # id 为数字形式，如 1,此时是list形式，后续需要转换 # 指定为1，因为只有”是车牌“这一类
        
         
     
        image_id += 1
        
        res = "1 " + str(segmentation[0]) + " " + str(segmentation[1]) + " " + str(segmentation[2]) + " " + str(segmentation[3])
      
        
        print (os.path.basename(im_file))
        basename = os.path.basename(im_file)
        txtname = basename.split(".")[0] + ".txt"
        outputfilepath = os.path.join (LABEL_DIR , txtname)
        print (outputfilepath)
        print(res)
        
        if not os.path.exists(LABEL_DIR):
            os.makedirs(LABEL_DIR)
            
        f = open(outputfilepath, 'w')
        f.write(res)
        f.close()
    print (image_id , ' images labeled')
    print('end')
        
        
    

    


if __name__ == "__main__":
    main()
