import json
import numpy as np
from nltk import word_tokenize, pos_tag
from nltk.corpus import stopwords


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


def createFeatureVector(accumulated_bag_of_words, accumulated_bag_of_phrases, SS_t):
    word_vector = [0] * len(accumulated_bag_of_words)
    phrase_vector = [0] * len(accumulated_bag_of_phrases)
    feature_vector = []
    data = []
    cleaned_data=[]
    input_data = []
    with open('Beauty_5.json','r') as f:
        for line in f:
            currentLine=json.loads(line)
            data.append(currentLine)

        # numpy.random.shuffle(data)
        # train_size = len(data)
        # div = round(80*train_size/100)
        # training, test = x[:div,:], x[div:,:]

        for currentLine in data:
            word_hash = 0
            phrase_hash = 0
            average_sentiment_score = 0
            #helpful[0] is number of helpful Votes.
            #helpful[1] is total total number of votes.
            #To determine if the number of helpful votes is more than the number of unhelpful votes.
            # currentLine['helpful'][1]-currentLine['helpful'][0] gives the total unhelpful votes.
            if currentLine['helpful'][0]>0 and currentLine['helpful'][1]-currentLine['helpful'][0]<currentLine['helpful'][0]:

                #tokenize and analyze the current review. Clean_data will consists of only adjectives.
                clean_data = convert_review_to_words(currentLine['summary'])

                #Create an occurence dictionary for rating wise token occurence.
                prev = None
                pPrev = None
                sentimentScoreSum = 0
                count = 0
                print("\n",currentLine['summary'],"\n");
                for word in clean_data:
                	x = -1;
                	if word in SS_t:
                		sentimentScoreSum += SS_t[word]
                		count+= 1
                	if word.startswith('not'):
                		if word in accumulated_bag_of_phrases:
                			x = accumulated_bag_of_phrases.index(word)
                			phrase_vector[x] = 1
                			print(word,"\n");
                	else:
                		if word in accumulated_bag_of_words:
                			x = accumulated_bag_of_words.index(word)
                			word_vector[x] = 1
                			print(word,"\n");

                print("===========================\n")
                # for word in clean_data:
                #     x = -1
                #     if prev:
                #         if prev == "not":
                #             if (prev+" "+word) in accumulated_bag_of_phrases:
                #                 accumulated_bag_of_phrases.index(prev+" "+word)
                #                 if x > -1:
                #                     phrase_vector[x] = 1
                #                 sentimentScoreSum += SS_t[prev+" "+word]
                #                 count += 1
                #         else:
                #             if pprev:
                #                 if pprev == "not":
                #                     if (pprev+" "+prev+" "+word) in accumulated_bag_of_phrases:
                #                         x = accumulated_bag_of_phrases.index(pprev+" "+prev+" "+word)
                #                         if x > -1:
                #                             phrase_vector[x] = 1
                #                         sentimentScoreSum += SS_t[pprev+" "+prev+" "+word]
                #                         count += 1
                #                 else:
                #                     if word in accumulated_bag_of_words:
                #                         x = accumulated_bag_of_words.index(word)
                #                         if x > -1:
                #                             word_vector[x] = 1
                #                         sentimentScoreSum += SS_t[word]
                #                         count += 1
                #             else:
                #                 if word in accumulated_bag_of_words:
                #                     x = accumulated_bag_of_words.index(word)
                #                     if x > -1:
                #                         word_vector[x] = 1
                #                     sentimentScoreSum += SS_t[word]
                #                     count += 1
                #     else:
                #         if word in accumulated_bag_of_words:
                #             x = accumulated_bag_of_words.index(word)
                #             if x > -1:
                #                 word_vector[x] = 1
                #             sentimentScoreSum += SS_t[word]
                #             count += 1
                #     pprev = prev
                #     prev = word
                if count > 0:
                    word_hash = hash(str(word_vector))
                    phrase_hash = hash(str(phrase_vector))
                    average_sentiment_score = sentimentScoreSum / count
                    row = []
                    row.append(average_sentiment_score)
                    row.append(word_hash)
                    row.append(phrase_hash)
                    if int(currentLine['overall']) > 3:
                        row.append(1)
                    else:
                        row.append(0)
                    feature_vector.append(row)
    print(feature_vector)
    np.savetxt("Output.csv", feature_vector, delimiter=",")
    np.savetxt("Output.txt", feature_vector, delimiter=",")
