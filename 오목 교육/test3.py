from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import *
from keras.regularizers import L1L2
from keras.optimizers import *
from keras.callbacks import ModelCheckpoint, EarlyStopping
import keras
import copy
import keras.backend.tensorflow_backend as K

import os
import numpy as np

np.random.seed(7)
f = open("./새기보.txt","r")
X = []
Y = []
ap = False
for i in range(300):
	print(i)
	line = f.readline()

	if not line:break

	pan = [[0 for i in range(15)] for j in range(15)]
	
	last = 1

	words = line.split()

	for i in range(len(words)):
		if len(words)-1 == i and last == 1:
			break
		if last == 1:
			try:
				pan[ord(words[i][0])-97][int(words[i][1:])-1] = last
			except Exception:
				break
			last = 2
		else: 
			ap = False
			height = ord(words[i][0])-97
			width = int(words[i][1:])-1
			for h in range(15):
				for w in range(15):
					if pan[h][w] == 0:
						copypan = copy.deepcopy(pan)
						copypan[h][w] = last
						X.append(copypan)
						if h == height and w == width:
							Y.append(1)
						else:
							Y.append(0)
			pan[ord(words[i][0])-97][int(words[i][1:])-1] = last
			last = 1

f.close()

print(len(X))
print(len(Y))

with K.tf.device('/gpu:1'):
    X_train = np.array(X,dtype='uint8')
    Y_train = np.array(Y,dtype='uint8')
	
    X_train = X_train.reshape(X_train.shape[0],-1,225)

    X_train = X_train.astype('float32')/2

    Y_train = keras.utils.to_categorical(Y_train,2)

    model = Sequential()
    reg = L1L2(l1=0.2, l2=0.2)
    model.add(Bidirectional(GRU(units=256, input_shape=(-1,225), dropout=0.3, recurrent_regularizer=reg, activation='relu',
                                return_sequences=True)))
    model.add(BatchNormalization())
    model.add(Bidirectional(GRU(units=64, dropout=0.3, recurrent_regularizer=reg, activation='relu',
                                return_sequences=True)))
    model.add(BatchNormalization())
    model.add(Bidirectional(GRU(units=16, dropout=0.3, recurrent_regularizer=reg, activation='relu',
                                return_sequences=True)))
    model.add(BatchNormalization())
    model.add(Bidirectional(GRU(units=4, dropout=0.3, recurrent_regularizer=reg, activation='relu',
                                return_sequences=True)))
    model.add(BatchNormalization())
    model.add(Flatten())
    model.add(Dense(units=2))
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop',metrics=['accuracy'])
    checkpointer = ModelCheckpoint(filepath="omok_model.h5",monitor='val_loss',verbose = 1, save_best_only=True)
    early_stopping_callback = EarlyStopping(monitor='loss',patience=5)
    hist = model.fit(X_train, Y_train,
                 batch_size=6000,
                 epochs=13,
                 verbose=1, 
                 validation_split=0.2,
		 callbacks = [early_stopping_callback,checkpointer])
