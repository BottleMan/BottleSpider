#!/usr/bin/python
# -*- coding:utf-8 -*-
import hashlib
import html

import dateparser
import datetime
import re
import time
import logging

from pytz import timezone


def get_cur_time():
    return get_time_in_delta()


def get_cur_date():
    return get_time_in_delta('%Y-%m-%d')


def get_time_in_delta(f='%Y-%m-%d %H:%M:%S', days=0, hours=0, minutes=0, seconds=0):
    now_time = datetime.datetime.now().astimezone(timezone('Asia/Shanghai'))
    t = now_time + datetime.timedelta(days=days,
                                      hours=hours,
                                      minutes=minutes,
                                      seconds=seconds)
    return t.strftime(f)


def parse_datetime_to_string(dt: datetime.datetime, f='%Y-%m-%d %H:%M:%S', tz='Asia/Shanghai', days=0, hours=0,
                             minutes=0, seconds=0):
    t = dt.astimezone(timezone(tz))
    t = t + datetime.timedelta(days=days,
                               hours=hours,
                               minutes=minutes,
                               seconds=seconds)
    return t.strftime(f)


def get_date_before_seconds(delsec, time_zone):
    """
    获取当前时间之前的 n 秒
    :param delsec: 前多少秒
    :param time_zone: 时区
    :return:
    """
    if time_zone == 'utc':
        now_time = datetime.datetime.utcnow()
    else:
        now_time = datetime.datetime.now().astimezone(timezone('Asia/Shanghai'))

    delsec = int(delsec)
    start_datetime = now_time - datetime.timedelta(seconds=delsec)
    start_datetime_str = time.strftime('%Y-%m-%d %H:%M:%S', start_datetime.timetuple())
    return start_datetime_str


def get_date_after_seconds(delsec, time_zone):
    """
    获取当前时间之后的 n 秒
    :param delsec: 多少秒
    :param time_zone: 时区
    :return:
    """
    if time_zone == 'utc':
        now_time = datetime.datetime.utcnow()
    else:
        now_time = datetime.datetime.now().astimezone(timezone('Asia/Shanghai'))

    delsec = int(delsec)
    start_datetime = now_time + datetime.timedelta(seconds=delsec)
    start_datetime_str = time.strftime('%Y-%m-%d %H:%M:%S', start_datetime.timetuple())
    return start_datetime_str


def get_date_before_today(delta, time_zone):
    """
    获取当前日期之前的 n 天
    :param delta: 前多少天
    :param time_zone: 时区
    :return:
    """
    delta = int(delta)
    if time_zone == 'utc':
        now_time = datetime.datetime.utcnow()
    else:
        now_time = datetime.datetime.now().astimezone(timezone('Asia/Shanghai'))

    start_date = now_time - datetime.timedelta(days=delta)
    start_date_str = time.strftime('%Y-%m-%d', start_date.timetuple())
    return start_date_str


def get_datetime_after_time(delsec, t):
    """
    获取指定时间之后的 n 秒
    :param delsec: 多少秒
    :param t: 指定时间（字符串，格式：%Y-%m-%d %H:%M:%S）
    :return:
    """
    point_datetime = datetime.datetime.strptime(t, '%Y-%m-%d %H:%M:%S')
    d = point_datetime + datetime.timedelta(seconds=delsec)
    tf = d.strftime('%Y-%m-%d %H:%M:%S')
    return tf


def datetime_format(dt, f="%Y-%m-%d %H:%M:%S"):
    """
    日期格式化
    :param dt:
    :param f:
    :return:
    """
    if not dt:
        return ''
    try:
        dt = str(dt)  # 可能有时间戳
        if '前' not in dt:
            if '年' in dt:
                dt = dt.replace('年', '-')
            if '月' in dt:
                dt = dt.replace('月', '-')
            if '日 ' in dt:
                dt = dt.replace('日', ' ')
            if '日' in dt:
                dt = dt.replace('日', ' ')
        datep = dateparser.parse(dt, settings={'TIMEZONE': 'Asia/Shanghai'})
        if datep:
            return datep.strftime(f)
        else:
            return "1970-01-01 00:00:00"
    except Exception as e:
        print(dt, e)
        return "1970-01-01 00:00:00"


def get_logger(path):
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(message)s')

    cur_date = get_cur_date()
    log_file = path + cur_date + '.log'

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(log_file)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    return logger


def e_trans_to_c(string):
    e_pun = u'%~+/|;:,.!?[]()<>"\'1234567890'
    c_pun = u'％～＋／｜；：，。！？［］（）《》“‘１２３４５６７８９０'
    table = {ord(f): ord(t) for f, t in zip(e_pun, c_pun)}
    return string.translate(table)


def un_quote_spec_str(s):
    s = filter_emoji(s)
    s = str(s) \
        .replace('*', "×") \
        .replace('\\n', "") \
        .replace('\u3000', ' ') \
        .replace('&#39;', "'") \
        .replace('&ldquo;', "“") \
        .replace('&nbsp;', " ") \
        .replace('&rdquo;', "”") \
        .replace('&hellip;', '…') \
        .replace('&quot;', '＂') \
        .replace('&middot;', '·') \
        .replace('&amp;', '＆') \
        .replace('&darr;', '↓') \
        .replace('&larr;', '←') \
        .replace('&rarr;', '→') \
        .replace('&bull;', '•') \
        .replace('&radic;', '√') \
        .replace('&yen;', '¥') \
        .replace('&eacute;', 'é') \
        .replace('&mdash;', '—')
    s = filter_str(s)

    return s


def filter_emoji(desstr, restr=''):
    res = re.compile("\&\#\d{5};")
    return res.sub(restr, desstr)


def filter_str(desstr, restr=''):
    res = re.compile("[^\u4e00-\u9fa5^a-z^A-Z^0-9^０-９]")
    return res.sub(restr, desstr)


def get_field(pattern, content, flags=0):
    field = ''
    match_obj = re.search(pattern, content, flags)
    if match_obj:
        field = match_obj.group(1)
        field = field.strip()
    return field


def get_int(s, default=-1):
    try:
        return int(s)
    except:
        return default


def get_sensitive_words(sensitive_words, content):
    sensitives = []
    for x in sensitive_words:
        if 'sensitive_word' not in x:
            continue
        if x['sensitive_word'].upper() not in content.upper():
            continue
        sensitives.append(x['sensitive_word'])
    return list(set(sensitives))


def get_all_param(params: str):
    """
    获取所有的参数，
    :param params: 参数字符串 ==>keyword=%E5%8C%97%E4%BA%AC%E7%96%AB%E6%83%85&offset=0&count=10&source=video_search
    :return:
    """
    _result = {}
    _split = params.split('&')
    for s in _split:
        __split = s.split('=')
        if len(__split) != 2:
            continue
        _result[__split[0]] = __split[1]
    return _result


def print_with_time(txt):
    print('[%s] %s' % (get_cur_time(), txt))


def md5_str(strs):
    """
    md5加密
    :param strs:
    :return:
    """
    md5 = hashlib.md5()
    if not isinstance(strs, bytes):
        strs = str(strs).encode('utf-8')
    md5.update(strs)
    return md5.hexdigest()


def remove_html_tag(html_str):
    html_str = str(html_str)
    html_str = html.unescape(html_str)
    html_str = re.compile(r'<[^>]+>', re.S).sub('', html_str)
    return html_str
