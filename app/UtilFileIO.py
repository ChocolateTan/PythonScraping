# -*- coding: UTF-8 -*-
import os


class UtilFileIO:
    def __init__(self):
        pass

    def write_log_to_header(self, file_name, save_dir, write_content):
        write_content = str(write_content)
        print write_content
        file_full = save_dir + '/' + file_name
        if not os.path.exists(save_dir):
            print 'create dir', save_dir
            os.makedirs(save_dir)

        if not os.path.exists(file_full):
            print 'create file', file_full
            f = open(file_full, 'w')
            f.close()
        with open(file_full, 'r+') as f:
            content = f.read()
            f.seek(0, 0)
            f.write(write_content + '\n' + content)
            f.close()
