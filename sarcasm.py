#Raunaq Foridi 2024
#Sarcasm detection
#Trained and tested with the Sarcasm Headlines dataset by Rishabh Misra 2019
print("importing modules")
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import tensorflow as tf
#tf.get_logger().setLevel('ERROR')
tf.autograph.set_verbosity(0)
print("successfully imported tensorflow")
import tokeniser
from ast import literal_eval
import numpy
print("opening dataset")
dataset = open("Sarcasm_Headlines_Dataset.json").readlines()

oov_token= "<oov>"
token_mode = "simple"  #how are tokens split?

#turn dataset into list of dictionaries
dataset = [literal_eval(i) for i in dataset]

#A list of only text, to use for tokenisation
corpus = [data["headline"] for data in dataset]
print("tokenising")
tokens = tokeniser.tokenise(corpus, token_mode)
sequences = [[tokens.index(token)+1 for token in tokeniser.pre_process(line, token_mode)] for line in corpus]
sequences = tokeniser.pad_sequences(sequences)

training_split=21000    #How much of the dataset is used for training rather than testing

train_x=numpy.array(sequences[0:training_split])     #Input data
test_x =numpy.array(sequences[training_split:])

labels= [data["is_sarcastic"] for data in dataset]
train_y = numpy.array(labels[0:training_split])     #Expected Outputs
test_y =  numpy.array(labels[training_split:])

#number of parameters
vocab_size = 10000
embedding_dim = 16

print("building model")
#Model
#The embedding layer analyses each token in a sequence, so doesn't give a fixed length output
#pooling allows us to get a single embedding for the entire sequence
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(vocab_size,embedding_dim),    #returns variable length
    tf.keras.layers.GlobalAveragePooling1D(),   #fixes length to average
    tf.keras.layers.Dense(24, activation = "relu"),
    tf.keras.layers.Dense(1, activation="sigmoid")])

model.compile(
    loss="binary_crossentropy",
    optimizer="adam",
    metrics=["accuracy"])

print("training")
#training
model.fit(train_x,train_y,epochs=10,validation_data=(test_x,test_y), verbose = 1)
#model.fit(train_x,train_y,epochs=1)
print("trained")
print("testing:")
model.evaluate(test_x,test_y,verbose=1)
sentences = ["granny starting to fear spiders in the garden might be real",
            "game of thrones season finale showing this sunday night",
             "weird officials assure idiots that today's trains will run just as fucked up as usual",
             "of course not",
             "damn, I'm not good at this",
             "i just dont understand how this guy is so bad !"]
#sentences = tokeniser.tokenise(sentences)
#print(sentences[0:5])
#sentences = [[tokens.index(token) for token in line] for line in sentences]
tokenised_sentences=[[] for i in sentences]
for i in range(len(sentences)):
    for word in tokeniser.pre_process(sentences[i], token_mode):
        if word in tokens:
            tokenised_sentences[i].append(tokens.index(word)+1)
        else:
            #print(word)
            tokenised_sentences[i].append(-1)

#print("might" in tokens)
tokenised_sequences=tokeniser.pad_sequences(tokenised_sentences)
tokenised_sentences=numpy.array(tokenised_sentences)
#print("DELINEATOR.")
#print(sentences)
print(model.predict(tokenised_sentences))
#model.save(token_mode+"Sarcasm.keras")
