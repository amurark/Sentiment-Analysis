#!usr//bin/python3
import json
from bs4 import BeautifulSoup             


# json_data = open('Digital_Music_5_sub.json','r')
# data = json.load(json_data)
y=0
helpful=0
unhelpful=0
total=0
reviewCount=0
data = []
with open('Beauty_5.json','r') as f:
    for line in f:
    	currentLine=json.loads(line)
    	data.append(currentLine)
    	# data.append(json.loads(line))
    	# if len(currentLine['reviewText'])<50:
    	# 	reviewCount+=1
    	# 	if currentLine['helpful'][0]==0 and currentLine['helpful'][1]==0:
    	# 		total+=1
    	# 	if currentLine['helpful'][0]>0:
    	# 		helpful+=1
    	# 	if currentLine['helpful'][1]>0:
    	# 		unhelpful+=1
    	reviewCount+=1
    	if currentLine['helpful'][0]==0 and currentLine['helpful'][1]==0:
    		total+=1
    	if currentLine['helpful'][0]>0:
    		helpful+=1
    	if currentLine['helpful'][1]>0:
    		unhelpful+=1
# print(len(data))
print(data[41]["reviewText"])
# example1 = BeautifulSoup(data[41]["reviewText"], "lxml") 
# print(".......")
# print(example1) 
print(reviewCount)
print(total)
print(helpful)
print(unhelpful)
# json_data.close()
# x=0
# for x in range(0, 2):
# 	row=data[x]
# 	# print(type(row))
# 	print(row['reviewTime'])
# 	print(len(row['reviewText']))
# 	x+=1