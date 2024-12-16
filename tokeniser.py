#Raunaq Foridi 2024
#tokeniser
#takes a corpus of text and tokenises it
import re

def pre_process(text, mode="simple"):
    if mode=="simple":
        #breaks a string into individual words, removes case and punctuation
        for symbol in [",",".","!","?","/","*","'",'"',"(",")"]:
            text=text.replace(symbol,"").lower()

        return text.split(" ")

    elif mode=="unicode":
        return [i for i in re.split("([,.!?/*' ])",text) if i!=""]

def tokenise(text,mode="simple"):
    
    #Assumes the text is in the form of a list of entries
    #if not, creates one.
    
    if type(text) is not list:
        text = [text]

    token_list=[]
    for line in text:
        #preprocessing, removing punctuaton
        #for symbol in [",",".","!","?","/","*"]:
        #    line=line.replace(symbol,"").lower()

        #tokens=line.split(" ")
        tokens = pre_process(line, mode)
        for token in tokens:
            if token not in token_list:
                token_list.append(token)

    return token_list
    
def pad_sequences(sequences,padding="post"):
    output=[]
    output.extend(sequences)
    #takes a list of sequences, and pads them to be the same length
    length = max([len(i) for i in sequences])
    for sequence in output:
        if len(sequence)<length:
            if padding=="post":
                sequence.extend([0 for i in range(0,length-len(sequence))])
            else:
                sequence=[0 for i in range(0,length-len(sequence))].extend(sequence)

    return output
