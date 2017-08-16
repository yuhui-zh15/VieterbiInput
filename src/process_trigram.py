#coding=utf-8

# Author: Zhang Yuhui
# E-mail: yuhui-zh15@mails.tsinghua.edu.cn
# Date: 20170326

import sys
import os
import json

hanzi = set()

with open('hanzibiaoutf8.txt', 'r') as f:
    s = f.read()
    s = s.decode('utf-8')

for i in xrange(0, len(s)):
    hanzi.add(s[i])
start_probability = dict() #一维
transition_probability = dict() #二维
num = 0

print 'Build Dictionary ... OK'

filecnt = 0
filelist = os.listdir('sina_news')
for file in filelist:
    filecnt += 1
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
            if i + 1 >= len(title) or title[i] not in hanzi or title[i + 1] not in hanzi: continue
            if (title[i] + title[i + 1]) not in start_probability:
                start_probability[title[i] + title[i + 1]] = 1
            else: 
                start_probability[title[i] + title[i + 1]] += 1
            if i + 2 >= len(title) or title[i + 2] not in hanzi: continue
            if (title[i] + title[i + 1]) not in transition_probability:
                transition_probability[title[i] + title[i + 1]] = dict()
            if title[i + 2] not in transition_probability[title[i] + title[i + 1]]:
                transition_probability[title[i] + title[i + 1]][title[i + 2]] = 1
            else:
                transition_probability[title[i] + title[i + 1]][title[i + 2]] += 1
        for i in xrange(0, len(html)):
            if i + 1 >= len(html) or html[i] not in hanzi or html[i + 1] not in hanzi: continue
            if (html[i] + html[i + 1]) not in start_probability:
                start_probability[html[i] + html[i + 1]] = 1
            else:
                start_probability[html[i] + html[i + 1]] += 1
            if i + 2 >= len(html) or html[i + 2] not in hanzi: continue 
            if (html[i] + html[i + 1]) not in transition_probability:
                transition_probability[html[i] + html[i + 1]] = dict()
            if html[i + 2] not in transition_probability[html[i] + html[i + 1]]:
                transition_probability[html[i] + html[i + 1]][html[i + 2]] = 1
            else:
                transition_probability[html[i] + html[i + 1]][html[i + 2]] += 1
    print 'Process ' + file + ' ... OK'
    fin.close()

with open('start_probability_trigram.json', 'w') as fout:
    fout.write(json.dumps(start_probability))

with open('transition_probability_trigram.json', 'w') as fout:
    fout.write(json.dumps(transition_probability))

with open('num.txt', 'w') as fout:
    fout.write(str(num))

print 'Save Dictionary ... OK'


