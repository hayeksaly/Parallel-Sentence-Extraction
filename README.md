# Parallel-Sentence-Extraction
Capstone Project- Parallel Sentence Extraction from comparable corpora.
Definition of concepts: 
Comparable Corpora: Comparable corpora are two texts containing same information and same topic in two different languages.
Parallel Sentences: Parallel sentences are sentences from two different languages that are the exact translation of each others.

## Goal of the project: Extract parallel sentences from comparable corpora.
Motivation: Lack of available parallel sentences in all languages influence on the low quality of translation of sentences used 
in Machine translation models. For this purpuse, it is mandatory to have parallel sentences in two languages(this project works on
Arabic-English). In the presence of abondance of comparable corpora texts(every website having more than one language version), 
Extracting parallel sentences from comparable corpora is a very important process to improve machine translation.

### Overview:
The program is executed to take as input 2 texts in Arabic and English language, and gives us the parallel data: English and Arabic parallel sentences.
The program is divided in 3 steps:
1st Step: Processing the data.
Takes the path of the directory that contains the Arabic and English texts that we want to extract parallel data from, open and reads the texts successively and saves them in Python as 2 lists of texts that will be handled later. The texts should be present in the directory as txt file for both English and Arabic, and the name of the Arabic document same as English for the comparable corpora. (example: Global Voices and the Power of We.ar; Global Voices and the Power of We.en) The Arabic document ends with .ar and the English document ends with .en. This way the machine can understand the document given, read the data and stores it.

2nd Step: Creating alignment function
Creating the align function, that segments the texts into sentences, translate Arabic to English, computes chrf-score for each 2 sentences and saves the sentences with a high chrf-score(>0.5) which means that they are parallel. It also contains SacreBleu computation of sentences for Evaluation, in addition to number of aligned sentences extracted, English and Arabic Words.
Align text function takes 2 texts as input: English and Arabic and gives as a result 7 outputs:  the parallel data (in a data frame shape containing 2 columns Arabic and English sentences), in addition to number of parallel sentences extracted, initial number of English and Arabic sentences, number of English and Arabic words extracted, with SacreBleu score of the parallel sentences extracted. 

3rd Step: Extracting data
Loop over the data collected in Step 1(English-Arabic texts), input them successively in text_align function, extracts the parallel data that we want and outputs it. Parallel Sentences are then grouped in a big Data Frame that is printed finally. The data frame has 2 column: 1 column for English Sentences and one for Arabic sentences extracted from all the texts of the directory.

### Practical Usage:

Packages required to install before running the program: nltk, nltk.download(‘puntk’), deep_translator, spacy, numpy, pandas, re, os, sacrebleu.(if any package is missing it can be installed through pip install package)
When first running the program, it will demand the user to write the path of the directory where the files are present ("Enter the path of the folder containing texts: "). The user is supposed to enter the path of the directory (for example: C:\Users\Ideapad\Desktop\Comparable-Corpora). For best usage it is preferred to put the python program file (ParallelSentenceExtraction.py.py) in the same directory of the files wished to extract information from.
Time: The program takes about 1 hr to extract parallel sentences from Global voices comparable texts (610 Arabic and 610 English texts).
Then the program will run and give 4 outputs: First, it will compute the number of Arabic and English texts present in the directory, Secondly, it will output the parallel sentences considered parallel through chrf-score. These sentences are English-English sentences representing the translated Arabic sentences vs the English sentences. Thirdly, it will output the evaluation metrics scores, initial and final English and Arabic words and sentences, in addition to sacrebleu score. And lastly, it outputs the final parallel sentences extracted from all the documents in the directory as a data frame containing English and Arabic sentences. 
Note: This program can be used on any IDE but preferably not to be used with Google Collab because it is more complex to handle the files from the directory.

#### Optional arguments:
•	The chrf-score level: This program gives as output the sentences that are considered parallel relatively to chrf-score>0.5. In our practice, we found that a score higher than 0.5 is the ultimate value to keep the high quality of sentences extracted and the high coverage. 
However, this scoring can be changed by the user. It is present at line 91 in the code. Chrf-score can be between 0 and 1. A chrf-score = 1 means that the sentences are exact same in the English language and that the original Arabic and English are exact parallel. A score higher than 0.7 usually indicates very high quality of parallel data. The more we raise the score the higher the quality of parallel data we obtain. But of course the higher the score is, the less coverage of data we obtain. So this option make it flexible to the user to choose the trade-off quality-coverage. 
•	Another optional thing is to change the output structure of parallel data. If the user doesn’t wants the data as a data frame representing the parallel sentences; an option is to uncomment lines 132-135 in the code to have the data outputted as strings (Arabic sentence pursued by its parallel English sentence..) and comment the next lines from 137-139 that output it as a data frame and the line 171 that appends the data.

#### Diving into coding:
After doing many researches, we found the optimal ways to tackle each step. So first, in the align_text function, the first step is the segmentation. After trials on the data, we found spacy and nltk libraries. Spacy showed best practice for English and nltk for Arabic. So we used them for English and Arabic texts segmenting to sentences. 
Then for the translation step, we used Google translate API from deep learning library. For aligning step, we used chrf-score. And for evaluation, we used SacreBleu and coverage calculations. Note that higher chrf-score chosen will lead to higher SacreBleu score and less coverage. 
For splitting sentences into words we used .split() function. And for iterating over the sentences we want to compare, we looped over each sentence from English document compared to each sentence in the Arabic translated document approach. 


