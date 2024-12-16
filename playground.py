#Raunaq Foridi 2024
#A simple "playground" for the sentiment networks
#Allows you to type in sentence and receive the networks "Judgement" of it

import tensorflow as tf
import numpy
import tokeniser

file=open("sarcasm_tokens.txt").readlines()
file = [i[2:-2] for i in file]

def prep(text):
    output=[]
    for word in tokeniser.pre_process(text):
        if word in file:
            output.append(file.index(word)+1)
        else:
            output.append(-1)
    return numpy.array([output])

sarcasm = tf.keras.models.load_model("simpleSarcasm.keras")

test=""
while test!="EXIT_CODE":
    test=input("Sentence to test: ")
    print(sarcasm.predict(prep(test)))
