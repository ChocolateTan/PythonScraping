# -*- coding: UTF-8 -*-
import os
import urllib
import urllib2


class UtilScraping:
    def __init__(self):
        pass

    def read_url(self, url, user_agent='wswp', num_retries=2):
        print 'Reading:', url
        headers = {'User-agent': user_agent}
        request = urllib2.Request(url, headers=headers)
        try:
            html = urllib2.urlopen(request).read()
        except Exception as e:
            print 'Reading error:', e
            html = None
            if num_retries > 0:
                if hasattr(e, 'code') and 500 <= e.code < 600:
                    # retry 5xx http errors
                    return self.read_url(url=url, user_agent=user_agent, num_retries=num_retries - 1)
        return html

    def download(self, url, user_agent='wswp', num_retries=2, file_name='', save_dir=''):
        if file_name == '':
            file_name = url.split("/")[-1]
            if file_name.endswith('.html') is False:
                file_name = file_name + '.html'

        if save_dir == '':
            local_dir = os.getcwd() + '/downloads'
        else:
            local_dir = save_dir

        save_dir = os.path.join(local_dir, file_name)

        if not os.path.exists(local_dir):
            print '\nmk dir', local_dir
            os.makedirs(local_dir)

        try:
            print '\nDownloading ', url
            urllib.urlretrieve(url, save_dir)
            print '\nSuccess Download URL:', url
        except Exception as e:
            print '\nError when retrieving the URL:', url
            print e
            if num_retries > 0:
                if hasattr(e, 'code') and 500 <= e.code < 600:
                    # retry 5xx http errors
                    return self.download(url=url,
                                         user_agent=user_agent,
                                         num_retries=num_retries - 1,
                                         file_name=file_name,
                                         save_dir=save_dir)

# download(url="http://smp3.yoedge.com/view/gotoAppLine/1070219")
