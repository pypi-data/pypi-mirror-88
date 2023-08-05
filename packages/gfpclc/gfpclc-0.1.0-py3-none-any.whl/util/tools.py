#!/usr/bin/env python
# coding: utf-8
import json
import os
import re
import logging
import requests
from scrapy.utils.response import get_base_url
from urllib.parse import urljoin
from scrapy.http import Response
import arrow


def mrkdir(path):
    if not os.path.isdir(path):
        mrkdir(os.path.split(path)[0])
    else:
        return
    os.mkdir(path)


def unify_date(date_str):
    """
    功能:处理时间为统一格式
    :param data: str 时间字符串
    :return:
    """
    if not date_str:
        return None
    date = re.search(r'(\d+(\-|年|/)\d+(\-|月|/)\d+)', date_str)
    if date:
        date = date.group()
        return re.sub('年|月|/', '-', date)


def draftdate_from_textlines(textlines):
    """
    在正文里面去提取成文日期
    :param textlines: 正文的每一行
    :return: 提取结果
    """
    if textlines:
        textlines.reverse()
        for line in textlines:
            line = line.strip()
            is_date = re.search(r'^\d+年\d+月\d+日$', line)
            if is_date:
                return unify_date(is_date.group())


def del_quote(s):
    """
    删除字符串中的中英文冒号
    :param s: str
    :return: str
    """
    return re.sub(':|：', '', s)


def unify_url(response, url):
    """
    标准化url路径 （绝对路径和相对路径都会转换成绝对路径）
    :param response: scrapy.Response
    :param url: url
    :return:
    """
    if not isinstance(response, Response):
        logging.error("[** ERROR **] function unify_path(response, url) "
                      "papram response is not instance of scrapy.Response")
    return urljoin(get_base_url(response), url)


def getAllDayPerYear(years):
    def isLeapYear(years):
        """
        通过判断闰年，获取年份years下一年的总天数
        :param years: 年份，int
        :return:days_sum，一年的总天数
        """
        # 断言：年份不为整数时，抛出异常。
        assert isinstance(years, int), "请输入整数年，如 2018"

        if ((years % 4 == 0 and years % 100 != 0) or (years % 400 == 0)):  # 判断是否是闰年
            # print(years, "是闰年")
            days_sum = 366
            return days_sum
        else:
            # print(years, '不是闰年')
            days_sum = 365
            return days_sum
    start_date = '%s-1-1' % years
    a = 0
    all_date_list = []
    days_sum = isLeapYear(int(years))
    while a < days_sum:
        b = arrow.get(start_date).shift(days=a).format("YYYY-MM-DD")
        a += 1
        all_date_list.append(b)
    return all_date_list


def upload(url, files):
    res = requests.post(
        url=url,
        files={'file': files}
    )
    res = json.loads(str(res.content, encoding="utf-8"))

    if res.get("code") == 10000:
        return res["result"]["fileUuid"]



