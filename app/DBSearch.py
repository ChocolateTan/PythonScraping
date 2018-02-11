# -*- coding: UTF-8 -*-
# import pymongo
#
# connection = pymongo.Connection('localhost', 27017)
#
# db = connection.db_comic
import os
import json
from collections import Counter
import time
from bson import json_util
import jieba
import jieba.analyse
from optparse import OptionParser
from pymongo import MongoClient

from UtilFileIO import UtilFileIO
import GlobalList
import sys
import pandas as pd
from pandas import Series, DataFrame

reload(sys)
sys.setdefaultencoding('utf-8')
conn = MongoClient('localhost', 27017)
# 连接mydb数据库，没有则自动创建
db = conn.db_comic
# 使用test_set集合，没有则自动创建
my_set = db.set_comic
set_comic_list = db.set_comic_list


def insert_db():
    path = "/Users/don/Downloads/PythonScraping/app/cache"  # 文件夹目录
    files = os.listdir(path)  # 得到文件夹下的所有文件名称
    s = []
    for file_name in files:  # 遍历文件夹
        if file_name == 'posts':
            return
        print 'file_name', file_name
        if not os.path.isdir(file_name):  # 判断是否是文件夹，不是文件夹才打开
            f = open(path + "/" + file_name)  # 打开文件
            iter_f = iter(f)  # 创建迭代器
            for line in iter_f:  # 遍历文件，一行行遍历，读取文本
                # print json.loads(line, encoding="UTF-8")
                # print type(line)
                dict_line = json.loads(line)
                dict_line['file_name'] = file_name
                # print dict_line
                # print json.dumps(dict_line, encoding="UTF-8", ensure_ascii=False)
                # print type(json.loads(line))
                # line_json['']
                my_set.insert(dict_line)
            print file_name + ' finish'


def find_db():
    group = {
        '_id': {
            'book_name': '$book_name',
            'book_cover': '$book_cover',
            'book_detail': '$book_detail',
            'book_author': '$book_author',
            'create_time': 'create_time'
        },
        'book_count': {'$sum': 1},
        'urls': {'$push': '$url'}
    }
    # limit = {'$limit': 5}
    # data = db.set_comic.aggregate([{'$group': group}, {'$limit': 1}])
    data = db.set_comic.aggregate([{'$group': group}])
    data = list(data)
    # data = json.dumps(data, encoding="UTF-8", ensure_ascii=False)
    for dict_line in data:
        urls = ''
        time_format = time.strftime("%Y-%m-%d", time.localtime())
        time_format2 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        book_name = dict_line['_id']['book_name']
        book_name = book_name.replace('×', '').replace(':', '').replace('/', '份').replace('(', '').replace(')',
                                                                                                           '').replace(
            ' ', '').replace('~', '').replace('+', '').replace('？', '').replace('！', '').replace('*', '')
        book_detail = dict_line['_id']['book_detail'].replace('[', '').replace(']', '').replace('"', '')
        for url_line in dict_line['urls']:
            # [http://smp3.yoedge.com/view/gotoAppLine/1125059](http://smp3.yoedge.com/view/gotoAppLine/1125059)
            url_format = '[{0}]({1})\n'.format(url_line, url_line)
            urls = urls + url_format
        urls = '\n' + urls
        sb = '''---
layout: post
title: "{0}"
date: "{1}"
image: '{2}'
description: {3}
introduction: {4}
---
入口
{5}
        '''.format(book_name,
                   time_format2,
                   dict_line['_id']['book_cover'],
                   book_detail,
                   book_detail,
                   urls)
        # 2012-10-10-seja-bem-vindo
        # 2018-02-02-post-測試
        print 'book_name', book_name

        file_name = time_format + '-' + book_name + '.md'
        UtilFileIO().write_log_to_header(file_name=file_name,
                                         save_dir='/Users/don/Downloads/PythonScraping/app/cache/posts',
                                         write_content=sb)

        # UtilFileIO().write_log_to_header(file_name='Z_BookInfo.txt',
        #                                  save_dir='/Users/don/Downloads/PythonScraping/app/cache',
        #                                  write_content=data)
        # for dict_line in data:
        #     data = json.dumps(dict_line, encoding="UTF-8", ensure_ascii=False)
        #     # data = data.encode('unicode-escape').decode('string_escape')
        #     print data
        #     # print type(data)
        #     # content = json.dumps(dict_line, encoding="UTF-8", ensure_ascii=False)
        #     UtilFileIO().write_log_to_header(file_name='Z_BookInfo.txt',
        #                                      save_dir='/Users/don/Downloads/PythonScraping/app/cache',
        #                                      write_content=data)


def work_count():
    group = {
        '_id': {
            'book_name': '$book_name',
            'book_cover': '$book_cover',
            'book_detail': '$book_detail',
            'book_author': '$book_author',
            'create_time': 'create_time'
        },
        'book_count': {'$sum': 1},
        'urls': {'$push': '$url'}
    }
    # limit = {'$limit': 5}
    # data = db.set_comic.aggregate([{'$group': group}, {'$limit': 1}])
    data = db.set_comic.aggregate([{'$group': group}])
    data = list(data)

    file_path = os.path.dirname(os.path.abspath(__file__)) + '/stop.txt'
    stopwords = open(file_path, 'r').read()

    # print 'stopwords', stopwords
    for dict_line in data:
        urls = dict_line['urls']
        book_name = dict_line['_id']['book_name']
        book_cover = dict_line['_id']['book_cover']
        book_detail = dict_line['_id']['book_detail']

        seg_list_name = jieba.cut(book_name, cut_all=False)
        seg_list_detail = jieba.cut(book_detail, cut_all=False)
        # allowPOS=('ns', 'n', 'vn', 'v')
        name_keyword = jieba.analyse.textrank(book_name, topK=20, withWeight=False,
                                              allowPOS=('ns', 'n', 'a', 'nr', 'nz', 'al', 'vn', 'v'))
        detail_keyword = jieba.analyse.textrank(book_detail, topK=20, withWeight=False,
                                                allowPOS=('ns', 'n', 'a', 'nr', 'nz', 'al', 'vn', 'v'))
        catagroy = jieba.analyse.textrank(book_name, topK=1, withWeight=False,
                                          allowPOS=('ns', 'n', 'a', 'nr', 'nz''al', 'vn', 'v'))

        name_seg = list(seg_list_name)
        detail_seg = list(seg_list_detail)
        name_keyword = list(name_keyword)
        detail_keyword = list(detail_keyword)

        name_seg_new = []
        detail_seg_new = []
        # print stopwords
        for seg in name_seg:
            if seg not in stopwords:
                name_seg_new.append(seg)
        for seg in detail_seg:
            if seg not in stopwords:
                detail_seg_new.append(seg)
        new_line = {
            'name_seg': name_seg_new,
            'detail_seg': detail_seg_new,
            'name_seg_count': Counter(name_seg_new),
            'detail_seg_count': Counter(detail_seg_new),
            'book_name': book_name,
            'book_cover': book_cover,
            'book_detail': book_detail,
            'urls': urls,
            'name_keyword': name_keyword,
            'detail_keyword': detail_keyword,
            'catagroy': catagroy
        }

        set_comic_list.insert(new_line, check_keys=False)


def out_put_post():
    data = db.set_comic_list.find()#.limit(1)
    data = list(data)
    for dict_line in data:
        print dict_line
        urls = ''
        time_format = time.strftime("%Y-%m-%d", time.localtime())
        time_format2 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        book_name = dict_line['book_name']
        book_name = book_name.replace('×', '').replace(':', '').replace('/', '份').replace('(', '').replace(')',
                                                                                                           '').replace(
            ' ', '').replace('~', '').replace('+', '').replace('？', '').replace('！', '').replace('*', '')
        book_detail = dict_line['book_detail'].replace('[', '').replace(']', '').replace('"', '')
        word = ''

        if len(dict_line['catagroy']) > 0:
            category = dict_line['catagroy'][0]
        else:
            category = '其他'

        if len(dict_line['name_seg']) > 0:
            list_tag = dict_line['name_seg']
        else:
            list_tag = dict_line['detail_keyword']

        for keyword_line in list_tag:
            word_format = '- {0}\n'.format(keyword_line)
            word = word + word_format

        for url_line in dict_line['urls']:
            # [http://smp3.yoedge.com/view/gotoAppLine/1125059](http://smp3.yoedge.com/view/gotoAppLine/1125059)
            url_format = '[{0}]({1})\n'.format(url_line, url_line)
            urls = urls + url_format
        urls = '\n' + urls
        sb = '''---
layout: blog
title: "{0}"
category: {7}
date: "{1}"
background-image: '{2}'
tags:
{6}
---
{3}
{4}
入口
{5}
        '''.format(book_name,
                   time_format2,
                   dict_line['book_cover'],
                   book_detail,
                   book_detail,
                   urls,
                   word,
                   category)
        # 2012-10-10-seja-bem-vindo
        # 2018-02-02-post-測試
        print 'book_name', book_name

        file_name = time_format + '-' + book_name + '.md'
        UtilFileIO().write_log_to_header(file_name=file_name,
                                         save_dir='/Users/don/Downloads/PythonScraping/app/cache/posts',
                                         write_content=sb)


# sudo mongod
# mongo
if __name__ == '__main__':
    # insert_db()
    # find_db()
    # limit = {'$limit': 5}
    # data = db.set_comic.aggregate([{'$group': group}, {'$limit': 1}])
    # data = db.set_comic.find()

    # work_count()

    # data = list(data)
    # data_name = []
    # data_name = []
    # for dict_line in data:
    #     name_seg = dict_line['name_seg']
    #     detail_seg = dict_line['detail_seg']
    #     name_seg_count = dict_line['name_seg_count']
    #     detail_seg_count = dict_line['detail_seg_count']
    #     book_name = dict_line['book_name']
    #     book_cover = dict_line['book_cover']
    #     book_detail = dict_line['book_detail']
    #     urls = dict_line['urls']
    out_put_post()

    print 'finish...'
