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

def draw_bbox(image, im_id, catid2name, bboxes, threshold):
    """
    Draw bbox on image
    """
    draw = ImageDraw.Draw(image)

    #dangerous areas
    w, h = image.size[0], image.size[1]
    danger = [(w/5, h/4), (w*3/5, h/4), (w*3/5, h*3/4), (w/5, h*3/4),  (w/5, h/4)]
    x_min, y_min = danger[0][0],danger[0][1]
    x_max, y_max = danger[2][0], danger[2][1]
    draw.line(danger, width=4, fill=128)
    red_flag = 3



    catid2color = {}
    color_list = colormap(rgb=True)[:40]

    count = 0  #count person nums
    danger_num = 0

    for dt in np.array(bboxes):
        if im_id != dt['image_id']:
            continue
        catid, bbox, score = dt['category_id'], dt['bbox'], dt['score']
        if score < threshold:
            continue
        count += 1

        if catid not in catid2color:
            idx = np.random.randint(len(color_list))
            catid2color[catid] = color_list[idx]
        color = tuple(catid2color[catid])

        # draw bbox
        if len(bbox) == 4:
            # draw bbox
            xmin, ymin, w, h = bbox
            xmax = xmin + w
            ymax = ymin + h
            if (xmin >= x_min and xmin <= x_max and ymin >= y_min and ymin <= y_max) or (xmax >= x_min and xmax <= x_max and ymax >= y_min and ymax <= y_max) or (xmax >= x_min and xmax <= x_max and ymin >= y_min and ymin <= y_max) or (xmin >= x_min and xmin <= x_max and ymax >= y_min and ymax <= y_max):

                danger_num += 1

            #if x_min <= xmin and x_max >= xmax and y_min <= ymin and y_max >= ymax:
             #   danger_num += 1

            draw.line(
                [(xmin, ymin), (xmin, ymax), (xmax, ymax), (xmax, ymin),
                 (xmin, ymin)],
                width=2,
                fill=(0, 255, 0))
        elif len(bbox) == 8:
            print("out"*30)
            x1, y1, x2, y2, x3, y3, x4, y4 = bbox
            draw.line(
                [(x1, y1), (x2, y2), (x3, y3), (x4, y4), (x1, y1)],
                width=2,
                fill=color)
            xmin = min(x1, x2, x3, x4)
            ymin = min(y1, y2, y3, y4)
        else:
            logger.error('the shape of bbox must be [M, 4] or [M, 8]!')

        # draw label
        text = "{}".format(count)
        text_danger = "{}".format(danger_num)
        #text = "{},{} ".format(count, danger_num)
        #text ="{} {:.2f}".format(catid2name[catid], score)
        font = ImageFont.truetype(r'/disk2/yjh/font/simsun.ttc', 20)
        tw, th = draw.textsize(text)
        tw, th = float(15), float(20)
        #draw.rectangle(
        #    [(xmin + 1, ymin - th), (xmin + tw + 1, ymin)], fill=(0, 0, 255))
        #draw.text((xmin + 1, ymin - th), text,font = font, fill=(255, 255, 255))

        draw.rectangle(
            [(x_min + 1, y_min - th), (x_min + tw + 1, y_min)], fill=(255, 0, 0))
        draw.text((x_min + 1, y_min - th), text_danger,font = font, fill=(255, 255, 255))

    #print("total:", count)
    #print("count:", count)
    font = ImageFont.truetype(r'/disk2/yjh/font/simsun.ttc', 30)
    title = "total_num:{},danger_num:{} ".format(count, danger_num)
    draw.text((4, 4), title, font = font, fill=(0, 0, 230))

    print(text)
    return image



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







