import os
import requests
import time
import uuid
from iupdatable.system.hardware.CSProduct import CSProduct
import ctypes
import locale
import urllib


class UMeng(object):

    @classmethod
    def log_stat(cls, id, page, category='', action='', label='', value=0):
        os.environ['NO_PROXY'] = 'cnzz.com'
        host_url = 'https://ei.cnzz.com/stat.htm'
        um_uuid = cls.get_um_uuid()
        user32 = ctypes.windll.user32
        resolution = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        lang = locale.getdefaultlocale()[0]
        ei = urllib.parse.quote_plus(f'{category}|{action}|{label}|{value}|')
        rnd = int(time.time())
        page = urllib.parse.quote_plus('http://' + page)
        url = host_url + f'?id={id}&lg={lang}&ei={ei}&p={page}' \
                         f'&umuuid={um_uuid}&showp={resolution[0]}x{resolution[1]}&h=1'
        response = requests.get(url)

    @staticmethod
    def get_um_uuid():
        # section1
        timestamp = int(round(time.time() * 1000))
        d = 0
        while timestamp == int(round(time.time() * 1000)):
            d += 1
        section1 = format(timestamp, 'x') + format(d, 'x')
        # section2
        section2 = str(uuid.uuid1()).replace('-', '')[:14]
        # section3
        section3 = str(uuid.uuid1()).replace('-', '')[:6]
        # section4
        user32 = ctypes.windll.user32
        screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        section4 = format(screensize[0] * screensize[1], 'x')
        return '{0}-{1}-{2}-{3}'.format(section1, section2, section3, section4)
