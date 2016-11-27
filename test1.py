import gensim
from gensim import utils
from gensim.models.doc2vec import LabeledSentence
from gensim.models import Doc2Vec
from string import punctuation

import json
import numpy
import random
import os
import numpy as np

from sklearn.cross_validation import train_test_split

# neg_revs = open('Negative_Rev_FullText.txt','w')
# pos_revs = open('Positive_Rev_FullText.txt','w')
# with open('Beauty_5.json','r') as f:
# 	for line in f:
# 		currentLine=json.loads(line)
# 		if currentLine['helpful'][0]>0 and currentLine['helpful'][1]-currentLine['helpful'][0]<currentLine['helpful'][0]:
# 			if(currentLine['overall']<4):
# 				statement_lower = currentLine['reviewText'].lower()
# 				neg_revs.write(statement_lower)
# 				neg_revs.write("\n")
# 			else:
# 				statement_lower = currentLine['reviewText'].lower()
# 				pos_revs.write(statement_lower)
# 				pos_revs.write("\n")
# neg_revs.close()
# pos_revs.close()




with open('./Positive_Rev_FullText.txt','r') as infile:
    pos_reviews = infile.readlines()

with open('./Negative_Rev_FullText.txt','r') as infile:
    neg_reviews = infile.readlines()


#use 1 for positive sentiment, 0 for negative
y = np.concatenate((np.ones(len(pos_reviews)), np.zeros(len(neg_reviews))))

x_train, x_test, y_train, y_test = train_test_split(np.concatenate((pos_reviews, neg_reviews)), y, test_size=0.2)

#Do some very minor text preprocessing
def cleanText(corpus):
    punctuation = """.,?!:;(){}[]"""
    corpus = [z.lower().replace('\n','') for z in corpus]
    corpus = [z.replace('<br />', ' ') for z in corpus]

    #treat punctuation as individual words
    for c in punctuation:
        corpus = [z.replace(c, ' %s '%c) for z in corpus]
    corpus = [z.split() for z in corpus]
    return corpus

x_train = cleanText(x_train)
x_test = cleanText(x_test)

#Gensim's Doc2Vec implementation requires each document/paragraph to have a label associated with it.
#We do this by using the LabeledSentence method. The format will be "TRAIN_i" or "TEST_i" where "i" is
#a dummy index of the review.
def labelizeReviews(reviews, label_type):
    labelized = []
    for i,v in enumerate(reviews):
        label = '%s_%s'%(label_type,i)
        labelized.append(LabeledSentence(v, [label]))
    return labelized

x_train = labelizeReviews(x_train, 'TRAIN')
x_test = labelizeReviews(x_test, 'TEST')





print("dataset created")





















size = 100

#instantiate our DM and DBOW models
model_dm = gensim.models.Doc2Vec(min_count=1, window=10, size=size, sample=1e-3, negative=5, workers=8)
model_dbow = gensim.models.Doc2Vec(min_count=1, window=10, size=size, sample=1e-3, negative=5, dm=0, workers=8)

#build vocab over all reviews
model_dm.build_vocab(np.concatenate((x_train, x_test)))
model_dbow.build_vocab(np.concatenate((x_train, x_test)))

print("model training with train reviews started...")

#We pass through the data set multiple times, shuffling the training reviews each time to improve accuracy.
all_train_reviews = np.concatenate((x_train,[]))
for epoch in range(10):
    perm = np.random.permutation(all_train_reviews.shape[0])
    model_dm.train(all_train_reviews[perm])
    model_dbow.train(all_train_reviews[perm])

print("getting training vectors...")

#Get training set vectors from our models
def getVecs(model, corpus, size):
    vecs = [np.array(model[z.labels[0]]).reshape((1, size)) for z in corpus]
    return np.concatenate(vecs)

train_vecs_dm = getVecs(model_dm, x_train, size)
train_vecs_dbow = getVecs(model_dbow, x_train, size)

train_vecs = np.hstack((train_vecs_dm, train_vecs_dbow))



print("model training with test reviews started...")

#train over test set
x_test = np.array(x_test)
for epoch in range(10):
    perm = np.random.permutation(x_test.shape[0])
    model_dm.train(x_test[perm])
    model_dbow.train(x_test[perm])

print("getting testing vectors")

#Construct vectors for test reviews
test_vecs_dm = getVecs(model_dm, x_test, size)
test_vecs_dbow = getVecs(model_dbow, x_test, size)

test_vecs = np.hstack((test_vecs_dm, test_vecs_dbow))

print(test_vecs)
model_dm.save('./model_dm.d2v')
model_dbow.save('./model_dbow.d2v')


print("Applying SGD classifier")

from sklearn.linear_model import SGDClassifier

lr = SGDClassifier(loss='log', penalty='l1')
lr.fit(train_vecs, y_train)

print('Test Accuracy: %.2f'%lr.score(test_vecs, y_test))