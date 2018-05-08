import os
import sys
import pickle

from numpy import array
from keras.preprocessing.text import Tokenizer
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Embedding
from keras.utils.vis_utils import plot_model
from keras.models import model_from_json

# generate a sequence from the model
def generate_seq(modelComp, seed_text, n_words):
	model = modelComp[0]
	tokenizer = modelComp[1]
	in_text, result = seed_text, seed_text
	# generate a fixed number of words
	for _ in range(n_words):
		# encode the text as integer
		encoded = tokenizer.texts_to_sequences([in_text])[0]
		encoded = array(encoded)
		# predict a word in the vocabulary
		yhat = model.predict_classes(encoded, verbose=0)
		# map predicted word index to word
		out_word = ''
		for word, index in tokenizer.word_index.items():
			if index == yhat:
				out_word = word
				break
		# append to input
		in_text, result = out_word, result + ' ' + out_word
	return result

def createPredictionModel(data):
	# source text
	# integer encode text
	tokenizer = Tokenizer()
	tokenizer.fit_on_texts([data])
	encoded = tokenizer.texts_to_sequences([data])[0]
	# determine the vocabulary size
	vocab_size = len(tokenizer.word_index) + 1
	print('Vocabulary Size: %d' % vocab_size)
	# create word -> word sequences
	sequences = list()
	for i in range(1, len(encoded)):
		sequence = encoded[i-1:i+1]
		sequences.append(sequence)
	print('Total Sequences: %d' % len(sequences))
	# split into X and y elements
	sequences = array(sequences)
	X, y = sequences[:,0],sequences[:,1]
	# one hot encode outputs
	y = to_categorical(y, num_classes=vocab_size)
	# define model
	model = Sequential()
	model.add(Embedding(vocab_size, 10, input_length=1))
	model.add(LSTM(50))
	# IMPORTANT!!
	model.add(Dense(vocab_size, activation='softmax'))
	print(model.summary())
	plot_model(model, to_file='models/predict/predictor_plot.png', show_shapes=True, show_layer_names=True)
	# compile network
	model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
	# fit network
	model.fit(X, y, epochs=500, verbose=2)
	# serialize model to JSON
	model_json = model.to_json()
	with open("models/predict/predictor.json", "w") as json_file:
	    json_file.write(model_json)
	# serialize weights to HDF5
	model.save_weights("models/predict/model.h5")
	save_obj(tokenizer,'tokenizer')

def save_obj(obj, name):
    with open('models/predict/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open('models/predict/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def loadPredicitonModel():
	global path
	path = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])),'models/predict')

	if not os.path.exists(os.path.join(path,'predictor.json')):
	# source text
		data = """ Jack and Jill went up the hill\n
				 To fetch a pail of water\n
				 Jack fell down and broke his crown\n
				 And Jill came tumbling after\n """
		createPredictionModel(data)

	# load json and create model
	json_file = open('models/predict/predictor.json', 'r')
	loaded_model_json = json_file.read()
	json_file.close()
	model = model_from_json(loaded_model_json)
	# load weights into new model
	model.load_weights("models/predict/model.h5")
	tokenizer = load_obj('tokenizer')	
	return model, tokenizer

if __name__ == '__main__':
	model = loadPredicitonModel()

	print(generate_seq(model, 'Jack', 6))
	print(generate_seq(model, 'Jill', 6))