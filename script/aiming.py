from PIL import Image, ImageDraw, ImageFont
import cv2 as cv
import numpy as np


def cv2ImgAddText(img, text, left, top, textColor=(0, 0, 0), textSize=30):
    if (isinstance(img, np.ndarray)):  #判断是否OpenCV图片类型
        img = Image.fromarray(cv.cvtColor(img, cv.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)
    fontText = ImageFont.truetype(
        "fonts/simsun.ttc", textSize, encoding="utf-8")
    draw.text((left, top), text, textColor, font=fontText)
    return cv.cvtColor(np.asarray(img), cv.COLOR_RGB2BGR)




def imgAddText(img, text, left, top, danger_area,count,danger_num,textColor=(0, 0, 255), textSize=30):
    # image = Image.open(image_path).convert('RGB')

    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(r'/disk2/yjh/font/simsun.ttc', textSize,encoding="utf-8")
    text = "total_num:{},danger_num:{} ".format(count, danger_num)
    draw.text((4, 4), text, font = font, fill=textColor)

def draw_rectang(img,danger_area, bbox):
    '''
    :param img:
    :param danger_area: [(x_min, y_min), (x_max, y_min), (x_max, y_max), (x_min, y_max)]
    :return:
    '''

    danger_num = 0 # danger nums
    cout = 0 # count
    xmin, ymin, xmax, ymax = bbox[0], bbox[1], bbox[2], bbox[3]
    x_min, y_min, x_max, y_max = danger_area[0][0], danger_area[0][1], danger_area[2][0], danger_area[2][1]
    draw = ImageDraw.Draw(img)
    draw.line(danger_area, width=4, fill=128)  #draw danger area

    if (xmin >= x_min and xmin <= x_max and ymin >= y_min and ymin <= y_max) or (
            xmax >= x_min and xmax <= x_max and ymax >= y_min and ymax <= y_max) or (
            xmax >= x_min and xmax <= x_max and ymin >= y_min and ymin <= y_max) or (
            xmin >= x_min and xmin <= x_max and ymax >= y_min and ymax <= y_max):
        danger_num += 1

    return cout, danger_num









if __name__ == '__main__':
    count = 10
    danger_num = 3
    image_path = 'pic.png'
    left, top = 4, 4

    image = Image.open(image_path).convert('RGB')
    text = "total_num:{},danger_num:{} ".format(count, danger_num)
    imgAddText(image, text, left, top)







