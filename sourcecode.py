import csv
import xlrd
import subprocess
import random
import string
import sys
import os
import time
from sklearn.metrics import classification_report
from nltk.corpus import stopwords
import nltk, re, pprint
from nltk import word_tokenize
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn.metrics import accuracy_score
from nltk.classify import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB
from __future__ import print_function
from collections import defaultdict
from nltk.metrics import *
from nltk.corpus import stopwords
from nltk.classify import SklearnClassifier, NaiveBayesClassifier
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn import tree

workbook = xlrd.open_workbook('try_set1234.xlsx')
worksheet = workbook.sheet_by_index(0)
stop_words = set(stopwords.words('english'))

documents = []
every_word = []
for row in range (0, 2000):
    a = worksheet.cell(row, 0).value #getting one tweet
    a_widout_url = re.sub(r'http\S+', "", a)#removes URL->S any non-white space character
    a_wid_alpha = re.sub('[^A-Za-z0-9]+'," ", a_widout_url)#removing special characters 
    tokenized_words = word_tokenize(a_wid_alpha) #tokenizing each tweet
    b = [w for w in tokenized_words if not w in stop_words]#removing stopwords
    
    c = worksheet.cell(row, 1).value #storing label of tweets
    
    every_word += b #storing every tokenized word in this list   
    
    documents.append((b,c)) # creating tweet->label

random.shuffle(documents)


#getting most frequent words from our data set
allwords = nltk.FreqDist(w.lower() for w in every_word)
frequent_words = list(allwords)[:2000] #No labels here Just words from all tweet set


#function for feature extraction
def feature_extractor(provided_doc):
    realtime_doc_words = set(provided_doc)
    features = {}
    for w in frequent_words:
        features['contain({})'.format(w)]= (w in realtime_doc_words)
    return features
#--------------------------------Naive Bayes------------------------------------
#train the classifier(Naive Bayes Classifier)
featuresets = [(feature_extractor(d), c) for (d,c) in documents]
training_set = featuresets [:1900]
classifier = nltk.NaiveBayesClassifier.train(training_set)

testing_set= featuresets[1900:]
#testing accuracy
print("Naive Bayes Classifiers' Accuracy ", nltk.classify.accuracy(classifier, testing_set))
classifier.show_most_informative_features(5)

refset = collections.defaultdict(set)
testsets12 = collections.defaultdict(set)

for i, (feats, label) in enumerate(testing_set):
    #print(i, feats, label)
    refset[label].add(i)
    observed = classifier.classify(feats)
    testsets12[observed].add(i)

print("Leave Evaluation-- ")
print("Precison Of leave ", precision(refset['leave'], testsets12['leave']))
print("Recall of leave ", recall(refset['leave'], testsets12['leave']))
print("F-measure ", f_measure(refset['leave'], testsets12['leave']))

print("Stay Evaluation-- ")
print("Precision ", precision(refset['stay'], testsets12['stay']))
print("Recall ", recall(refset['stay'], testsets12['stay']))
print("f-measure", f_measure(refset['stay'], testsets12['stay']))

print("No Sentiment/Don't care Evaluation-- ")
print("Precision ", precision(refset['no sentiment/don\'t care'], testsets12['no sentiment/don\'t care']))
print("Recall ", recall(refset['no sentiment/don\'t care'], testsets12['no sentiment/don\'t care']))
print("F- measure ", f_measure(refset['no sentiment/don\'t care'], testsets12['no sentiment/don\'t care']))

print("Undecided Evaluation-- ")
print("Precision ", precision(refset['undecided'], testsets12['undecided']))
print("Recall ", recall(refset['undecided'], testsets12['undecided']))
print("F-measure", f_measure(refset['undecided'], testsets12['undecided']))

print("Irrelevant Evaluation-- ")
print("Precision ", precision(refset['irrelevant'], testsets12['irrelevant']))
print("Recall ", recall(refset['irrelevant'], testsets12['irrelevant']))
print("F-measure ", f_measure(refset['irrelevant'], testsets12['irrelevant']))

classif_multinom = SklearnClassifier(MultinomialNB()).train(training_set)
print("MultinomialNB Accuracy ", nltk.classify.accuracy(classif_multinom, testing_set))



#-----------------------------------------------DECISION TREE-------------------------------------------
print("--------DEcision Tree---------")


decTree_classifier = nltk.DecisionTreeClassifier.train(training_set)

print("Leaf node of the test set Decision Tree->>",decTree_classifier.leaf(testing_set))

print("Decision Tree Classifier Accuracy ", nltk.classify.accuracy(decTree_classifier, testing_set))
print("Pseudocode ", decTree_classifier.pseudocode(depth=6))


refset_dec = collections.defaultdict(set)#same as dict but in this we can override a method
testsets12_dec = collections.defaultdict(set)

for i, (feats, label) in enumerate(testing_set):
    #print(i, feats, label)
    refset_dec[label].add(i)#adding labels of test datset to refset dict
    observed = decTree_classifier.classify(feats)#classifying each test tweet
    testsets12_dec[observed].add(i)#stores classified tweet's label

print("Stay Evaluation-- ")
print("Precision ", precision(refset_dec['stay'], testsets12_dec['stay']))
print("Recall ", recall(refset_dec['stay'], testsets12_dec['stay']))
print("f-measure", f_measure(refset_dec['stay'], testsets12_dec['stay']))

print("Leave Evaluation-- ")
print("Precison Of leave ", precision(refset_dec['leave'], testsets12_dec['leave']))
print("Recall of leave ", recall(refset_dec['leave'], testsets12_dec['leave']))
print("F-measure ", f_measure(refset_dec['leave'], testsets12_dec['leave']))

print("No Sentiment/Don't care Evaluation-- ")
print("Precision ", precision(refset_dec['no sentiment/don\'t care'], testsets12_dec['no sentiment/don\'t care']))
print("Recall ", recall(refset_dec['no sentiment/don\'t care'], testsets12_dec['no sentiment/don\'t care']))
print("F- measure ", f_measure(refset_dec['no sentiment/don\'t care'], testsets12_dec['no sentiment/don\'t care']))

print("Undecided Evaluation-- ")
print("Precision ", precision(refset_dec['undecided'], testsets12_dec['undecided']))
print("Recall ", recall(refset_dec['undecided'], testsets12_dec['undecided']))
print("F-measure", f_measure(refset_dec['undecided'], testsets12_dec['undecided']))

print("Irrelevant Evaluation-- ")
print("Precision ", precision(refset_dec['irrelevant'], testsets12_dec['irrelevant']))
print("Recall ", recall(refset_dec['irrelevant'], testsets12_dec['irrelevant']))
print("F-measure ", f_measure(refset_dec['irrelevant'], testsets12_dec['irrelevant']))


#---------------------------------------------------------SVM------------------------------------------


print("------------------SVM-------------------")
train_data2=[]
train_labels2 = []
test_data2= [] 
test_labels2 = []
documents_thrd = []

#
for row in range (0, 2000):
    a = worksheet.cell(row, 0).value #getting one tweet
    a_widout_url = re.sub(r'http\S+', "", a)#removes URL
    a_wid_alpha = re.sub('[^A-Za-z0-9]+'," ", a_widout_url)#removing special characters 
    b111 = ''.join(a_wid_alpha)
    
    c = worksheet.cell(row, 1).value #getting label of tweet
    e111 = ''.join(c) 
    
    documents_thrd.append((b111,e111)) #tweet->label
#
random.shuffle(documents_thrd)

for row1 in range(0,1900):
    train_data2.append(documents_thrd[row1][0])
    train_labels2.append(documents_thrd[row1][1])

for row2 in range(1900,2000):
    test_data2.append(documents_thrd[row2][0])
    test_labels2.append(documents_thrd[row2][1])

#min_df if a word has occurence less than this then avoid it
vectorizer = TfidfVectorizer(min_df = 2,max_df = 1.0, sublinear_tf = True, use_idf = True)

#fit=creating a vocab of features && transform=creates feature weights
train_vectors = vectorizer.fit_transform(train_data2)

test_vectors = vectorizer.transform(test_data2)#creates feature weights for test data && vocab is same as of trainers

classifierSVM_linear = svm.SVC(C = 1.0, kernel='linear')
classifierSVM_linear.fit(train_vectors, train_labels2)#this does the training of the training set

prediction_linear = classifierSVM_linear.predict(test_vectors)#this predicts for the testing set

print("Results for SVC(kernel=linear)")
print(classification_report(test_labels2, prediction_linear))

print ("SVM Accuracy ", accuracy_score(test_labels2, prediction_linear))
