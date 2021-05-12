'''
Author: 佘文轩
Date: 2021-05-11 21:27:45
LastEditTime: 2021-05-12 19:29:43
LastEditors: Please set LastEditors
Description: 剪切板图片识别生成letax公式文本
FilePath: \pythoncode\mathcopy.py
'''
import http.client
import base64
from urllib import parse
from PIL import ImageGrab
import pyperclip


def getimage():
    img = ImageGrab.grabclipboard()
    img.save('paste.jpg')

# 获得letax公式数据
def getletax(file_name):
    bin_data = open(file_name, 'rb')
    image_data = bin_data.read()
    image_data_base64 = base64.b64encode(image_data)
    image_data_base64 = parse.quote(image_data_base64)
    conn = http.client.HTTPConnection("openapiai.xueersi.com")
    appkey_string = 'app_key=8102b22a5e81e840176d9f381ec6f837'
    img_string = 'img=' + image_data_base64
    img_type_string = 'img_type=base64'
    payload = appkey_string + '&' + img_string + '&' + img_type_string
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache",
    }
    conn.request("POST", "/v1/api/img/ocr/general/", payload, headers)
    res = conn.getresponse()
    data = str(res.read())
    conn.close()
    return data


def analysis(answer):
    answer = answer.split("$$")
    formula = []
    for item in range(1, len(answer)//2, 2):
        formula.append(answer[item].replace('\\\\\\\\', '\\'))
    formula = "\\\\".join(formula)
    return formula


def writecopy(formula):
    pyperclip.copy(formula)


if __name__ == '__main__':
    try:
        getimage()
        answer = getletax('paste.jpg')
        formula = analysis(answer)
        writecopy(formula)
    except:
        pyperclip.copy("复制错误！")