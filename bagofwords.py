#!usr//bin/python3
import json
import re
import numpy as np
# import nltk
from nltk.corpus import stopwords # Import the stop word list
# print(stopwords.words("english"))
def convert_review_to_words(review_data):
    letters_only=re.sub("[^a-zA-Z]"," ",review_data)
    all_words=letters_only.lower().split()
    #Set is faster than list
    stop_words=set(stopwords.words("english"))
    useful_words=[w for w in all_words if w not in stop_words]
    return(" ".join(useful_words))


# json_data = open('Digital_Music_5_sub.json','r')
# data = json.load(json_data)
y=0
helpful=0
unhelpful=0
total=0
reviewCount=0
data = []
cleaned_data=[]
with open('Beauty_5.json','r') as f:
    for line in f:
        currentLine=json.loads(line)
        data.append(currentLine)
        # if(y<10):
        clean_data=convert_review_to_words(currentLine['reviewText'])
        cleaned_data.append(clean_data)
        
        if(y%10000==0):
            print(y)
            print(cleaned_data[y])
        y+=1
# print(cleaned_data[0])
print("Creating the bag of words...\n")
from sklearn.feature_extraction.text import CountVectorizer

# Initialize the "CountVectorizer" object, which is scikit-learn's
# bag of words tool.  
vectorizer = CountVectorizer(analyzer = "word",   \
                             tokenizer = None,    \
                             preprocessor = None, \
                             stop_words = None,   \
                             max_features = 300) 

# fit_transform() does two functions: First, it fits the model
# and learns the vocabulary; second, it transforms our training data
# into feature vectors. The input to fit_transform should be a list of 
# strings.
train_data_features = vectorizer.fit_transform(cleaned_data)

# Numpy arrays are easy to work with, so convert the result to an 
# array
train_data_features = train_data_features.toarray()
print(train_data_features.shape)
vocab = vectorizer.get_feature_names()
# print(vocabulary)
# Sum up the counts of each vocabulary word
dist = np.sum(train_data_features, axis=0)
zip(vocab, dist)
# For each, print the vocabulary word and the number of times it 
# appears in the training set
for tag, count in zip(vocab, dist):
    print(count, tag)

print("Sorted")
for tag, count in sorted(zip, key=zip.get, reverse=True):
    print(count, tag)


        # data.append(json.loads(line))
    	# if len(currentLine['reviewText'])<50:
    	# 	reviewCount+=1
    	# 	if currentLine['helpful'][0]==0 and currentLine['helpful'][1]==0:
    	# 		total+=1
    	# 	if currentLine['helpful'][0]>0:
    	# 		helpful+=1
    	# 	if currentLine['helpful'][1]>0:
    	# 		unhelpful+=1
    	# reviewCount+=1
    	# if currentLine['helpful'][0]==0 and currentLine['helpful'][1]==0:
    	# 	total+=1
    	# if currentLine['helpful'][0]>0:
    	# 	helpful+=1
    	# if currentLine['helpful'][1]>0:
    	# 	unhelpful+=1
# print(data[0])
# print(len(data))
# sampleData=data[41]["reviewText"]
# letterOnly=re.sub("[^a-zA-Z]"," ",sampleData)
# allWords=letterOnly.lower().split()
# print(allWords)
# myList=[]
# x1 = 0
# for w in allWords:
#     if(w not in stopwords.words("english")):
#         myList.append(w)
# print(myList)
# print("......................")
# print(allWords)


# json_data.close()

# x=0
# for x in range(0, 2):
# 	row=data[x]
# 	# print(type(row))
# 	print(row['reviewTime'])
# 	print(len(row['reviewText']))
# 	x+=1



