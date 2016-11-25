#!usr/bin/python3
import json
import re
import numpy as np
import pprint;
import csv
#import nltk
from nltk.corpus import stopwords # Import the stop word list
from nltk import word_tokenize, pos_tag
from collections import Counter
import accumulated_bag_of_words as abw
sentence = "I tried to take dyed hair from a natural color to white/platinum blonde with Slpat bleach. Then I wanted to add their purple for a streak in the front.. My goodness what a horrible experience. Their stuff hurt and one application left my hair so fried I thought it'd fall out!! Their purple was not purple and bled even after careful dying. The bleach just ruined my hair, it was this horrible mush. I hated it but bleached the purple out, oh my poor hair.Now I have bleached before with the blue tub of bleach by l'oreal. That stuff was awesome, still dried out my hair but not as bad as Splat!Anyway this Platinum was a little weird as it expanded and erupted out of the bottle but I just needed my roots done. I was terrified because I'd been using Everto every super duper conditioner I could find but my hair was a mess. Wow it actually made my hair feel stronger! I don't understand how but it repaired my hair! My roots are not platinum but after one shot of this stuff they are a very light golden blonde. NOTHING will in one shot take a medium brown hair to pure white in one application with frying your hair to mush! If I had used this instead of splat, maybe would have taken two or three applications but my hair would not have been this damaged and I'd still have reached platinum.If you want white or platinum, either do it professionally for fast results that might not fry.. or get enough of this stuff for 2 -3 applications (i.e. 4 bottles if you need 2 just to get all of your hair) and avoid frying your hair! Believe me I won't make that mistake again."

#Get all the adjectives from the sentence.
#Word_Tokenize tokenizes the sentence into words.
#Pos_tag returns tuples for each word in the form (word, POS).
# J stands for POS tags for adjectives.
adjectives = [token.lower() for token, pos in pos_tag(word_tokenize(sentence)) if pos.startswith('J') or pos.startswith('RB') or pos.startswith('V')]#Need to add adverbs and verbs.
filtered_words = [word for word in adjectives if word not in stopwords.words('english')]
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
            if (prev[0] == "not" or prev[0]=="n't") and (word[1].startswith('J') or word[1].startswith('V')):
                processedReview.append("not "+word[0])
                negated_phrases.append("not "+word[0])
            else:
                if pprev:
                    if (pprev[0] == "not" or pprev[0]=="n't") and (word[1].startswith('J') or word[1].startswith('V')):
                        processedReview.append("not "+prev[0]+" "+word[0])
                        negated_phrases.append("not "+prev[0]+" "+word[0])
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
    #Removing stop words like is, so, have etc.
    filtered_words = [wrd for wrd in processedReview if wrd not in stopwords.words('english')]
    return(filtered_words)

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
print(len(cleaned_data))
print("review count array : ",star_wise_review_count)
print("y :",y)
print("Pos :",len(positive_data))
print("Neg :",len(negative_data))
pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(positive_bag_of_word)
# pp.pprint(negative_bag_of_word)
pp.pprint(occurence);
#Creating csv files so that these files can be used directly instead of extracting this data every time.
csvfile1 = "positive_bag_of_word.csv"
csvfile2 = "negative_bag_of_word.csv"
csvfile3 = "occurance.csv"
with open(csvfile1, 'w') as f:
    [f.write('{0},{1}\n'.format(key, value)) for key, value in positive_bag_of_word.items()]
with open(csvfile2, 'w') as f:
    [f.write('{0},{1}\n'.format(key, value)) for key, value in negative_bag_of_word.items()]
with open(csvfile3, 'w') as f:
    [f.write('{0},{1}\n'.format(key, value)) for key, value in occurence.items()]

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
# pp.pprint(SS_t)
# np.savetxt("Sentiment_Score.csv", SS_t, delimiter=",")
Sentiment_Score_csv = "Sentiment_Score.csv"
with open(Sentiment_Score_csv, 'w') as f:
    [f.write('{0},{1}\n'.format(key, value)) for key, value in SS_t.items()]


accumulated_bag_of_words = []
for token in occurence:
    if positive_bag_of_word[token] > 30 or negative_bag_of_word[token] > 30:
        accumulated_bag_of_words.append(token)

print("Accumulated bag of words:")
accumulated_bag_of_words = sorted(accumulated_bag_of_words)
print(accumulated_bag_of_words)
# np.savetxt("accumulated_bag_of_words.csv", accumulated_bag_of_words, delimiter=",")

accumulated_bag_of_phrases = []
for token in SS_t:
    if (' ' in token) == True:
        accumulated_bag_of_phrases.append(token)

print("Accumulated bag of phrases:")
accumulated_bag_of_phrases = sorted(accumulated_bag_of_phrases)
print(accumulated_bag_of_phrases)
# np.savetxt("accumulated_bag_of_phrases.csv", accumulated_bag_of_phrases, delimiter=",")


aVector=abw.createFeatureVector(accumulated_bag_of_words, accumulated_bag_of_phrases, SS_t)
# print(type(aVector))
# np.savetxt("foo.csv", aVector, delimiter=",")
