from django.shortcuts import render ,HttpResponse
from django.template import loader
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
import transformers
from transformers import T5ForConditionalGeneration , T5Tokenizer

# Create your views here.
def index (request):
    summary = ""
    
    if request.method == "POST" :
        text = request.POST.get('input_str')

        org_word = len(text.split())
        
        # print(text)
        stopwords = list(STOP_WORDS)
        punctuations = list(punctuation)
        # print(stopwords)
        text2 = ""
        for i in text.lower():
            if i in punctuations:
                continue
            else:
                text2+=i
        # print(text2)
        token = text2.split()
        #print(token)
        freq_words = {}
        for words in token:
            # print(words.lower())
            if words.lower() not in stopwords and words.lower() not in punctuations:
                if words.lower() in freq_words:
                    freq_words[words.lower()]+=1
                else:
                    freq_words[words.lower()] = 1
            else:
                continue
            
        max_freq = max(freq_words.values())
        #print(max_freq)

        for word in freq_words:
            freq_words[word]/=max_freq

        sent_scores = {}
        sents = text.split(".")
        for sent in sents:
            word = sent.split()
            for w in word :
                if w.lower() not in stopwords and w.lower() not in punctuations and w.lower() in freq_words:
                    if sent not in sent_scores:
                        sent_scores[sent]= freq_words[w.lower()]
                    else:
                        sent_scores[sent]+=freq_words[w.lower()]
                else:
                    continue
        #print(sent_scores)

        sen_len = int(len(sent_scores)*0.5)

        sum = nlargest (sen_len,sent_scores,key = sent_scores.get)
        #print(sum)
            
        for sen in sum:
            summary += sen + "."

        wordcnt = len(summary.split())
        return render(request,'extractive.html',{"result" : summary, "words" : wordcnt ,"original": org_word})
    return render(request , 'extractive.html',{"result": summary})        
    

def index2 (request):
    summary_text =""
    if request.method == "POST" :
        model = T5ForConditionalGeneration.from_pretrained('t5-small')
        tokenizer = T5Tokenizer.from_pretrained('t5-small')


        str = request.POST.get('input_str')
        text = ""

        for char in str:
            if char == ",":
                continue
            else:
                text += char

        org_word = len(text.split())
        max_length = int(0.6*len(text))

        input_ids = tokenizer.encode(text, return_tensors='pt')
        summary = model.generate(input_ids, max_length = max_length)

        summary_text = tokenizer.decode(summary[0],skip_special_tokens = True)
        
        print(type(summary_text))

        summary = summary_text[0].upper()

        for i in range(1,len(summary_text)):
            summary += summary_text[i]

        wordcount = len(summary.split())
        

       

        return render(request,'abstractive.html',{"result" : summary, "words" : wordcount ,"original": org_word})
    
    return render(request,'abstractive.html',{"result" : summary_text})

