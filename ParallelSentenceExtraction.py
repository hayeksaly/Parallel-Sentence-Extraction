'''1st Step:
   import arabic and english files, read them from the directory chosen by user,
   and place texts in lists  '''

#import libraries for getting documents
import os
from re import search

directory = input("Enter the path of the folder containing texts: ")

#opening folder that contains documents
arr = os.listdir(directory)

#finding english texts in the folder and appending each text in a list called english
strtxt = ".en.txt"
english= []
c=0
for txtfile in arr:
    if txtfile.__contains__(strtxt):
      fileObject = open(txtfile, "r", encoding="UTF-8")

      data = fileObject.read()
      english.append(data)
print("We have", len(english), "English texts in the document")

#finding arabic texts in the folder and appending each text in a list called arabic
arabic=[]

artext = ".ar.txt"
for txtfile in arr:
    if txtfile.__contains__(artext):
      fileObject = open(txtfile, "r", encoding="UTF-8")

      data = fileObject.read()
      arabic.append(data)
print("We have", len(arabic), "Arabic texts in the document")

''' 2nd Step:
    Text Align function: Takes English and Arabic texts, Segment them to sentences,
    translate arabic sentences, compute chrf-score(0.5 treashhold), and extract parallel sentences,
    it also keeps track of number of sentences and words to compute coverage and SacreBleu Score'''

#importing libraries for the aligning function
import nltk #for splitting arabic text to sentences and chrf_score
import nltk.translate.chrf_score #to find if 2 sentences are parallel or not
from deep_translator import GoogleTranslator #translate arabic sentences
import spacy #split english text to sentences
import pandas as pd #create data frame at the end
import sacrebleu
from nltk.translate import bleu_score
from sacrebleu import sentence_bleu


#function for aligning texts: takes arabic and english corpus and extract parallel sentences from them
def align_text(english_corpus, arabic_corpus):

#initializing iterators to compute sacrebleu score
  sacrebleu = 0

   #Split Arabic text to sentences using nltk library(best for arabic language)
  ar_list = nltk.tokenize.sent_tokenize(arabic_corpus)
  # print("Original Arabic Sentence array is:", ar_list)

  #translate the elements of the list
  trans_list = []
  for trans in ar_list:
      trans_ar = GoogleTranslator(source='auto', target='en').translate(trans)
      trans_list.append(trans_ar)
  nar = len(trans_list) #nar is the number of arabic sentences in the translated document
  # print("The number of sentences in the arabic text is:", nar)


  #split english text to sentences using spacy(best for english texts)
  nlp = spacy.load('en_core_web_sm')
  token = nlp(english_corpus)
  en_list = []
  nen = 0 #to compute number of sentences extracted
  for sent in token.sents:
     a = sent.text.strip()
     if len(a)>2:
        en_list.append(a)
        nen=nen+1 #nen is the number of english sentences in the english document

  # print("The number of sentences in english text is:", nen)

  #extracting parallel sentences
  i=[]
  index_list=[]
  en_res_list=[]
  wordarr=0
  worden=0
  #loop over all the sentences to catch parallel sentences
  for x, y in [(x,y) for x in en_list for y in trans_list]:

         try:
            chrf = nltk.translate.chrf_score.sentence_chrf(x, y) # using character F-score to score the sentences.
         except RuntimeError:
            chrf = 0
         if chrf>0.5:   #chrf for sentences to be aligned

          #compute english and arabic words obtained
           ref =x.split()
           tar=y.split()
           numen_words = len(ref)
           numar_words = len(tar)
           wordarr = wordarr + numar_words
           worden = worden + numen_words
           i.append(chrf)

           #print the sentences considered parallel(chrf-score>0.5)
           print('Parallel sentences are:')
           print(("Arabic Translated", y,"||","English", x))

           #keep track of arabic translated index to find the original arabic sentence
           index_list.append(trans_list.index(y))
           en_res_list.append(x)

           #compute sacrebleu score
           sacre = bleu_score.sentence_bleu([x], y)
           sacrebleu = sacrebleu + sacre

  #original arabic list extracted
  res_list = [ar_list[i] for i in index_list]

  #compute number of arabic words obtained
  araWords=0
  for j in res_list:
      wrd = j.split()
      lent = len(wrd)
      araWords= araWords +lent

  # parallel=[]
  # for x, y in zip(res_list, en_res_list):
  #     parallel.append((x,y))
  # print(parallel)

  parallel = pd.DataFrame()
  parallel["Arabic"] = res_list
  parallel["English"] = en_res_list

  #return english and translated arabic sentences, initial arabic and english sentences, number of sentences obtained, and sacrebleu score
  return parallel, len(i), nar, nen, araWords, worden, sacrebleu


''' 3rd Step:
    Loop over all texts prepared in the lists and align them in the 2nd step function: text_align,
    extract parallel sentences, and print the result in a data frame ,
    it also computes the initial and final number of words and sentences,
    in addition to final SacreBleu Score and prints the results'''

#loop over the texts in the directory and align them through align_text function
r=0
s=0
u=0
sb=0
we=0
wa=0
word_ar = 0
word_en = 0
Data_parallel = pd.DataFrame()
for x, y in zip(english, arabic):
     try:
       wordenglish = x.split()
       wordarabic = y.split()
       initial_english = len(wordenglish)
       initial_arabic = len(wordarabic)
       we = we + initial_english
       wa = wa + initial_arabic

       parallel, num, naar, neen,arabic_words, english_words, sacreb = align_text(x, y)
       Data_parallel = pd.concat([Data_parallel, parallel])
       r = r + num   #number of parallel sentences obtained
       s = s + naar  #initial arabic sentences number
       u = u + neen  #initial english sentences number
       sb = sb + sacreb #sacrebleu score
       word_ar = word_ar + arabic_words
       word_en = word_en + english_words

     except Exception as e:
        print(e)

print("Number of parallel sentences is:",r,"Initial arabic sentences number is:", s, "coverage=", r/s,"Initial number of english sentences is:", u, "coverage=", r/u, "Initial English Words", we, "Initial Arabic Words:", wa, "Extracted English words",word_en ,"Extracted Arabic Words:", word_ar,"Coveragewords(En; Ar)=",word_en/we, word_ar/wa,  "SacreBleu Score:",sb/r)
print(Data_parallel)
