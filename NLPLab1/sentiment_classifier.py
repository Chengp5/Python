######################################################
#TODO sentiment-classifier-file,several functions for other modules to call
#TODO functions about reading data, pre-processing data, training model , doing the prediction
#TODO functions about save and load vectorizer,save and load vectorizer,save prediction result
######################################################
import zipfile
from sklearn.utils import shuffle
from sklearn import model_selection
from sklearn.metrics import accuracy_score
import pickle

# six kinds of emotion labels
label_map={'anger':0,
           'fear':1,
           'joy':2,
           'love':3,
           'sadness':4,
           'surprise':5}
# mapping from emotion text to relevant emoji
emotion_emoji={
'anger':'😡',
'fear':'😱',
'joy':'😄',
'love':'😍',
'sadness':'😭',
'surprise':'😨',
}

#TODO read data from .txt files
def read_data(file_names):
    # zip .zip file directly
    files = zipfile.ZipFile('data.zip')
    # data for storing text and label
    data={'text':[],
          'label':[]}
    # read data from files(in this case ,we read train.txt for training and val.txt for testing)
    for file_name in file_names:
        file = files.open(file_name)
        temp_data=file.readlines()
        temp={'text':[],
          'label':[]}
        # for each file, read every line
        for line in temp_data:
            s = str(line, encoding='utf-8')
        # split sentence into text and label
            sps=s.split(';',1)
        # add to list
            temp['text'].append(sps[0])
            # remove '\n'
            temp['label'].append(sps[1].strip('\n'))
        # shuffle data for each file
        temp=shuffle(temp['text'],temp['label'])
        #concatenate data from each file
        data['text'].extend(temp[0])
        data['label'].extend(temp[1])
        #get texts and labels
    texts=data['text']
    labels=data['label']

    assert len(texts) == len(labels)

    return texts,labels
#TODO a simple read function for test_data.txt
def read_test_data(file_names):
    #zip .zip file
    files = zipfile.ZipFile('data.zip')
    #get texts
    data=[]
    # add each line to data list
    for file_name in file_names:
        file = files.open(file_name)
        temp_data = file.readlines()
        for line in temp_data:
            s = str(line, encoding='utf-8')
            data.append(s)
    return data

#TODO pre-process sentences
def pre_processing(data,labels):
    # use RegexpTokenizer for tokenization
    from nltk.tokenize import RegexpTokenizer
    # tokenizer to remove unwanted elements from out data like symbols and numbers
    token = RegexpTokenizer(r'[a-zA-Z0-9]+')

    #TfidfVectorizer
    #use TfidfVectorizer to generate tf-idf feature matrix
    from sklearn.feature_extraction.text import TfidfVectorizer
    # all characters are lowercase, use default english stop_words, uni-gram, use RegexpTokenizer
    cv=TfidfVectorizer(lowercase=True,stop_words='english',ngram_range = (1,1),tokenizer=token.tokenize)
    #get feature marix
    final_data=cv.fit_transform(data)
    # or
    # cv.fit()
    # cv.transform()
    # print(final_data.shape)
    # save this vectorizer
    save_vectorizer('TFIDFv',cv)


    Train_X, Test_X, Train_Y, Test_Y = model_selection.train_test_split(final_data, labels,shuffle=False,
                                                                test_size=2000)

    return Train_X, Test_X, Train_Y, Test_Y
#TODO a simple pre-process function using saved vectorizer
def pre_processing_new_data(data):
    # load vecotrizer
    cv=load_vectorizer()
    # get feature matrix
    final_data=cv.transform(data)
    print(final_data.shape)

    return final_data
#TODO SVM-Classifier
def SVMClassifier(Train_X, Test_X, Train_Y, Test_Y):
    from sklearn import svm
    # create a SVM classifier
    SVM = svm.SVC(C=1.0, kernel='linear', degree=3, gamma='auto')
    # use data to train this model
    SVM.fit(Train_X,Train_Y)
    # get prediction result
    prediction = SVM.predict(Test_X)
    # get accuracy
    accuracy = accuracy_score(prediction, Test_Y)
    # show accuracy
    print('SVM Accuracy Score -> {}%'.format(accuracy*100))

#TODO NaiveBayes-Classifier
def NaiveBayesClassifier(Train_X, Test_X, Train_Y, Test_Y):
    from sklearn.naive_bayes import MultinomialNB
    #create a NB classifier
    clf = MultinomialNB()
    #use data to train
    clf.fit(Train_X,Train_Y)
    #get prediction result
    prediction = clf.predict(Test_X)
    #calculate accuracy
    accuracy=accuracy_score(prediction, Test_Y)
    #show accuracy
    print("MultinomialNB Accuracy Score -> {}%".format((accuracy*100)))
#TODO save a classifier
def save_classifier(model_name,model):
    # save model at this path
    with open('./model/'+model_name+'.pkl', 'wb') as f:
        pickle.dump(model, f)
#TODO load a classifier
def load_clssifier(model_name='NBCLF'):
    try:
        # load classifier from this path
        with open('./model/'+model_name+'.pkl', 'rb') as f:
            clf = pickle.load(f)
            return clf
    except FileNotFoundError:
        return
#TODO save a vectorizer
def save_vectorizer(vectorizer_name,vectorizer):
    #save a vectorizer at this path
    with open('./vectorizer/'+vectorizer_name+'.pkl', 'wb') as f:
        pickle.dump(vectorizer, f)
#TODO load a vectorizer
def load_vectorizer(vectorizer_name='TFIDFv'):
    try:
        #load a vectorizer from this path
        with open('./vectorizer/'+vectorizer_name+'.pkl', 'rb') as f:
            vectorizer = pickle.load(f)
            return vectorizer
    except FileNotFoundError:
        return
#TODO use data to train model
def train_data(Train_X, Test_X, Train_Y, Test_Y,model_name='NBCLF'):
    # try to use old model, if don't have one, create a new model to train
    clf=load_clssifier(model_name)
    if clf:
        #if there is one old model , train this one
        clf.fit(Train_X,Train_Y)
    else:
        #if not create a NBclf or a SVMclf
        if model_name=='NBCLF':
            from sklearn.naive_bayes import MultinomialNB
            clf = MultinomialNB()
            #train model
            clf.fit(Train_X,Train_Y)
        elif model_name=='SVMCLF':
            from sklearn import svm
            clf = svm.SVC(C=1.0, kernel='linear', degree=3, gamma='auto')
            # train model
            clf.fit(Train_X, Train_Y)
        else:
            return
    #get prediction result
    prediction = clf.predict(Test_X)
    #calculate accuracy
    accuracy = accuracy_score(prediction, Test_Y)
    print(model_name+" Accuracy Score -> {}%".format((accuracy * 100)))
    from sklearn.metrics import classification_report
    #calculate and show precision, recall and F1-score
    print(classification_report(Test_Y, prediction, target_names=label_map,zero_division='warn'))
    # save this classifier
    save_classifier(model_name, clf)
#TODO predict a sentence
def predict_text(texts):
    #get feature matrix
    final_data=pre_processing_new_data(texts)
    #load a classifier
    clf=load_clssifier()
    #get prediction result
    prediction=clf.predict(final_data)
    #show result
    print(prediction)
    #return emoji and emotion to UI module
    return trans_to_emoji(prediction[0])
#TODO get emoji from emotion text(happy ->'😄')
def trans_to_emoji(emotion):
    return {'emotion':emotion,
            'emoji':emotion_emoji[emotion]}
#TODO save prediction result into a file
def save_result(results):
    # open file
    f = open('test_prediction.txt', 'w+')
    #write result into file
    for result in results:
        f.write(result)
        f.write('\n')
    read = f.readline()
    f.close()
    print(read)
# if __name__ == '__main__':
#     texts,labels=read_data(['data/train.txt','data/val.txt'])
#     Train_X, Test_X, Train_Y, Test_Y=pre_processing(texts,labels)
#     train_data(Train_X, Test_X, Train_Y, Test_Y,'NBCLF')
