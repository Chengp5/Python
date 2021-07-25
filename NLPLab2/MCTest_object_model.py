# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/4/10 18:47
# @Author  : chengp
# @File    : object_model.py
# @Funtionality




""" classes for creating passage instances
one passage contains one story represented by sents(a list of sentences) and four questions(Question class)
and a bag of words of this passage
one question contains four options(answer class) and one correct answer"""
import nltk

class Text(object):

    def __init__(self, text):
        self.text = text
        self.words = self.counting()
        self.sents = nltk.sent_tokenize(text)

    def counting(self):

        l = self.text.split()

        counts = {}

        for word in l:

            if word not in counts.keys():
                counts[word] = 1
            else:
                counts[word] += 1

        return counts


class Passage(Text):

    def __init__(self, title, story, questions):
        Text.__init__(self, story)
        self.title = title
        self.questions = questions

    def display(self):
        print(self.title + '\n')
        print(self.text + '\n\n***\n')
        for q in self.questions:
            print
            '\n' + q.text + ' (' + q.qtype + ')'
            for a in q.answers:
                print
                '\t' + a.text
            print
            '\n\tCorrect Answer: ' + q.correct_answer.text


class Question(Text):

    def __init__(self, qtext, qtype, answers, correct_answer):
        Text.__init__(self, qtext)
        self.qtype = qtype
        self.answers = answers
        self.correct_answer = correct_answer


class Answer(Text):

    def __init__(self, atext):
        Text.__init__(self, atext)