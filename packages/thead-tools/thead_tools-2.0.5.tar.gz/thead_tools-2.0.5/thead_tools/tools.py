# -*- coding:utf-8 -*-
#
# Copyright (C) 2019-2020 Alibaba Group Holding Limited


from __future__ import print_function
import os
import sys
import time
import hashlib
import zipfile
import codecs
import json
import re

try:
    from urlparse import urlparse
    import urllib
    import httplib as http
    urlretrieve = urllib.urlretrieve
    import urllib2 as urllib
except:
    from urllib.parse import urlparse
    import urllib.request
    import http.client as http
    urlretrieve = urllib.request.urlretrieve


try:
    import yaml
except:
    put_string("\n\nNot found pyyaml, please install: \nsudo pip install pyyaml")
    sys.exit(0)

def is_contain_chinese(check_str):
    zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
    match = zhPattern.search(check_str)
    if match:
        return True

def is_leagal_name(name):
    pattern = re.compile(u'^[_a-zA-Z]\w*$')
    match = pattern.search(name)
    if match:
        return True

def string_len(text):
    L = 0
    R = ''
    if sys.version_info.major == 2:
        if type(text) == str:
            text = text.decode('utf8')
    for c in text:
        if ord(c) >= 0x4E00 and ord(c) <= 0x9FA5:
            L += 2
        else:
            L += 1
    return L


def put_string(*args, **keys):
    for a in args:
        if sys.version_info.major == 2:
            if type(a) == unicode:
                a = a.encode('utf8')
        if 'key' in keys:
            key = keys['key']
            color_print(a, key=key, end=' ', ignorecase=True)
        else:
            print(a, end=' ')
    print()


def color_print(text, key=[], end='\n', ignorecase=False):
    idx = {}
    itext = text
    if ignorecase:
        itext = text.lower()
    for k in key:
        index = 0
        while True:
            s = itext.find(k, index)
            if s >= 0:
                e = s + len(k)
                need_del = []
                for a, b in idx.items():
                    if max(s, a) <= min(e, b):
                        s = min(s, a)
                        e = max(e, b)
                        need_del.append(a)
                for v in need_del:
                    del idx[v]
                idx[s] = e
                index = e
            else:
                break
    s = 0
    for v in list(sorted(idx)):
        e = v
        print(text[s: e], end='')
        print('\033[1;31m' + text[v: idx[v]] + '\033[0m', end='')
        s = idx[v]
    print(text[s: len(text)], end=end)


def yaml_load(filename):
    try:
        with codecs.open(filename, 'r', encoding='UTF-8') as fh:
            text = fh.read()
            return yaml.safe_load(text)
    except Exception as e:
        put_string("(%s) in file:%s" % (str(e), filename))
        exit(-1)


def home_path(path=''):
    return os.path.join(os.path.expanduser('~'), path)


def http2git(url):
    conn = urlparse(url)
    url = 'git@' + conn.netloc + ':' + conn.path[1:]
    return url


def MD5(str):
    hl = hashlib.md5()
    hl.update(str.encode(encoding='utf-8'))
    return hl.hexdigest()


def http_request(method, url, data=None, headers={}):
    conn = urlparse(url)

    if conn.scheme == "https":
        connection = http.HTTPSConnection(conn.netloc)
    else:
        connection = http.HTTPConnection(conn.netloc)
    # connection.debuglevel = 1

    connection.request(method=method, url=conn.path + '?' +
                       conn.query, body=data, headers=headers)
    response = connection.getresponse()
    return response.status, response.read(), response.msg



def http_get(url, path):
    conn = urlparse(url)

    if conn.scheme == "https":
        connection = http.HTTPSConnection(conn.netloc)
    else:
        connection = http.HTTPConnection(conn.netloc)

    connection.request('GET', conn.path)
    response = connection.getresponse()

    filename = os.path.join(path, os.path.basename(conn.path))

    try:
        with codecs.open(filename, 'wb', encoding='UTF-8') as f:
            f.write(response.read())
    except:
        pass

    return filename


def wget(url, out_file):
    start_time = time.time()

    def barProcess(blocknum, blocksize, totalsize):
        speed = (blocknum * blocksize) / (time.time() - start_time)
        # speed_str = " Speed: %.2f" % speed
        speed_str = " Speed: %sB/S         " % format_size(speed)
        recv_size = blocknum * blocksize

        # 设置下载进度条
        f = sys.stdout
        percent = float(recv_size) / totalsize
        if percent > 1:
            percent = 1
        percent_str = " %.2f%%" % (percent * 100)
        n = int(percent * 50)
        s = ('#' * n).ljust(50, '-')
        f.write(percent_str.ljust(9, ' ') + '[' + s + ']' + speed_str)
        f.flush()
        f.write('\r')

    def format_size(bytes):
        bytes = float(bytes)
        kb = bytes / 1024
        if kb >= 1024:
            M = kb / 1024
            if M >= 1024:
                G = M / 1024
                return "%.3fG" % (G)
            else:
                return "%.3fM" % (M)
        else:
            return "%.3fK" % (kb)

    return urlretrieve(url, out_file, barProcess)
