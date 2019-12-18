from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPooling2D, Dropout, Flatten
from keras.callbacks import ModelCheckpoint, EarlyStopping
import keras
import copy
from keras.optimizers import*
import keras.backend.tensorflow_backend as K
from keras.models import load_model
import os
import numpy as np

np.random.seed(7)
f = open("./새기보.txt","r")
X = []
Y = []
ap = False

def Xvalueappend(Xpan):
    board_mat = np.array(Xpan)
    
    X.append(board_mat.tolist())
    X.append(np.rot90(board_mat).tolist())
    X.append(np.rot90(board_mat,2).tolist())
    X.append(np.rot90(board_mat,3).tolist())
    
    board_fliplr = np.fliplr(board_mat)
    board_flipud = np.flipud(board_mat)
    
    X.append(board_fliplr.tolist())
    X.append(np.rot90(board_fliplr).tolist())
    X.append(np.rot90(board_fliplr,2).tolist())
    X.append(np.rot90(board_fliplr,3).tolist())
    
    X.append(board_flipud.tolist())
    X.append(np.rot90(board_flipud).tolist())
    X.append(np.rot90(board_flipud,2).tolist())
    X.append(np.rot90(board_flipud,3).tolist())

def Yvalueappend(Ypan):	
    a = [0 for i in range(225)]
    a[Ypan] = 1
    board_mat = np.array(a)
    board_mat[Ypan] = 1
    
    board_mat = board_mat.reshape(15,15)
    
    Y.append(board_mat.reshape(225).tolist())
    Y.append(np.rot90(board_mat).reshape(225).tolist())
    Y.append(np.rot90(board_mat,2).reshape(225).tolist())
    Y.append(np.rot90(board_mat,3).reshape(225).tolist())
    
    board_fliplr = np.fliplr(board_mat)
    board_flipud = np.flipud(board_mat)
    
    Y.append(board_fliplr.reshape(225).tolist())
    Y.append(np.rot90(board_fliplr).reshape(225).tolist())
    Y.append(np.rot90(board_fliplr,2).reshape(225).tolist())
    Y.append(np.rot90(board_fliplr,3).reshape(225).tolist())
    
    Y.append(board_flipud.reshape(225).tolist())
    Y.append(np.rot90(board_flipud).reshape(225).tolist())
    Y.append(np.rot90(board_flipud,2).reshape(225).tolist())
    Y.append(np.rot90(board_flipud,3).reshape(225).tolist())

for i in range(8468):
	print(i)
	line = f.readline()

	if not line:break

	pan = [[0 for i in range(15)] for j in range(15)]
	
	last = 1

	words = line.split()
	if len(words) < 5: continue

	for i in range(len(words)):
		if len(words)-1 == i and last == 1:
			break
		try:
			pan[ord(words[i][0])-97][int(words[i][1:])-1] = last
		except Exception:
			break
		if last == 1:
			Xvalueappend(copy.deepcopy(pan))
			last = 2
		else: 
			last = 1
			Yvalueappend((ord(words[i][0])-97)*15+int(words[i][1:])-1)

f.close()

print(len(X))
print(len(Y))

with K.tf.device('/gpu:1'):
    X_train = np.array(X,dtype='uint8')
    Y_train = np.array(Y,dtype='uint8')

    input_shape = (15,15,1)

    X_train = X_train.reshape(X_train.shape[0],15,15,1)

    X_train = X_train.astype('float32')/2

    model = load_model('omok_model.h5')
    """model = Sequential()
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
    model.add(Dense(500, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(225, activation='softmax'))
    model.summary()
    model.compile(loss='categorical_crossentropy', optimizer='adam',metrics=['accuracy'])"""
    checkpointer = ModelCheckpoint(filepath="omok_model.h5",monitor='val_loss',verbose = 1, save_best_only=True)
    early_stopping_callback = EarlyStopping(monitor='loss',patience=5)
    hist = model.fit(X_train, Y_train,
                 batch_size=128,
                 epochs=5,
                 verbose=2, 
                 validation_split=0.2,
	     callbacks = [early_stopping_callback,checkpointer])
