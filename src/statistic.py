#coding=utf-8

import sys
import os
if len(sys.argv) != 3: 
    print "Please input 2 files."
    exit(1)
f0 = open(sys.argv[1], 'r')
f1 = open(sys.argv[2], 'r')

sen_corr = 0
word_corr = 0
sen_all = 0
word_all = 0

for line0 in f0:
    line0 = line0.strip().decode('utf-8')
    line1 = f1.readline().strip().decode('utf-8')
    sen_all += 1
    word_all += len(line0)
    corr = 0
    for i in xrange(0, len(line0)):
        print line0[i], line1[i]
        if line0[i] == line1[i]:
            corr += 1
    word_corr += corr
    if corr == len(line0):
        sen_corr += 1

print 'sentence correct = ' + str(1.0 * sen_corr / sen_all)
print 'word correct = ' + str(1.0 * word_corr / word_all)
