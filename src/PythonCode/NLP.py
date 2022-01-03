from string import punctuation
from typing import Counter
from pyvi import ViTokenizer
from pyvi import ViUtils
from pyvi import ViPosTagger
import string
import wordcloud
import matplotlib.pyplot as plt
import numpy as np


#Lấy danh sách stopword tiếng việt
stop_word = []
with open ("vi-stopwords.txt",encoding= 'UTF-8') as file_in:
    text = file_in.read()
    for word in text.split():
      stop_word.append(word)
    file_in.close()
punc = list(punctuation)
#Xử lý dữ liệu tiếng việt qua thư viện
with open("text.txt" ,encoding='UTF8') as file:
    Data = file.read()
file.close()


text_lower = Data.lower()#chuyển data sang viết thường toàn bộ
text_token = ViTokenizer.tokenize(text_lower)#Tách từ sử dụng ViTokenizer

Data_main = text_token.replace('_',' ')#chuyển các từ ghép thành từ đơn
Data_split = Data_main.split(' ')#tách từ thành list

Data_punc =[]#list lưu các dấu câu
Data_NonPunc = Data_split#list lưu data đã remove dấu câu
countParagraph = 0#đếm số kí tự xuống dòng, mỗi lần xuống dòng thì có 1 đoạn
for word in Data_NonPunc:
    if(word in punc):
        Data_punc.append(word)
        Data_NonPunc.remove(word)
    if(word=='\n'):
        Data_NonPunc.remove(word)
        countParagraph +=1
print('Number of paragraphs: ', countParagraph)

countSentence = 0
for punc in Data_punc:
    if(punc == '.'):
        countSentence +=1
print('Number of sentences: ', countSentence)
print('Total wordl count:', len(Data_NonPunc))

Data_NonStopWord = Data_split
for word in Data_NonStopWord:
    if(word in stop_word):
        Data_NonStopWord.remove(word)

print('Word count (Excluding common word): ', len(Data_NonStopWord))

Data_UnIdentical =[]
for word in Data_NonPunc:
    if(word not in Data_UnIdentical):
        Data_UnIdentical.append(word)
print('Number of different word: ',len(Data_UnIdentical))

Data_NonStw_UnIdentical =[]
for word in Data_NonStopWord:
    if(word not in Data_NonStw_UnIdentical):
        Data_NonStw_UnIdentical.append(word)
print('Different words (Excluding common words):', len(Data_NonStw_UnIdentical))

print('Words per sentence: ',round(len(Data_NonPunc)/countSentence, 2) )

Data_temp = ViUtils.remove_accents(Data_main).decode("utf-8")
for i in string.punctuation:
    Data_temp1 = Data_temp.replace(i,"")

Data_temp = Data_temp.replace(" ","")

print('Number of characters (All):',len(Data_temp))
print('Number of characters (Non punctuation):',len(Data_temp1))
print('Characters per word: ',round(len(Data_temp1)/len(Data_NonPunc),2))

accents1 =list('áéóúíýấắếứốớ')
accents2 = list('àèòùìỳầằềừồờ')
accents3 = list('ảẻỏủỉỷẩẳểửổở')
accents4 = list('ãẽõũĩỹẫẵễữỗỡ')
accents5 = list('ạẹọụịỵậặệựộợ')

sac= 0
huyen = 0 
hoi = 0
nga = 0
nang = 0

for word in Data_main:

    if(word in accents1):
        sac +=1
    if (word in accents2):
        huyen +=1
    if (word in accents3):
        hoi +=1
    if (word in accents4):
        nga +=1
    if (word in accents5):
        nang +=1
print('So dau sac: ', sac)
print('So dau huyen: ', huyen)
print('So dau hoi: ', hoi)
print('So dau nga: ', nga)
print('So dau nang: ', nang)

countLong = 0
for word in Data_NonPunc:
    if(len(word)>=5):
        countLong +=1
print ('Number of long word (Have more than 5 character): ', countLong)

lenWord =[]
for word in Data_split:
    lenWord.append(len(word))

LenDif =[]

for i in sorted(lenWord):
    if(i not in LenDif):
        print('Frequence of', i , ' letter word: ', round(lenWord.count(i)*100/len(Data_NonStopWord),2),'%')
        LenDif.append(i)
    else:
        continue

Temp =  ViPosTagger.postagging(text_token)
Tag = Temp[1]

print('Number of Adjective: ', Tag.count('A'))
print('Number of Coordinating conjunction: ', Tag.count('C'))
print('Number of Preposition: ', Tag.count('E'))
print('Number of Interjection: ', Tag.count('I'))
print('Number of Determiner: ', Tag.count('L'))
print('Number of Numeral: ', Tag.count('M'))
print('Number of Common noun: ', Tag.count('N'))
print('Number of Noun Classifier: ', Tag.count('Nc'))
print('Number of Noun abbreviation: ', Tag.count('Ny'))
print('Number of Proper noun: ', Tag.count('Np'))
print('Number of Unit noun: ', Tag.count('Nu'))
print('Number of Pronoun: ', Tag.count('P'))
print('Number of Adverb: ', Tag.count('R'))
print('Number of Subordinating conjunction: ', Tag.count('S'))
print('Number of Auxiliary, modal words: ', Tag.count('T'))
print('Number of Verb: ', Tag.count('V'))
print('Number of Unknown: ', Tag.count('X'))
print('Number of Filtered out (punctuation): ', Tag.count('F'))

"""
cloud = np.array(Data_NonStopWord).flatten()
plt.figure(figsize=(20,10))
word_cloud = wordcloud.WordCloud(max_words=100,background_color ="black",
                               width=2000,height=1000,mode="RGB").generate(str(cloud))
plt.axis("off")
plt.imshow(word_cloud)
word_cloud.to_file("wordcloud.png")
"""
f = open('output.txt', 'w')
f.write('Number of paragraphs: '+ str(countParagraph)+'\n')
f.write('Number of sentences: '+ str(countSentence)+'\n')
f.write('Total wordl count:'+ str(len(Data_NonPunc))+'\n')
f.write('Number of different word: '+str(len(Data_UnIdentical))+'\n')
f.write('Different words (Excluding common words):'+ str(len(Data_NonStw_UnIdentical))+'\n')

f.write('Words per sentence: '+str(round(len(Data_NonPunc)/countSentence, 2) )+'\n')

f.write('So dau sac: '+ str(sac)+'\n')
f.write('So dau huyen: '+ str(huyen)+'\n')
f.write('So dau hoi: '+ str(hoi)+'\n')
f.write('So dau nga: '+ str(nga)+'\n')
f.write('So dau nang: '+ str(nang)+'\n')
f.write('Number of characters (All):'+str(len(Data_temp))+'\n')
f.write('Number of characters (Non punctuation):'+str(len(Data_temp1))+'\n')
f.write('Characters per word: '+str(round(len(Data_temp1)/len(Data_NonPunc),2))+'\n')
f.write ('Number of long word (Have more than 5 character): '+ str(countLong)+'\n')
f.write('Number of Adjective: '+ str(Tag.count('A'))+'\n')
f.write('Number of Coordinating conjunction: '+ str(Tag.count('C'))+'\n')
f.write('Number of Preposition: '+ str(Tag.count('E'))+'\n')
f.write('Number of Interjection: '+ str(Tag.count('I'))+'\n')
f.write('Number of Determiner: '+ str(Tag.count('L'))+'\n')
f.write('Number of Numeral: '+ str(Tag.count('M'))+'\n')
f.write('Number of Common noun: '+ str(Tag.count('N'))+'\n')
f.write('Number of Noun Classifier: '+ str(Tag.count('Nc'))+'\n')
f.write('Number of Noun abbreviation: '+ str(Tag.count('Ny'))+'\n')
f.write('Number of Proper noun: '+ str(Tag.count('Np'))+'\n')
f.write('Number of Unit noun: '+ str(Tag.count('Nu'))+'\n')
f.write('Number of Pronoun: '+ str(Tag.count('P'))+'\n')
f.write('Number of Adverb: '+ str(Tag.count('R'))+'\n')
f.write('Number of Subordinating conjunction: '+ str(Tag.count('S'))+'\n')
f.write('Number of Auxiliary, modal words: '+ str(Tag.count('T'))+'\n')
f.write('Number of Verb: '+ str(Tag.count('V'))+'\n')
f.write('Number of Unknown: '+ str(Tag.count('X'))+'\n')
f.write('Number of Filtered out (punctuation): '+ str(Tag.count('F'))+'\n')
f.close()