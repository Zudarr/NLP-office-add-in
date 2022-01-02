from string import punctuation
from typing import Counter
from pyvi import ViTokenizer
from pyvi import ViUtils
from pyvi import ViPosTagger
import string
import wordcloud
import matplotlib.pyplot as plt
import numpy as np
import sys


#Lấy danh sách stopword tiếng việt
stop_word = []
with open ("vi-stopwords.txt",encoding= 'UTF-8') as file_in:
    text = file_in.read()
    for word in text.split():
      stop_word.append(word)
    file_in.close()
punc = list(punctuation)
#Xử lý dữ liệu tiếng việt qua thư viện
Data = sys.argv[1]


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

countSentence = 0
for punc in Data_punc:
    if(punc == '.'):
        countSentence +=1

Data_NonStopWord = Data_split
for word in Data_NonStopWord:
    if(word in stop_word):
        Data_NonStopWord.remove(word)


Data_UnIdentical =[]
for word in Data_NonPunc:
    if(word not in Data_UnIdentical):
        Data_UnIdentical.append(word)

Data_NonStw_UnIdentical =[]
for word in Data_NonStopWord:
    if(word not in Data_NonStw_UnIdentical):
        Data_NonStw_UnIdentical.append(word)

Data_temp = ViUtils.remove_accents(Data_main).decode("utf-8")
for i in string.punctuation:
    Data_temp1 = Data_temp.replace(i,"")

Data_temp = Data_temp.replace(" ","")

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

countLong = 0
for word in Data_NonPunc:
    if(len(word)>=5):
        countLong +=1

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


#output
dcitOut = {
    "NumParagraph" : countParagraph,
    # "NumSentence" : countSentence,
    # "NumWord" : len(Data_NonPunc),
    # "NumWord_NonSTW": len(Data_NonStopWord),
    # "NumWord_Diff": len(Data_UnIdentical),
    # "NumWord_Diff_NonSTW": len(Data_NonStw_UnIdentical),
    # "WordPerSent": round(len(Data_NonPunc)/countSentence, 2),
    # "NumChar":len(Data_temp),
    # "NumChar_NonPunc": len(Data_temp1),
    # "CharPerWord": round(len(Data_temp1)/len(Data_NonPunc),2),
    # "NumSac": sac,
    # "NumHuyen": huyen,
    # "NumHoi": hoi,
    # "NumNga": nga,
    # "NumNang": nang,
    # "LongWord": countLong,
    # "NumAdj": Tag.count('A'),
    # "NumCoordinate": Tag.count('C'),
    # "NumPrep": Tag.count('E'),
    # "NumInterject": Tag.count('I'),
    # "NumDeter":Tag.count('L'),
    # "NumNumeral": Tag.count('M'),
    # "NumNoun": Tag.count('N'),
    # "NumNoun_classifier":Tag.count('Nc'),
    # "NumNoun_abberev": Tag.count('Ny'),
    # "NumNoun_prop":Tag.count('Np'),
    # "NumNoun_unit":Tag.count('Nu'),
    # "NumPronoun":Tag.count('P'),
    # "NumAdv":Tag.count('R'),
    # "NumSubor":Tag.count('S'),
    # "NumAu_Modal":Tag.count('T'),
    # "NumVerb":Tag.count('V'),
    # "NumUnknown":Tag.count('X'),
    # "NumPunc":Tag.count('F'),
}

print(dcitOut)