#coding=utf-8

# Author: Zhang Yuhui
# E-mail: yuhui-zh15@mails.tsinghua.edu.cn
# Date: 20170326

import sys
import os
import json
import math

# Viterbi Algorithm
def viterbi(obs, pin, start_p, trans_p, emit_p):
    V = [{}]
    path = {}

    # Initialize Base Cases (t == 0)
    s = 0
    for y in start_p: s += start_p[y]
    for y in pin[obs[0]]:
        if obs[0] not in emit_p[y]:
            V[0][y] = 0.0
        else:
            V[0][y] = 1.0 * start_p[y] * emit_p[y][obs[0]] / s 
        path[y] = [y]

    # Run Viterbi for t > 0
    for t in range(1, len(obs)):
        V.append({})
        newpath = {}
        s = {}
        # print json.dumps(s, ensure_ascii=False, indent=2)
        for y in pin[obs[t]]:
            prob = 0.0
            state = str()
            for y0 in pin[obs[t - 1]]:
                if start_p[y0] == 0 or y not in trans_p[y0] or obs[t] not in emit_p[y]: 
                    prob_tmp = 0.0
                else:
                    prob_tmp = 1.0 * V[t - 1][y0] * trans_p[y0][y] * emit_p[y][obs[t]] / start_p[y0] 
                if prob_tmp >= prob:
                    prob = prob_tmp
                    state = y0
            V[t][y] = prob
            if state in path:
                newpath[y] = path[state] + [y]
        path = newpath

    # Return Result
    prob = 0.0
    state = str()
    for y in pin[obs[len(obs) - 1]]:
        if y not in V[len(obs) - 1]:
            prob_tmp = 0.0
        else:
            prob_tmp = V[len(obs) - 1][y]
        if prob_tmp >= prob:
            prob = prob_tmp
            state = y

    if state in path:
        return (prob, path[state])

def main():
    if len(sys.argv) != 3:
        print 'Please input 2 arguments represent inputfile and outputfile name'
        exit(-1)
    # Load Dictionary
    print 'Load Dictionary ...' 
    with open('./lib/start_probability.json', 'r') as fin:
        start_probability = json.load(fin)
    with open('./lib/transition_probability.json', 'r') as fin:
        transition_probability = json.load(fin)
    with open('./lib/emission_probability.json', 'r') as fin:
        emission_probability = json.load(fin)
    with open('./lib/pinyin.json', 'r') as fin:
        pinyin = json.load(fin)
    print 'Load Dictionary ... OK'
    # Process File
    print 'Process ...'
    fin = open(sys.argv[1], 'r')
    fout = open(sys.argv[2], 'w')
    for line in fin:
        observations = line.strip().split(' ')
        (prob, path) = viterbi(observations, pinyin, start_probability, transition_probability, emission_probability)
        if path == None: continue
        output = str()
        for item in path:
            output += item
        output += '\n'
        fout.write(output.encode('utf-8'))
    fin.close()
    fout.close()
    print 'Process ... OK'

if __name__ == "__main__":
    main()