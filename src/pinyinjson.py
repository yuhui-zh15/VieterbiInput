#coding=utf-8

# Author: Zhang Yuhui
# E-mail: yuhui-zh15@mails.tsinghua.edu.cn
# Date: 20170326

import sys
import os
import json

fin = open('pinyinutf8.txt', 'r')
d = dict()

for line in fin:
    line = line[:-2]
    splitline = line.split(' ')
    d[splitline[0]] = []
    for i in xrange(1, len(splitline)):
        d[splitline[0]].append(splitline[i])
fin.close()

fout = open('pinyin.json', 'w')
fout.write(json.dumps(d))

print 'ok'


