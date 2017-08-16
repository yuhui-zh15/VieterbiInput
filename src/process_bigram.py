#coding=utf-8

# Author: Zhang Yuhui
# E-mail: yuhui-zh15@mails.tsinghua.edu.cn
# Date: 20170326

import sys
import os
import json

with open('hanzibiaoutf8.txt', 'r') as f:
    s = f.read()
    s = s.decode('utf-8')

start_probability = dict() #一维
transition_probability = dict() #二维
num = 0
for i in xrange(0, len(s)):
    transition_probability[s[i]] = dict()
    start_probability[s[i]] = 0

print 'Build Dictionary ... OK'

filelist = os.listdir('sina_news')
for file in filelist:
    file = './sina_news/' + file;
    if 'txt' not in file: continue
    fin = open(file, 'r')
    for line in fin:
        data = json.loads(line)
        title = data['title']
        html = data['html']
        num += len(title)
        num += len(html)
        for i in xrange(0, len(title)):
            if title[i] in start_probability:
                start_probability[title[i]] += 1; 
                if i + 1 != len(title) and title[i + 1] in start_probability:
                    if title[i + 1] not in transition_probability[title[i]]:
                        transition_probability[title[i]][title[i + 1]] = 1
                    else:
                        transition_probability[title[i]][title[i + 1]] += 1
        for i in xrange(0, len(html)):
            if html[i] in start_probability:
                start_probability[html[i]] += 1; 
                if i + 1 != len(html) and html[i + 1] in start_probability:
                    if html[i + 1] not in transition_probability[html[i]]:
                        transition_probability[html[i]][html[i + 1]] = 1
                    else:
                        transition_probability[html[i]][html[i + 1]] += 1
    print 'Process ' + file + ' ... OK'
    fin.close()

with open('start_probability.json', 'w') as fout:
    fout.write(json.dumps(start_probability))

with open('transition_probability.json', 'w') as fout:
    fout.write(json.dumps(transition_probability))

with open('num.txt', 'w') as fout:
    fout.write(str(num))

print 'Save Dictionary ... OK'


