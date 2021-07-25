# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/4/10 18:48
# @Author  : chengp
# @File    : MCTest_QA_system.py
# @Funtionality

"""
QA_system for MCTest dataset
main() here
"""




from MCTest_DataLoader import *
from MCTest_scorer import *
from MCTest_sentence_similarity import SentenceSimilarity



# answers a queston using an answer scorer
def get_best_answer(context, bow, question, answers):
    # create question-answer pair
    q_a_pair=question+' '+answers[0].text
    q_a_pair=q_a_pair.lower().split(' ')
    # assume answer A is best answer
    best_score = scorer(context,bow,q_a_pair)
    best_answer = answers[0]
    # score every answer
    for answer in answers[1:]:
        q_a_pair = question+' '+answer.text
        q_a_pair = q_a_pair.lower().split(' ')
        score = scorer(context,bow,q_a_pair)
        if score > best_score:
            best_answer = answer
            best_score = score
    #return best answer
    return best_answer



# answer all questions
def answerQuestions(passages):
    choosed_answers=[]
    for i,p in enumerate(passages):
        #  initialize sentence similarity model
        model=SentenceSimilarity('\\n')
        model.set_sentences(p.sents)
        # choose TfidfModel
        # sometimes LdaModel crashes
        model.TfidfModel()

        # answer every question
        for q in p.questions:
            answers=q.answers
            # get top k sentences related to question
            result, _ = model.similarity_k(q.text,8)
            # create context for these sentence
            context=[]
            for r in result:
                sent=p.sents[r]
                sent=sent.split(' ')
                for w in sent:
                    context.append(w)
            # try to get best answer based on context, question, options
            best_answer=get_best_answer(context, p.words,q.text,answers)
            choosed_answers.append(best_answer)
    return choosed_answers


# evaluate answers for this training or testing
def evaluate_answers(choosed_answers, passages):
    # number of question type multiple
    multiple=0
    # number of correct answered question type multiple
    multiple_correct=0
    # number of correct answered question type one
    one_correct=0
    # number of question type one
    one=0
    for i,answer in enumerate(choosed_answers):
        index=int(i/4)
        question=passages[index].questions[i % 4]
        answer=choosed_answers[i]
        if question.qtype=='one':
            if answer.text==question.correct_answer.text:
                one_correct+=1
            one+=1
        elif  question.qtype=='multiple':
            if answer.text==question.correct_answer.text:
                multiple_correct+=1;
            multiple+=1
    # question type one accurate rate
    one_correct_rate=one_correct/one
    # question type multiple accurate rate
    multiple_correct_rate=multiple_correct/multiple
    # total accurate rate
    correct_rate=(one_correct+multiple_correct)/(one+multiple)
    # print result
    print('one_correct_rate:',one_correct_rate,'\n'
          ,'multiple_correct_rate:',multiple_correct_rate,'\n'
          ,'total_correct_rate:',correct_rate,'\n')



def main():
    # prepare passages (change path here)
    passages = processData('data\\mc500.train')
    # answer all questions
    choosed_answers=answerQuestions(passages)
    # evaluate result
    evaluate_answers(choosed_answers,passages)

if __name__ == '__main__':
    main()