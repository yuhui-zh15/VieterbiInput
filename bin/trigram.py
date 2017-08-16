#coding=utf-8

# Author: Zhang Yuhui
# E-mail: yuhui-zh15@mails.tsinghua.edu.cn
# Date: 20170408

import sys
import os
import json
import math

# Viterbi Algorithm
def viterbi(obs, pin, start_p_bi, trans_p_bi, start_p_tri, trans_p_tri, emit_p, lamda):
    V = [{}]
    path = {}

    # Initialize Base Cases (t == 0)
    s = 0
    for y in start_p_bi: s += start_p_bi[y]
    for y in pin[obs[0]]:
        if obs[0] not in emit_p[y]:
            V[0][y] = 0.0
        else:
            V[0][y] = 1.0 * start_p_bi[y] * emit_p[y][obs[0]] / s 
        path[y] = [y]

    # Initialize Base Cases (t == 1)
    if len(obs) > 1:
        V.append({})
        newpath = {}
        for y in pin[obs[1]]:
            prob = 0.0
            state = str()
            for y0 in pin[obs[0]]:
                if start_p_bi[y0] == 0 or y not in trans_p_bi[y0] or obs[1] not in emit_p[y]:
                    prob_tmp = 0.0
                else:
                    prob_tmp = 1.0 * V[0][y0] * trans_p_bi[y0][y] * emit_p[y][obs[1]] / start_p_bi[y0]
                V[1][y0 + y] = prob_tmp
                if prob_tmp >= prob:
                    prob = prob_tmp
                    state = y0
            V[1][y] = prob
            if state in path:
                newpath[y] = path[state] + [y]
        path = newpath

    # Run Viterbi for t > 1
    for t in range(2, len(obs)):
        V.append({})
        newpath = {}
        for y in pin[obs[t]]:
            prob = 0.0
            state = str()
            for y0 in pin[obs[t - 1]]:
                #Trigram
                prob_tri_tmp = 0.0
                for y00 in pin[obs[t - 2]]:
                    if (y00 + y0) not in start_p_tri or (y00 + y0) not in trans_p_tri or y not in trans_p_tri[y00 + y0] or obs[t] not in emit_p[y]:
                        prob_tri_tmp_tmp = 0.0
                    else:
                        prob_tri_tmp_tmp = 1.0 * V[t - 1][y00 + y0] * trans_p_tri[y00 + y0][y] * emit_p[y][obs[t]] / start_p_tri[y00 + y0] 
                    if prob_tri_tmp_tmp >= prob_tri_tmp:
                        prob_tri_tmp = prob_tri_tmp_tmp
                #Bigram
                prob_bi_tmp = 0.0
                if start_p_bi[y0] == 0 or y not in trans_p_bi[y0] or obs[t] not in emit_p[y]:
                    prob_bi_tmp = 0.0
                else:
                    prob_bi_tmp = 1.0 * V[t - 1][y0] * trans_p_bi[y0][y] * emit_p[y][obs[t]] / start_p_bi[y0]
                #Add Weight To Smooth The Probability
                prob_tmp = lamda * prob_tri_tmp + (1.0 - lamda) * prob_bi_tmp   
                V[t][y0 + y] = prob_tmp
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
        prob_tmp = 0.0
        if len(obs) < 2: 
            prob_tmp = V[len(obs) - 1][y]
        else:
            for y0 in pin[obs[len(obs) - 2]]:
                if (y0 + y) not in V[len(obs) - 1]:
                    prob_tmp_tmp = 0.0
                else:
                    prob_tmp_tmp = V[len(obs) - 1][y0 + y]
                if prob_tmp_tmp >= prob_tmp:
                    prob_tmp = prob_tmp_tmp
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
        start_probability_bigram = json.load(fin)
    with open('./lib/transition_probability.json', 'r') as fin:
        transition_probability_bigram = json.load(fin)
    with open('./lib/start_probability_trigram.json') as fin:
        start_probability_trigram = json.load(fin)
    with open('./lib/transition_probability_trigram.json') as fin:
        transition_probability_trigram = json.load(fin)
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
        (prob, path) = viterbi(observations, pinyin, start_probability_bigram, transition_probability_bigram, start_probability_trigram, transition_probability_trigram, emission_probability, 0.9)
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