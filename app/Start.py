# -*- coding: UTF-8 -*-
import json
import random
import time

import sys

import thread

import GlobalList
from GlobalList import Init
from UtilFileIO import UtilFileIO
from UtilScraping import UtilScraping
from lxml import etree, html

reload(sys)
sys.setdefaultencoding('utf8')  # gb2312,gbk


def scrap_api(start_num, end_num):
    file_name = '{0}_{1}_{2}.txt'.format(GlobalList.SAVE_FILE_NAME, start_num, end_num)
    for book_id in range(start_num, end_num + 1):
        random_time = random.randint(1, 3)
        time.sleep(random_time)
        request_url = 'http://smp3.yoedge.com/view/gotoAppLine/{0}'.format(book_id)
        html_result = UtilScraping().read_url(url=request_url, num_retries=0)
        # html = etree.parse('hello.html')
        if html_result is not None:
            # result = html.fromstring(result)
            con = etree.HTML(html_result)
            img = con.xpath('//img')
            abbr = con.xpath('//abbr')
            detail = con.xpath("//div[@style='font-size:0.8em;line-height:1.2em']")
            # [@style='font-size:200%']
            book_cover = ''
            book_name = ''
            book_author = ''
            book_detail = ''
            if len(img) > 0:
                book_cover = img[0].get('src')
            if len(abbr) > 0:
                index = 0
                for item in abbr:
                    conss = etree.HTML(etree.tostring(item))
                    string = conss.xpath('string()').strip()

                    if index == 0:
                        book_name = string
                    if index == 1:
                        book_author = string

                    index = index + 1

            if len(detail) > 0:
                conss = etree.HTML(etree.tostring(detail[0]))
                book_detail = conss.xpath('string()').strip()

            time_format = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print 'book_cover', book_cover
            print 'book_name', book_name
            print 'book_author', book_author
            print 'book_detail', book_detail

            content = {
                'id': book_id,
                'url': request_url,
                'book_cover': book_cover,
                'book_name': book_name,
                'book_author': book_author,
                'book_detail': '' + book_detail,
                'create_time': time_format,
                'random_time': random_time
            }
            print 'isinstance(b,unicode)', isinstance(str(content), unicode)
            UtilFileIO().write_log_to_header(file_name=file_name,
                                             save_dir=GlobalList.PATH_CACHE_ROOT,
                                             write_content=str(
                                                 json.dumps(content, encoding="UTF-8", ensure_ascii=False)))
    print 'scrap finish from {0} to {1}'.format(start_num, end_num)


if __name__ == '__main__':
    Init()
    try:
        # thread.start_new_thread(scrap_api, (1000000, 1000999))
        # thread.start_new_thread(scrap_api, (1001000, 1001999))
        # thread.start_new_thread(scrap_api, (1002000, 1002999))
        # thread.start_new_thread(scrap_api, (1003000, 1003999))
        # thread.start_new_thread(scrap_api, (1004000, 1004999))
        # thread.start_new_thread(scrap_api, (1005000, 1005999))
        # thread.start_new_thread(scrap_api, (1006000, 1006999))
        # thread.start_new_thread(scrap_api, (1007000, 1007999))
        # thread.start_new_thread(scrap_api, (1008000, 1008999))
        # thread.start_new_thread(scrap_api, (1009000, 1009999))
        # thread.start_new_thread(scrap_api, (1010000, 1019999))
        # thread.start_new_thread(scrap_api, (1018646, 1019999))
        # thread.start_new_thread(scrap_api, (1027305, 1029999))
        # thread.start_new_thread(scrap_api, (1037079, 1039999))
        # thread.start_new_thread(scrap_api, (1047396, 1049999))
        # thread.start_new_thread(scrap_api, (1057268, 1059999))
        # thread.start_new_thread(scrap_api, (1067576, 1069999))
        # thread.start_new_thread(scrap_api, (1077443, 1079999))
        # thread.start_new_thread(scrap_api, (1087452, 1089999))
        # thread.start_new_thread(scrap_api, (1097419, 1099999))
        # thread.start_new_thread(scrap_api, (1107482, 1109999))
        # thread.start_new_thread(scrap_api, (1020000, 1029999))
        # thread.start_new_thread(scrap_api, (1030000, 1039999))
        # thread.start_new_thread(scrap_api, (1040000, 1049999))
        # thread.start_new_thread(scrap_api, (1050000, 1059999))
        # thread.start_new_thread(scrap_api, (1060000, 1069999))
        # thread.start_new_thread(scrap_api, (1070000, 1079999))
        # thread.start_new_thread(scrap_api, (1080000, 1089999))
        # thread.start_new_thread(scrap_api, (1090000, 1099999))
        # thread.start_new_thread(scrap_api, (1100000, 1109999))
        # thread.start_new_thread(scrap_api, (1110000, 1119999))
        # thread.start_new_thread(scrap_api, (1120000, 1129999))
        # thread.start_new_thread(scrap_api, (1130000, 1139999))
        # thread.start_new_thread(scrap_api, (1140000, 1149999))
        # thread.start_new_thread(scrap_api, (1150000, 1159999))
        # thread.start_new_thread(scrap_api, (1160000, 1169999))
        # thread.start_new_thread(scrap_api, (1170000, 1179999))
        # thread.start_new_thread(scrap_api, (1180000, 1189999))
        # thread.start_new_thread(scrap_api, (1190000, 1199999))

        for index in range(100):
            start = 1100000 + 1000 * index
            end = 1100000 + 1000 * index + 999
            # thread.start_new_thread(scrap_api, (start, end))
            print 'start,end', start, end

        while True:
            time.sleep(1)
            pass
    except:
        print 'thread error'
