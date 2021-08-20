import cv2
import os
import math
from aip import AipOcr
import base64
import time


client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
options = {}
options["detect_language"] = "true"

mode = 'web'


def print33(indexnow, indextotal, doing, title):  # 进度条
    A_count = math.floor(indexnow/indextotal*33)
    A = '#'*A_count
    B = '-'*(33-A_count)
    C = math.floor(indexnow/indextotal*1000)/10
    print('>> 正在' + doing + ' |' + A + B + '| ' +
          str(C) + '% | ' + title, flush=True)


path = './images'
list = os.listdir(path)
custom_config = r'tosp_min_sane_kn_sp=2 --oem 3 --psm 6'


def sizelimit(x, y):
    ratio = min(min(1900/x, 1900/y), 1)
    (_x, _y) = (x*ratio, y*ratio)
    return math.floor(_x), math.floor(_y)


def image_to_base64(image_np):
    # cv2.imwrite("./catch/temp.jpg",image_np)
    # with open ('./catch/temp.jpg','r') as f:
    #     return f.read()
    image = cv2.imencode('.jpg', image_np)[1]
    return image


def imgsticker(arr):
    _arr = []
    for i in arr:
        img = cv2.imread(path + '/' + i)
        _arr.append(img)
    _img = cv2.vconcat(_arr)
    return _img


def getorc(mode, img, opthon):
    if mode == 'basic':
        return client.webImage(img, opthon)
    elif mode == 'web':
        return client.basicGeneral(img, opthon)
    else:
        return None


def main():
    with open('./output_' + str(math.floor(time.time())) + '.txt', 'a+', encoding='utf-8') as f:
        _counter = 0
        list1 = cv2.imread(path+'/'+list[0])
        timestostick = list1.shape[1]//list1.shape[0]
        _list = []
        for m in range(0, math.ceil(len(list)/timestostick)):
            _m_count = m*timestostick
            _list.append(imgsticker(list[_m_count:_m_count+timestostick]))
        for i in _list:
            img = i
            resized = cv2.resize(img, sizelimit(img.shape[1], img.shape[0]))
            req = getorc(mode, image_to_base64(resized), options)
            # print(req)
            __str = req['words_result']
            _m = ''
            for m in __str:
                _m += m['words'] + '\n'
            print33(_counter, len(_list), '提取文字', _m)
            # _str +=
            f.write(_m + '\n')
            _counter += 1
        # f.write(_str)


if __name__ == "__main__":
    main()
