#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import sys
import os
from os.path import join, getsize

#refs http://www.5dollarwhitebox.org/drupal/node/84
def convert_bytes(bytes):
    bytes = float(bytes)
    if bytes >= 1099511627776:
        terabytes = bytes / 1099511627776
        size = '%.2fT' % terabytes
    elif bytes >= 1073741824:
        gigabytes = bytes / 1073741824
        size = '%.2fG' % gigabytes
    elif bytes >= 1048576:
        megabytes = bytes / 1048576
        size = '%.2fM' % megabytes
    elif bytes >= 1024:
        kilobytes = bytes / 1024
        size = '%.2fK' % kilobytes
    else:
        size = '%.2fb' % bytes
    return size

if __name__ == '__main__':
    try:
        options = '[chm|pdf]'
        pattern = r'(^.*\([0-9]+\)\.'+options+'+$)'
        greeting = u"请输入绝对路径:>>>>\n"
        path = raw_input(greeting.encode('utf8'))
        dupfiles = []
        size = 0

        if os.path.exists(path):
            for root, dirs, files in os.walk(path):
                for file in files:
                    filename = os.path.join(root,file)
                    dup = re.match(pattern, filename)
                    if dup:
                        each_size = getsize(filename)
                        size += each_size
                        dupfiles.append((file ,convert_bytes(each_size)))
                        #origfile = dup.group()
                        origs = re.match(r'(^.*?.)\([0-9]+\)\.('+options+'+)$',file)
                        if origs:
                            try:
                                origname = origs.groups()[0]+'.'+origs.groups()[1]
                                origfile = os.path.join(root, origname)
                            except Exception, e:
                                print 'Error::: %s' % str(e)

                        if os.path.exists(origfile):
                            origsize = getsize(origfile)
                        else:
                            origsize = 0
                        print origsize, each_size
                        if origsize >= each_size:
                            print 'removing...'
                            os.remove(filename)
                        elif 0 < origsize < each_size:
                            print 'renaming...'
                            os.rename(filename, origfile)
                        else:
                            print 'None'

        else:
            print u"路径无效\n"

    except Exception, e:
        sys.exit()
    else:
        sys.exit()
        pass
    finally:
        print u"重复文件总数::: %s\n 释放资源:::%s\n" % (len(dupfiles), convert_bytes(size))
        for file, size in dupfiles:
            print u"***********\nname:%s\nsize:%s\n" % (file, size)
        pass


