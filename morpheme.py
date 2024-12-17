#Raunaq Foridi 2024
#break a list of words into English morphemes, with or without keeping repeats
import json
import re

def morpheme(words,morphemes):
    if type(words) is not list:
        words=words.split(" ") #not preferable if dealing with punctuation, but better than errors.

    #morphemes should be provided as a dictionary
    #An Ordered list of Tokens, and an Ordered list of their respective roots listed
    output=[]
    for word in words:
        if len(word)<=4:
            output.append(word)
            #print(word)
            continue
        spans=[]
        for morpheme in morphemes["roots"]: #list of lists, each about a single morpheme
            for form in morpheme:              #each possible form of the morpheme
                form=form.lower()
                #print(form)
                if form[0]=="-" and form[-1]=="-":
                    #central case
                    #out of personal preference, skip any "short" internal morphemes
                    if len(form[1:-1])<3:
                        continue
                    search = re.search(r"\B"+form[1:-1]+r"\B",word)
                    if search:
                        #print(form+" "+word)
                        spans.append([search.span(),form[1:-1]])
                elif form[0]=="-":
                    #prefix case
                    #search = re.search(r"\b"+form[1:],word)
                    search = re.search(form[1:]+r"\b",word)
                    if search:
                        #print(form+" "+word)
                        spans.append([search.span(),form[1:]])
                elif form[-1]=="-":
                    #suffix case
                    #search = re.search(form[:-1]+r"\b",word)
                    search = re.search(r"/b"+form[:-1],word)
                    if search:
                        #print(form+" "+word)
                        spans.append([search.span(),form[:-1]])
        spans=sorted(spans, key = lambda x: x[0][0])        #sort by 1st position the morpheme begins at
        buffer=""               #when a letter isnt part of a morpheme, add it to the buffer.
        skip=0

        '''for i in range(len(word)):
            overlaps=[]
            for span_token in spans:
                if i in range(span_token[0][0],span_token[0][1]):   #if morpheme is over the ith letter
                    overlaps.append(span_token)
            if len(overlaps)>=1:
                if buffer!="":
                    output.append(buffer)
                    buffer=""
                #cull overlapping morphemes
                #impossible to guess which is most applicable. simply choose longest.
                overlaps.remove(max(overlaps, key = lambda x: len(x[1]))) #removes the one we want to keep in the end
                for j in overlaps:
                    spans.remove(j) #removes all conflicts. If no conflicts, overlaps is now empty so nothing happens
                if skip>0:
                    skip-=1
                    print("skipped %s, %s remain"%(word[i],skip))
                else:
                    for span_token in spans:
                        if i in range(span_token[0][0],span_token[0][1]):
                            output.append(span_token[1])
                            print(span_token[1])
                            skip=span_token[0][1]-span_token[0][0]-1
                            print("skip: "+str(skip))
                            break#'''

        
        '''for i in range(len(word)):
            overlaps=[]
            for span_token in spans:
                if i in range(span_token[0][0],span_token[0][1]):   #if morpheme is over the ith letter
                    overlaps.append(span_token)
            if len(overlaps)>=1:
                if buffer!="":
                    output.append(buffer)
                    buffer=""
                #cull overlapping morphemes
                #impossible to guess which is most applicable. simply choose longest.
                overlaps.remove(max(overlaps, key = lambda x: len(x[1]))) #removes the one we want to keep in the end
                for j in overlaps:
                    spans.remove(j) #removes all conflicts. If no conflicts, overlaps is now empty so nothing happens
                if skip>0:
                    skip-=1
                    print("skipped %s, %s remain"%(word[i],skip))
                else:
                    for span_token in spans:
                        if i in range(span_token[0][0],span_token[0][1]):
                            output.append(span_token[1])
                            print(span_token[1])
                            skip=span_token[0][1]-span_token[0][0]-1
                            print("skip: "+str(skip))
                            break

            else:
                buffer+=word[i]
                print("buffer: "+buffer)'''

        word_output=[]
        for i in range(len(word)):
            overlaps=[]
            for span_token in spans:
                if i in range(span_token[0][0],span_token[0][1]):   #if morpheme is over the ith letter
                    overlaps.append(span_token)
            if len(overlaps)>=1:
                if buffer!="":
                    word_output.append(buffer)
                    buffer=""
                #cull overlapping morphemes
                #impossible to guess which is most applicable. simply choose longest.
                overlaps.remove(max(overlaps, key = lambda x: len(x[1]))) #removes the one we want to keep in the end
                for j in overlaps:
                    spans.remove(j) #removes all conflicts. If no conflicts, overlaps is now empty so nothing happens
                if skip>0:
                    skip-=1
                    #print("skipped %s, %s remain"%(word[i],skip))
                else:
                    for span_token in spans:
                        if i in range(span_token[0][0],span_token[0][1]):
                            word_output.append(span_token[1])
                            #print(span_token[1])
                            skip=span_token[0][1]-span_token[0][0]-1
                            #print("skip: "+str(skip))
                            break

            else:
                buffer+=word[i]
                #print("buffer: "+buffer)
        if buffer:
            word_output.append(buffer)
        #print(word_output)
        #deal with remaining overlaps
        skip=0
        temp_word=word
        for token in word_output:
            #print("word: " +temp_word, "token: " +token)
            if re.search(r"\b"+token,temp_word):
                temp_word = temp_word[len(token):]  #removes the token from the word.
            else:
                #else there is an overlap
                while not re.search(r"\b"+token,temp_word):
                    token=token[1:] #iteratively remove the first character from token, until there is now a match
                    #print("modified to "+token)
                if token!=temp_word:
                    temp_word=temp_word[len(token):]
            #print("appending "+token)
            output.append(token)
            
                    

        #output.extend(word_output)      
        '''for span_token in spans:
            #print(span_token[1])
            output.append(span_token[1])   #[0] is the span, [1] is the token
            #print(output)'''

        #print(spans)
    #print(output)
    return output
                
def parse(path="morphemes.json"):
    with open(path,encoding="utf-8") as f:
        morph_dict=json.load(f)

    forms_list=[morph_dict[i]["forms"] for i in morph_dict]
    #forms = [[j["form"] for j in i] for i in forms_list]
    roots = [[j["root"] for j in i] for i in forms_list]
    tokens=[morph_dict[i] for i in morph_dict]

    return {"tokens": tokens, "roots": roots}
        
#sentence = "this is a standard sentence intentionally containing a number of words with both prefixes and suffices which will hopefully demonstrate this system"

#morpheme(sentence,parse())
