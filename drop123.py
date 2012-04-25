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
    '''
    options = '(chm|pdf|pdf.part|chm.part|chm.chm)'
    pattern = r'(^.*\([0-9]+\)\.'+options+'$)'
    origs = re.match(r'(^.*?.)\([0-9]+\)\.'+options+'+$', 'asdfasf(2).pdf.part')
    print origs.groups()
    print re.match(pattern, 'asdfasdf(2).chm.chm').groups()
    sys.exit()
    '''

    try:
        # 异常部分
        ext_table = ['.part']
        options = '(chm|pdf|chm.part|pdf.part|tar.gz|tar|rar|zip)'
        pattern = r'(^.*\([0-9]+\)\.'+options+'+$)'
        greeting = u"请输入绝对路径:>>>>\n"
        path = raw_input(greeting.encode('utf8'))
        dupfiles = []
        allsize = 0

        if os.path.exists(path):
            for root, dirs, files in os.walk(path):
                for file in files:
                    filename = os.path.join(root,file)
                    dup = re.match(pattern, filename)
                    if dup:
                        each_size = getsize(filename)
                        allsize += each_size
                        dupfiles.append((file ,convert_bytes(each_size)))
                        origs = re.match(r'(^.*?.)\([0-9]+\)\.'+options+'+$',file)
                        if origs:
                            try:
                                origs_tuple = origs.groups()
                                '''Todo::: 文件明额外部分应取得'''
                                for ext in ext_table:
                                    if ext in origs_tuple[1]:
                                        origname = \
                                        origs_tuple[0]+'.'+''.join(origs_tuple[1].split(ext))
                                    else:
                                        origname = \
                                        origs_tuple[0]+'.'+origs_tuple[1]
                                #print 'ori::::%s' % origname
                                #print filename
                                origfile = os.path.join(root, origname)
                            except Exception, e:
                                print 'Error::: %s' % str(e)

                        if os.path.exists(origfile):
                            origsize = getsize(origfile)
                        else:
                            origsize = 0

                        if origsize > 0:
                            if origsize >= each_size:
                                #print u'原文件大于等于重复文件:::删除重复文件'
                                os.remove(filename)
                            elif origsize < each_size:
                                #print u'原文件小于重复文件:::替换成原文件'
                                os.rename(filename, origfile)
                        else:
                            if origsize <= each_size:
                                #print u"不存在原文件:::创建原文件"
                                os.rename(filename, origfile)


        else:
            print u"路径无效\n"

    except Exception, e:
        sys.exit()
    else:
        sys.exit()
    finally:
        for file, size in dupfiles:
            print u"***********\nname:%s\nsize:%s\n" % (file, size)

        print u"重复文件总数::: %s\n 释放资源:::%s\n" % (len(dupfiles), convert_bytes(allsize))
