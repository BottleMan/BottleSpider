# -*- coding:utf-8 -*-
import requests
import json
import re

from base64 import b64decode


def b64_padding(b64_str):
    """
    base64 字符串结尾补齐 =
    """
    missing_count = 4 - len(b64_str) % 4

    while missing_count:
        b64_str += '='
        missing_count -= 1
    return b64_str


def auto_b64decode(b64_str):
    """
    base64 字符解码
    """

    # 特殊字符处理
    b64_str = re.sub(r'-', '+', b64_str)
    b64_str = re.sub(r'_', '/', b64_str)
    b64_str = re.sub(r'[^A-Za-z0-9\+\/]', '', b64_str)

    # 补 = 操作
    b64_str = b64_padding(b64_str)

    return b64decode(b64_str)


def get_decode_text(txt):
    """
    文本解密
    """

    # 先处理掉多于的字符
    txt = re.sub('[\\\\|\n]', '', txt)

    # 执行解密步骤（翻译自 JS）
    split = txt[0: int(1e3)]
    split = list(split)
    for idx, s in enumerate(split):
        split[idx] = chr(ord(s) - idx % 2)
    split = ''.join(split)
    txt = '%s%s' % (split, txt[int(1e3):])

    # 将得到的 base64 字符串进行解码
    return auto_b64decode(txt)


# 获取页面内的加密内容
def get_encode_text(text):
    print(text)
    if '__INITIAL_DATA__' in text:
        pattern = "window.__INITIAL_DATA__ = '([\w\W]*?)';"
        ret = re.findall(pattern, text)

        if ret and ret[0]:
            return ret[0]
    return ''


if __name__ == '__main__':
    # 请求测试页面
    test_url = 'https://www.360kuai.com/9b091e35e504e3239'
    res = requests.get(test_url)
    content = res.text

    # 获取加密数据
    text_encode = get_encode_text(content)

    print(text_encode)

    # 解密数据
    text_decode = get_decode_text(text_encode)
    obj_decode = json.loads(text_decode)

    print(obj_decode)

    # 获取需要的字段
    title = obj_decode['detail']['title']
    pub_time = obj_decode['detail']['pub_time']
    src = obj_decode['detail']['src']
    content = obj_decode['detail']['content']

    print("title: %s" % title)
    print("pub_time: %s" % pub_time)
    print("src: %s" % src)
    print("content: %s" % content)
