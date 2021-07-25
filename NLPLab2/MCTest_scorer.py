# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/4/13 14:55
# @Author  : chengp
# @File    : MCTest_scorer.py
# @Funtionality

""" scorer for each option"""


import math

# calculate score
def score(word, bow):
    if word not in bow:
        return 0
    final_score = math.log2(1 + (1 / bow[word]))
    return final_score

def scorer(context, bow, q_a_pair):

    # Set size of window
    size = len(q_a_pair)

    # Make a set for q_a_pair
    qaSet = set(q_a_pair)

    # Score of the window with the max score
    maxPoint = 0

    # Traverse story window size at a time
    for i in range(len(context) - size):

        # Make a sliding window
        window = context[i: i + size]

        # Score for this window
        point = 0

        # Traverse set and look for matches
        for word in qaSet:

            # If match, add to score
            if word in window:
                point += score(word,bow)

        # Adjust max score if its greater
        if point > maxPoint:
            maxPoint = point

    return maxPoint

