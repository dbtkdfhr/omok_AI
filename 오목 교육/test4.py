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
import time

np.random.seed(7)

def victory_condition(omok_pan):
    cont = 0
    
    for i in range(15):
        for j in range(15):
            if omok_pan[i][j] == 0:
                cont += 1
                
    if cont == 0:
        print("무승부 입니다.")
        return 1
            
    for i in range(11):
        for j in range(11):
            last = omok_pan[i][j]
            cnt = 1
            for z in range(1, 5):
                if omok_pan[i + z][j + z] == last and omok_pan[i + z][j + z] != 0:
                    cnt += 1
                else:
                    break

            if cnt == 5:
                if last == 1:
                    print("흑돌 승리")
                    return 2
                elif last == 2:
                    print("백돌 승리")
                    return 3

    for i in range(4,15):
        for j in range(11):
            last = omok_pan[i][j]
            cnt = 1
            for z in range(1, 5):
                if omok_pan[i - z][j + z] == last and omok_pan[i - z][j + z] != 0:
                    cnt += 1
                else:
                    break

            if cnt == 5:
                if last == 1:
                    print("흑돌 승리")
                    return 2
                elif last == 2:
                    print("백돌 승리")
                    return 3
                    
    for i in range(15):
        for j in range(11):
            last = omok_pan[i][j]
            cnt = 1
            for z in range(1, 5):
                if omok_pan[i][j + z] == last and omok_pan[i][j + z] != 0:
                    cnt += 1
                else:
                    break

            if cnt == 5:
                if last == 1:
                    print("흑돌 승리")
                    return 2
                elif last == 2:
                    print("백돌 승리")
                    return 3

    for i in range(11):
        for j in range(15):
            last = omok_pan[i][j]
            cnt = 1
            for z in range(1, 5):
                if omok_pan[i + z][j] == last and omok_pan[i + z][j] != 0:
                    cnt += 1
                else:
                    break

            if cnt == 5:
                if last == 1:
                    print("흑돌 승리")
                    return 2
                elif last == 2:
                    print("백돌 승리")
                    return 3

    return 0
    
def draw(pan):    
    for i in range(15):
        for j in range(15):
            if pan[i][j] == 1:
                print('o',end = ' ')
            elif pan[i][j] == 2:
                print('x',end = ' ')
            else:
                print('.',end = ' ')
        print()
    time.sleep(0.1)    
    
def findMaxIndex(lst):
    a = lst.index(max(lst))
    return (a//15,a%15)    
    
def move_select(model,pan,change=False):
    if not change:
        q = copy.deepcopy(pan)

        xhat = np.array(q)

        xhat = xhat.reshape(1,15,15,1)
        xhat = xhat.astype('float32')/2
        yhat = model.predict(xhat)
        predict = yhat[0].tolist()

        for i in range(15):
            for j in range(15):
                if pan[i][j] != 0: predict[i*15+j] = 0

        y, x = findMaxIndex(predict)
        return (y,x)
    else:
        q = copy.deepcopy(pan)

        xhat = np.array(q)
        
        xhat[xhat == 1] = 3
        xhat[xhat == 2] = 1
        xhat[xhat == 3] = 2
        
        xhat = xhat.reshape(1,15,15,1)
        xhat = xhat.astype('float32')/2
        yhat = model.predict(xhat)
        predict = yhat[0].tolist()

        for i in range(15):
            for j in range(15):
                if pan[i][j] != 0: predict[i*15+j] = 0

        y, x = findMaxIndex(predict)
        return (y,x)
    
def train(model):
    omok_pan = [[0 for i in range(15)] for j in range(15)]
    omok_pan[7][7] = 1
    pan_list = []
    where_list = []
    cond = 0
    
    #draw(omok_pan)
    while True:
        y,x = move_select(model,omok_pan)
        omok_pan[y][x] = 2
        pan_list.append(copy.deepcopy(omok_pan))
        where_list.append(y*15+x)
        
        cond = victory_condition(omok_pan)
        #draw(omok_pan)
        if cond >= 1:
            break
        
        y,x = move_select(model,omok_pan,True)
        omok_pan[y][x] = 1
        #draw(omok_pan)
        if cond >= 1:
            break
    
    x1 = np.array(copy.deepcopy(pan_list),dtype='uint8')
    y1 = np.array(copy.deepcopy(where_list),dtype='uint8')
    y1 = keras.utils.to_categorical(y1,225)
    if cond == 2:
        x1[x1 == 1] = 3
        x1[x1 == 2] = 1
        x1[x1 == 3] = 2
    
    def unison_shuffled_copies(a, b):
        assert len(a) == len(b)
        p = np.random.permutation(len(a))
        return a[p], b[p]

    x1, y1 = unison_shuffled_copies(x1, y1)
    print(y1.shape)
    x1 = x1.reshape(x1.shape[0],15,15,1)
    print(y1.shape)
    
    model.fit(x1,y1,batch_size = 1, epochs = 1,verbose=2)
    return model

with K.tf.device('/gpu:1'):
    model = load_model('omok_AI.h5')
    #model.compile(loss='mean_squared_error', optimizer=Adadelta())
    for i in range(20000):
        print(i+1,"번째 게임")
        model = train(model)
        
    model.save('omok_AI.h5')
