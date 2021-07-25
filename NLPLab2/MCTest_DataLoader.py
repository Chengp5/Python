# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/4/10 11:15
# @Author  : chengp
# @File    : DataLoader.py
# @Funtionality
"""load and process data here """




import  re
from MCTest_object_model import *

# read training data or testing data from file
def readData(path):

    # passages and correct answer file names
    passages_file = path + '.tsv'
    answers_file = path + '.ans'

    # read passages
    f = open(passages_file)
    passages = f.read()
    f.close()

    # read correct answers
    f = open(answers_file)
    correct_answers = f.read()
    f.close()

    return passages, correct_answers

# read stop words from file
def readStopWords(path):

    stop_words_file = path + '.txt'

    # read passages
    f = open(stop_words_file)
    stop_words = f.read()
    f.close()
    return stop_words

# mapping option to index
# converts answers from characters to integers
# so they can be used as indices into the answer set
def letterToDigit(answer_index):
    if answer_index=='' :
        return
    answer_dict = {'A':0,'B':1,'C':2,'D':3}
    return answer_dict[answer_index]


# remove punctuation
punctuation = '!,;:?"\'、，；.'
def remove_punctuation(text):
    text = re.sub(r'[{}]+'.format(punctuation), ' ', text)
    return text.strip()

#remover question_words
question_words=set(['what','which','how','who','where','why'])
def remove_question_word(text):
    word_tokens = nltk.word_tokenize(text)
    filtered_sentence = []
    for word in word_tokens:
        if word.lower() not in question_words:
            filtered_sentence.append(word)
    filtered_sentence=' '.join(filtered_sentence)
    return filtered_sentence


#remove stop words
def remove_stopwords(stop_words, sent):
    word_tokens =nltk.word_tokenize(sent)
    filtered_sentence=[]
    for word in word_tokens:
        if word not in stop_words:
            filtered_sentence.append(word)
    return filtered_sentence




def processData(path):
    # read passages and answers
    passages_from_file, correct_answers_from_file = readData(path)

    # read stop words and create a set for it
    stop_words=readStopWords('data\\stopwords')
    stop_words=stop_words.split('\n');
    stop_words=set(stop_words)

    # correct answers
    correct_answers=correct_answers_from_file.split('\n')
    del correct_answers[len(correct_answers)-1]
    for i in range(len(correct_answers)):
        correct_answers[i]=correct_answers[i].split('\t')
        for j in range(len(correct_answers[i])):
            correct_answers[i][j]=letterToDigit(correct_answers[i][j])



    # parse passages
    data = []


    #split passages
    passages = passages_from_file.split('\n')
    del passages[len(passages) - 1]
    for i in range(len(passages)):
        passages[i] = passages[i].split('\t')



    for (i,passage) in enumerate(passages):
        # get passage title
        title=passage[0]
        # get story, replace escaped newlines and tabs, transform upper case letters to lower case
        story = passage[2]
        story = re.sub(r'\\newline','\n',story)
        story = re.sub(r'\\tab','\t',story)
        story = story.lower()
        questions = []
        for j in range(4):
            # get question and four answers
            question_elements = passage[3+j*5:3+j*5+5]
            # get question type and text
            question_type, question_text = question_elements[0].split(': ')
            # process question
            question_text =question_text.lower()
            question_text =remove_punctuation(question_text)
            question_text =remove_question_word(question_text)
            # get answers
            answers = [Answer(text) for text in question_elements[1:5]]
            # get correct answer from correct answer data
            correct_answer = answers[correct_answers[i][j]]
            # define question
            question = Question(question_text,question_type,answers,correct_answer)
            questions[j:] = [question]

        # define passage
        p =Passage(title,story,questions)
        new_sents=[]
        for sent in p.sents:
            sent=remove_punctuation(sent)
            new_sents.append(sent)
        p.sents=new_sents
        data[i:] = [p]

    return data
