#!usr/bin/python3
import json
import re
import numpy as np
import pprint;
#import nltk
from nltk.corpus import stopwords # Import the stop word list
from nltk import word_tokenize, pos_tag
from collections import Counter
sentence = "I tried to take dyed hair from a natural color to white/platinum blonde with Slpat bleach. Then I wanted to add their purple for a streak in the front.. My goodness what a horrible experience. Their stuff hurt and one application left my hair so fried I thought it'd fall out!! Their purple was not purple and bled even after careful dying. The bleach just ruined my hair, it was this horrible mush. I hated it but bleached the purple out, oh my poor hair.Now I have bleached before with the blue tub of bleach by l'oreal. That stuff was awesome, still dried out my hair but not as bad as Splat!Anyway this Platinum was a little weird as it expanded and erupted out of the bottle but I just needed my roots done. I was terrified because I'd been using Everto every super duper conditioner I could find but my hair was a mess. Wow it actually made my hair feel stronger! I don't understand how but it repaired my hair! My roots are not platinum but after one shot of this stuff they are a very light golden blonde. NOTHING will in one shot take a medium brown hair to pure white in one application with frying your hair to mush! If I had used this instead of splat, maybe would have taken two or three applications but my hair would not have been this damaged and I'd still have reached platinum.If you want white or platinum, either do it professionally for fast results that might not fry.. or get enough of this stuff for 2 -3 applications (i.e. 4 bottles if you need 2 just to get all of your hair) and avoid frying your hair! Believe me I won't make that mistake again."

#Get all the adjectives from the sentence.
#Word_Tokenize tokenizes the sentence into words.
#Pos_tag returns tuples for each word in the form (word, POS).
# J stands for POS tags for adjectives.
adjectives = [token.lower() for token, pos in pos_tag(word_tokenize(sentence)) if pos.startswith('J') or pos.startswith('RB') or pos.startswith('V')]#Need to add adverbs and verbs.


negated_phrases = []
#Get all the adjectives from the sentence.
#Word_Tokenize tokenizes the sentence into words.
#Pos_tag returns tuples for each word in the form (word, POS).
# J stands for POS tags for adjectives.
# RB stands for Adverbs.
# V stands for verbs.
def convert_review_to_words(review_data):
    prev = None
    pPrev = None
    processedReview = []
    words = word_tokenize(review_data)
    describers = [(token.lower(),pos) for token, pos in pos_tag(word_tokenize(review_data)) if pos.startswith('J') or pos.startswith('RB') or pos.startswith('V')]
    for word in describers:
        if prev:
            if prev[0] == "not" and (word[1].startswith('J') or word[1].startswith('V')):
                processedReview.append(prev[0]+" "+word[0])
                negated_phrases.append(prev[0]+" "+word[0])
            else:
                if pprev:
                    if pprev == "not" and (word[1].startswith('J') or word[1].startswith('V')):
                        processedReview.append(pprev[0]+" "+prev[0]+" "+word[0])
                        negated_phrases.append(pprev[0]+" "+prev[0]+" "+word[0])
                    else:
                        if word[0] != "not" and word[0] != "n't":
                            processedReview.append(word[0])
                else:
                    if word[0] != "not" and word[0] != "n't":
                        processedReview.append(word[0])
        else:
            if word[0] != "not" and word[0] != "n't":
                processedReview.append(word[0])
        pprev = prev
        prev = word
    return(processedReview)

y=0
helpful=0
unhelpful=0
total=0
reviewCount=0
data = []
cleaned_data=[]
positive_data = []
negative_data=[]
neutral_data=[]
star_wise_review_count = [0] * 5
occurence = {}
with open('Beauty_5.json','r') as f:
    for line in f:
        currentLine=json.loads(line)
        data.append(currentLine)
        #helpful[0] is number of helpful Votes.
        #helpful[1] is total total number of votes.
        #To determine if the number of helpful votes is more than the number of unhelpful votes.
        # currentLine['helpful'][1]-currentLine['helpful'][0] gives the total unhelpful votes.
        if currentLine['helpful'][0]>0 and currentLine['helpful'][1]-currentLine['helpful'][0]<currentLine['helpful'][0]:
            #Overall is review rating.
            star_wise_review_count[int(currentLine['overall'])-1] += 1

            #tokenize and analyze the current review. Clean_data will consists of only adjectives.
            clean_data = convert_review_to_words(currentLine['summary'])

            #Create an occurence dictionary for rating wise token occurence.
            for word in clean_data:
                if word in occurence:
                    occurence[word][int(currentLine['overall'])-1] += 1
                else:
                    occurence[word] = [0] * 5
                    occurence[word][int(currentLine['overall'])-1] += 1

            #Create positive and negative bag of words.
            if(currentLine['overall'] > 3):
                #appending clean_data
                positive_data = positive_data + clean_data
            elif(currentLine['overall'] < 4):
                negative_data = negative_data + clean_data
            # else:
            #     neutral_data.append(clean_data)
            if(y%10000==0):
                print(y,",",clean_data)
            y+=1

positive_bag_of_word = Counter(positive_data)
negative_bag_of_word = Counter(negative_data)
# print(len(cleaned_data))

print("review count array : ",star_wise_review_count)
print("y :",y)
print("Pos :",len(positive_data))
print("Neg :",len(negative_data))
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(positive_bag_of_word)
pp.pprint(negative_bag_of_word)
pp.pprint(occurence);

#Calculate TokenWise sentiment score SS(t)
SS_t = {}
for token in occurence:
    if positive_bag_of_word[token] > 30 or negative_bag_of_word[token] > 30:
        SS_t[token] = 0
        num = 0;
        den = 0;
        for count in range(5):
            i = count + 1
            val1 = star_wise_review_count[4]/star_wise_review_count[count] * i * occurence[token][count]
            val2 = star_wise_review_count[4]/star_wise_review_count[count] * occurence[token][count]
            num += val1
            den += val2
        SS_t[token] = num/den

print("Sentiment Score:")
pp.pprint(SS_t)





# from sklearn.feature_extraction.text import CountVectorizer
#
# # Initialize the "CountVectorizer" object, which is scikit-learn's
# # bag of words tool.
# vectorizer = CountVectorizer(analyzer = "word",   \
#                              tokenizer = None,    \
#                              preprocessor = None, \
#                              stop_words = None,   \
#                              max_features = 50)
#
# # fit_transform() does two functions: First, it fits the model
# # and learns the vocabulary; second, it transforms our training data
# # into feature vectors. The input to fit_transform should be a list of
# # strings.
# train_positive_data_features = vectorizer.fit_transform(positive_data)
# train_negative_data_features = vectorizer.fit_transform(negative_data)
# # train_data_features = vectorizer.fit_transform(cleaned_data)
#
# # Numpy arrays are easy to work with, so convert the result to an
# # array
# # train_data_features = train_data_features.toarray()
# train_positive_data_features = train_positive_data_features.toarray()
# train_negative_data_features = train_negative_data_features.toarray()
# print("---------------")
# # print(train_data_features.shape)
# print("Positive :",train_positive_data_features.shape)
# print("Negative :",train_negative_data_features.shape)
# print("...............")
# vocab = vectorizer.get_feature_names()
# # print(vocabulary)
# # Sum up the counts of each vocabulary word
# # dist = np.sum(train_data_features, axis=0)
# dist_pos = np.sum(train_positive_data_features, axis=0)
# dist_neg = np.sum(train_negative_data_features, axis=0)
#
# zip(vocab, dist_pos)
# zip(vocab, dist_neg)
#
# # For each, print the vocabulary word and the number of times it
# # appears in the training set
# print("=========Printing Positive===========")
# for tag, count in zip(vocab, dist_pos):
#     print(count, tag)
# print("=========Printing Negative===========")
# for tag, count in zip(vocab, dist_neg):
#     print(count, tag)
#
# print("Sorted")
# for tag, count in sorted(zip, key=zip.get, reverse=True):
#     print(count, tag)
#
#
#         data.append(json.loads(line))
#     	if len(currentLine['reviewText'])<50:
#     		reviewCount+=1
#     		if currentLine['helpful'][0]==0 and currentLine['helpful'][1]==0:
#     			total+=1
#     		if currentLine['helpful'][0]>0:
#     			helpful+=1
#     		if currentLine['helpful'][1]>0:
#     			unhelpful+=1
#     	reviewCount+=1
#     	if currentLine['helpful'][0]==0 and currentLine['helpful'][1]==0:
#     		total+=1
#     	if currentLine['helpful'][0]>0:
#     		helpful+=1
#     	if currentLine['helpful'][1]>0:
#     		unhelpful+=1
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
#
#
# json_data.close()
#
# x=0
# for x in range(0, 2):
# 	row=data[x]
# 	# print(type(row))
# 	print(row['reviewTime'])
# 	print(len(row['reviewText']))
# 	x+=1