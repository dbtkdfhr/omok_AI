from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPooling2D, Dropout, Flatten
from keras.callbacks import ModelCheckpoint, EarlyStopping
import keras
import copy
from keras.optimizers import*
import keras.backend.tensorflow_backend as K
from keras.callbacks import ModelCheckpoint, EarlyStopping

import os
import numpy as np

np.random.seed(7)

f = open("./새기보.txt","r")
X = []
Y = []
ap = False
for i in range(500):
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

	input_shape = (15,15,1)
	
	X_train = X_train.reshape(X_train.shape[0],15,15,1)

	X_train = X_train.astype('float32')/2

	Y_train = keras.utils.to_categorical(Y_train,2)

	model = Sequential()
	model.add(Conv2D(64, kernel_size=(7, 7),
		 strides=(1,1),
		 padding='same',
                 activation='relu',
                 input_shape=input_shape))
	model.add(Dropout(0.25))
	#model.add(MaxPooling2D(pool_size=(2,2),strides=(2,2)))
	model.add(Conv2D(32, kernel_size = (5, 5),strides=(1,1), activation='relu',padding='same'))
	model.add(Dropout(0.25))
	model.add(Conv2D(32, kernel_size = (3, 3),strides=(1,1), activation='relu',padding='same'))
	model.add(Dropout(0.25))
	model.add(Conv2D(32, kernel_size = (3, 3),strides=(1,1), activation='relu',padding='same'))
	model.add(Dropout(0.25))
	model.add(Conv2D(32, kernel_size = (3, 3),strides=(1,1), activation='relu',padding='same'))
	model.add(Dropout(0.25))
	model.add(Conv2D(32, kernel_size = (3, 3),strides=(1,1), activation='relu',padding='same'))
	model.add(Dropout(0.25))
	model.add(Conv2D(32, kernel_size = (3, 3),strides=(1,1), activation='relu',padding='same'))
	model.add(Dropout(0.25))
	model.add(Conv2D(32, kernel_size = (3, 3),strides=(1,1), activation='relu',padding='same'))
	model.add(Dropout(0.25))
	model.add(Conv2D(32, kernel_size = (3, 3),strides=(1,1), activation='relu',padding='same'))
	#model.add(MaxPooling2D(pool_size=(2,2)))
	model.add(Dropout(0.25))
	model.add(Flatten())
	model.add(Dense(100, activation='relu'))
	model.add(Dropout(0.5))
	model.add(Dense(2, activation='softmax'))
	model.summary()
	model.compile(loss='categorical_crossentropy', optimizer='adam',metrics=['accuracy'])
	checkpointer = ModelCheckpoint(filepath="omok_model.h5",monitor='loss',verbose = 2, save_best_only=True)
	early_stopping_callback = EarlyStopping(monitor='loss',patience=5)
	hist = model.fit(X_train, Y_train,
                 batch_size=225,
                 epochs=15,
                 verbose=2, 
                 validation_split=0.1,
		 callbacks = [early_stopping_callback,checkpointer])
