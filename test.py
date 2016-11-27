from gensim import utils
from gensim.models.doc2vec import LabeledSentence
from gensim.models import Doc2Vec
from string import punctuation

import json
import numpy
from random import shuffle
import os
import numpy as np

all_revs = open('All_Rev.txt','w')
neg_revs = open('Negative_Rev.txt','w')
pos_revs = open('Positive_Rev.txt','w')
with open('Beauty_5.json','r') as f:
	for line in f:
		currentLine=json.loads(line)
#		if(currentLine['overall']<4):
		statement_lower = currentLine['summary'].lower()
		for p in list(punctuation):
			statement_lower = statement_lower.replace(p,'')			
#			neg_revs.write(statement_lower)
#			neg_revs.write("\n")
#		else:
#			statement_lower = currentLine['summary'].lower()
#			for p in list(punctuation):
#				statement_lower = statement_lower.replace(p,'')
#			pos_revs.write(statement_lower)
#			pos_revs.write("\n")
		all_revs.write(statement_lower)
		all_revs.write("\n")
#neg_revs.close()
#pos_revs.close()
all_revs.close()
class LabeledLineSentence(object):

    def __init__(self, sources):
        self.sources = sources

        flipped = {}

        # make sure that keys are unique
        for key, value in sources.items():
            if value not in flipped:
                flipped[value] = [key]
            else:
                raise Exception('Non-unique prefix encountered')

    def __iter__(self):
        for source, prefix in self.sources.items():
            with utils.smart_open(source) as fin:
                for item_no, line in enumerate(fin):
                    yield LabeledSentence(utils.to_unicode(line).split(), [prefix + '_%s' % item_no])

    def to_array(self):
        self.sentences = []
        for source, prefix in self.sources.items():
            with utils.smart_open(source) as fin:
                for item_no, line in enumerate(fin):
                    self.sentences.append(LabeledSentence(
                        utils.to_unicode(line).split(), [prefix + '_%s' % item_no]))
        return self.sentences

    def sentences_perm(self):
        shuffle(self.sentences)
        return self.sentences
#sources = {'Negative_Rev.txt':'NEG', 'Positive_Rev.txt':'POS'}
sources = {'All_Rev.txt':'ALL'}
sentences = LabeledLineSentence(sources)
def labelize(reviews, label_type):
	labelized = []
	for i,v in enumerate(reviews):
		label = '%s_%s'%(label_type,i)
		labelized.append(LabeledSentence(v, [label]))
	return labelized

#all = labelize('Negative_Rev.txt', 'TRAIN')
model = Doc2Vec(min_count = 1, window = 10, size = 300, workers = 10)
model.build_vocab(sentences.to_array())

for epoch in range(10):
#	perm = np.random.permutation(all)
	model.train(sentences.sentences_perm())

def getVecs(model, corpus, size):
	vecs = [np.array(model[z.labels[0]]).reshape((1, size)) for z in corpus]
	return np.concatenate(vecs)

#all_vecs_dm = getVecs(model, all, 100)

model.save('./testResult.d2v')
model = Doc2Vec.load('./testResult.d2v')
hello = model.syn0
#print(all_vecs_dm)
print(hello)
