from gensim import utils
from gensim.models.doc2vec import LabeledSentence
from gensim.models import Doc2Vec
from string import punctuation

import json
import numpy
from random import shuffle
import os

neg_revs = open('Negative_Rev.txt','w')
pos_revs = open('Positve_Rev.txt','w')

with open('Beauty_5.json','r') as f:
	for line in f:
		currentLine=json.loads(line)
		if(currentLine['overall']<4):
			statement_lower = currentLine['summary'].lower()
			for p in list(punctuation):
				statement_lower = statement_lower.replace(p,'')			
			neg_revs.write(statement_lower)
			neg_revs.write("\n")
		else(currentLine['overall']>3):
			statement_lower = currentLine['summary'].lower()
			for p in list(punctuation):
				statement_lower = statement_lower.replace(p,'')
			pos_revs.write(statemen_lower)
			pos_revs.write("\n")
neg_revs.close()
pos_revs.close()

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
sources = {'test_data.txt':'TEST'}
sentences = LabeledLineSentence(sources)
model = Doc2Vec(min_count = 1, window = 10, size = 100, sample = 1e-4, negative = 5, workers = 7)
model.build_vocab(sentences.to_array())

for epoch in range(50):
	model.train(sentences.sentences_perm())

model.save('./testResult.d2v')
model = Doc2Vec.load('./testResult.d2v')
hello = model.syn0
hello.save('./testVecs.vec')
print(hello)

