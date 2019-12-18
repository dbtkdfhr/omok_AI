from keras.models import load_model
import numpy as np

model = load_model('./omok_model.h5')

x = [[0 for i in range(19)] for j in range(19)]

x[10][10] = 1

xhat = np.array(x)

xhat = xhat.reshape(1,19,19,1)
xhat = xhat.astype('float32') / 2

yhat = model.predict_classes(xhat)

x[yhat[0]//19][yhat[0]%19] = 2

for i in range(19):
    for j in range(19):
        print(x[i][j],end=" ")
    print()