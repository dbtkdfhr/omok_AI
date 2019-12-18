from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
from PyQt5 import QtCore

from keras.models import load_model
import numpy as np

import copy

class Main(QMainWindow):
    def __init__(self):
        super().__init__()

        self.model = load_model('./omok_AI.h5')
        self.Finish = False
        self.omok_pan = [[0 for i in range(15)] for j in range(15)]
        self.omok_pan[7][7] = 1
        self.order = False
        self.setMouseTracking(True)

        """oImage = QImage("./plate.png")
        sImage = oImage.scaled(760,620)
        palette = QPalette()
        palette.setBrush(10,QBrush(sImage))
        self.setPalette(palette)"""

        self.setWindowTitle('Omok_AI')
        self.resize(600, 600)
        self.omok_AI()
        self.show()
        self.draw()

    def paintEvent(self,event):
        painter = QPainter(self)
        pen = QPen(Qt.black,3)
        painter.setPen(pen)
        for i in range(15):
            painter.drawLine(20,20 + i*40,580,20 + i*40)
            
        for i in range(15):
            painter.drawLine(20 + i*40,20,20 + i*40,580)

    def weight_AI(self,y,x):

        pan_weight = [[0 for i in range(15)] for j in range(15)]
        pan = copy.deepcopy(self.omok_pan)
        pan[y][x] = 1

        for i in range(1, 12):
            for j in range(15):
                if pan[i][j] == pan[i + 1][j] == pan[i + 2][j] == pan[i + 3][
                    j] == 1 and pan[i - 1][j] == 0:
                    pan_weight[i-1][j] += 100

        for i in range(11):
            for j in range(15):
                if pan[i][j] == pan[i + 1][j] == pan[i + 2][j] == pan[i + 3][
                    j] == 1 and pan[i + 4][j] == 0:
                    pan_weight[i+4][j] += 100

        for i in range(15):
            for j in range(1, 12):
                if pan[i][j] == pan[i][j + 1] == pan[i][j + 2] == pan[i][
                    j + 3] == 1 and pan[i][j - 1] == 0:
                    pan_weight[i][j-1] += 100

        for i in range(15):
            for j in range(11):
                if pan[i][j] == pan[i][j + 1] == pan[i][j + 2] == pan[i][
                    j + 3] == 1 and pan[i][j + 4] == 0:
                    pan_weight[i][j+4] += 100

        for i in range(1, 12):
            for j in range(1, 12):
                if pan[i][j] == pan[i + 1][j + 1] == pan[i + 2][j + 2] == \
                        pan[i + 3][j + 3] == 1 and pan[i - 1][j - 1] == 0:
                    pan_weight[i-1][j-1] += 100

        for i in range(11):
            for j in range(11):
                if pan[i][j] == pan[i + 1][j + 1] == pan[i + 2][j + 2] == \
                        pan[i + 3][j + 3] == 1 and pan[i + 4][j + 4] == 0:
                    pan_weight[i+4][j+4] += 100

        for i in range(3, 14):
            for j in range(12):
                if pan[i][j] == pan[i - 1][j + 1] == pan[i - 2][j + 2] == \
                        pan[i - 3][j + 3] == 1 and pan[i + 1][j - 1] == 0:
                    pan_weight[i+1][j-1] += 100

        for i in range(4, 15):
            for j in range(11):
                if pan[i][j] == pan[i - 1][j + 1] == pan[i - 2][j + 2] == \
                        pan[i - 3][j + 3] == 1 and pan[i - 4][j + 4] == 0:
                    pan_weight[i-4][j+4] += 100

        # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        for i in range(11):
            for j in range(15):
                if pan[i][j] == pan[i + 1][j] == pan[i + 2][j] == pan[i + 4][
                    j] == 1 and pan[i + 3][j] == 0:
                    pan_weight[i + 3][j] += 100

        for i in range(15):
            for j in range(11):
                if pan[i][j] == pan[i][j + 1] == pan[i][j + 2] == pan[i][
                    j + 4] == 1 and pan[i][j + 3] == 0:
                    pan_weight[i][j + 3] += 100

        for i in range(11):
            for j in range(11):
                if pan[i][j] == pan[i + 1][j + 1] == pan[i + 2][j + 2] == \
                        pan[i + 4][j + 4] == 1 and pan[i + 3][j + 3] == 0:
                    pan_weight[i + 3][j + 3] += 100

        for i in range(4, 15):
            for j in range(11):
                if pan[i][j] == pan[i - 1][j + 1] == pan[i - 2][j + 2] == \
                        pan[i - 4][j + 4] == 1 and pan[i - 3][j + 3] == 0:
                    pan_weight[i - 3][j + 3] += 100

        # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        for i in range(11):
            for j in range(15):
                if pan[i][j] == pan[i + 1][j] == pan[i + 3][j] == \
                        pan[i + 4][j] == 1 and pan[i + 2][j] == 0:
                    pan_weight[i + 2][j] += 100

        for i in range(15):
            for j in range(11):
                if pan[i][j] == pan[i][j + 1] == pan[i][j + 3] == \
                        pan[i][j + 4] == 1 and pan[i][j + 2] == 0:
                    pan_weight[i][j + 2] += 100

        for i in range(11):
            for j in range(11):
                if pan[i][j] == pan[i + 1][j + 1] == pan[i + 3][j + 3] == \
                        pan[i + 4][j + 4] == 1 and pan[i + 2][j + 2] == 0:
                    pan_weight[i + 2][j + 2] += 100

        for i in range(4, 15):
            for j in range(11):
                if pan[i][j] == pan[i - 1][j + 1] == pan[i - 3][j + 3] == \
                        pan[i - 4][j + 4] == 1 and pan[i - 2][j + 2] == 0:
                    pan_weight[i - 2][j + 2] += 100

        # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        for i in range(11):
            for j in range(15):
                if pan[i][j] == pan[i + 2][j] == pan[i + 3][j] == \
                        pan[i + 4][j] == 1 and pan[i + 1][j] == 0:
                    pan_weight[i + 1][j] += 100

        for i in range(15):
            for j in range(11):
                if pan[i][j] == pan[i][j + 2] == pan[i][j + 3] == \
                        pan[i][j + 4] == 1 and pan[i][j + 1] == 0:
                    pan_weight[i][j + 1] += 100

        for i in range(11):
            for j in range(11):
                if pan[i][j] == pan[i + 2][j + 2] == pan[i + 3][j + 3] == \
                        pan[i + 4][j + 4] == 1 and pan[i + 1][j + 1] == 0:
                    pan_weight[i + 1][j + 1] += 100

        for i in range(4, 15):
            for j in range(11):
                if pan[i][j] == pan[i - 2][j + 2] == pan[i - 3][j + 3] == \
                        pan[i - 4][j + 4] == 1 and pan[i - 1][j + 1] == 0:
                    pan_weight[i - 1][j + 1] += 100

        # --------------------------------------------------------------------------------------------------------------------------------

        for i in range(11):
            for j in range(15):
                if pan[i][j] == pan[i + 4][j] == 0 and pan[i + 1][j] == \
                        pan[i + 2][j] == pan[i + 3][j] == 1:
                    pan_weight[i][j] += 30
                    pan_weight[i + 4][j] += 30

        for i in range(15):
            for j in range(11):
                if pan[i][j] == pan[i][j + 4] == 0 and pan[i][j + 1] == pan[i][
                    j + 2] == pan[i][j + 3] == 1:
                    pan_weight[i][j] += 30
                    pan_weight[i][j + 4] += 30

        for i in range(11):
            for j in range(11):
                if pan[i][j] == pan[i + 4][j + 4] == 0 and pan[i + 1][j + 1] == \
                        pan[i + 2][j + 2] == pan[i + 3][j + 3] == 1:
                    pan_weight[i][j] += 30
                    pan_weight[i + 4][j + 4] += 30

        for i in range(4, 15):
            for j in range(11):
                if pan[i][j] == pan[i - 4][j + 4] == 0 and pan[i - 1][j + 1] == \
                        pan[i - 2][j + 2] == pan[i - 3][j + 3] == 1:
                    pan_weight[i][j] += 30
                    pan_weight[i - 4][j + 4] += 30

        # ------------------------------------------------------------------------------------------------------------

        for i in range(10):
            for j in range(15):
                if pan[i][j] == pan[i + 3][j] == pan[i + 5][j] == 0 and \
                        pan[i + 1][j] == \
                        pan[i + 2][j] == pan[i + 4][j] == 1:
                    pan_weight[i + 3][j] += 30
                    pan_weight[i][j] += 20
                    pan_weight[i + 5][j] += 20

        for i in range(15):
            for j in range(10):
                if pan[i][j] == pan[i][j + 3] == pan[i][j + 5] == 0 and pan[i][
                    j + 1] == \
                        pan[i][j + 2] == pan[i][j + 4] == 1:
                    pan_weight[i][j + 3] += 30
                    pan_weight[i][j] += 20
                    pan_weight[i][j + 5] += 20

        for i in range(10):
            for j in range(10):
                if pan[i][j] == pan[i + 3][j + 3] == pan[i + 5][j + 5] == 0 and \
                        pan[i + 1][j + 1] == \
                        pan[i + 2][j + 2] == pan[i + 4][j + 4] == 1:
                    pan_weight[i + 3][j + 3] += 30
                    pan_weight[i][j] += 20
                    pan_weight[i + 5][j + 5] += 20

        for i in range(5, 15):
            for j in range(10):
                if pan[i][j] == pan[i - 3][j + 3] == pan[i - 5][j + 5] == 0 and \
                        pan[i - 1][j + 1] == \
                        pan[i - 2][j + 2] == pan[i - 4][j + 4] == 1:
                    pan_weight[i - 3][j + 3] += 30
                    pan_weight[i][j] += 20
                    pan_weight[i - 5][j + 5] += 20

        # ------------------------------------------------------------------------------------------------------------

        for i in range(10):
            for j in range(15):
                if pan[i][j] == pan[i + 2][j] == pan[i + 5][j] == 0 and \
                        pan[i + 1][j] == \
                        pan[i + 3][j] == pan[i + 4][j] == 1:
                    pan_weight[i + 2][j] += 30
                    pan_weight[i][j] += 20
                    pan_weight[i + 5][j] += 20

        for i in range(15):
            for j in range(10):
                if pan[i][j] == pan[i][j + 2] == pan[i][j + 5] == 0 and \
                        pan[i][j + 1] == \
                        pan[i][j + 3] == pan[i][j + 4] == 1:
                    pan_weight[i][j + 2] += 30
                    pan_weight[i][j] += 20
                    pan_weight[i][j + 5] += 20

        for i in range(10):
            for j in range(10):
                if pan[i][j] == pan[i + 2][j + 2] == pan[i + 5][j + 5] == 0 and \
                        pan[i + 1][j + 1] == \
                        pan[i + 3][j + 3] == pan[i + 4][j + 4] == 1:
                    pan_weight[i + 2][j + 2] += 30
                    pan_weight[i][j] += 20
                    pan_weight[i + 5][j + 5] += 20

        for i in range(5, 15):
            for j in range(10):
                if pan[i][j] == pan[i - 2][j + 2] == pan[i - 5][j + 5] == 0 and \
                        pan[i - 1][j + 1] == \
                        pan[i - 3][j + 3] == pan[i - 4][j + 4] == 1:
                    pan_weight[i - 2][j + 2] += 30
                    pan_weight[i][j] += 20
                    pan_weight[i - 5][j + 5] += 20

        # --------------------------------------------------------------------------------------------------

        for i in range(12):
            for j in range(15):
                if pan[i][j] == pan[i + 3][j] == 0 and pan[i + 1][j] == \
                        pan[i + 2][j] == 1:
                    pan_weight[i][j] += 5
                    pan_weight[i + 3][j] += 5

        for i in range(15):
            for j in range(12):
                if pan[i][j] == pan[i][j + 3] == 0 and pan[i][j + 1] == pan[i][
                    j + 2] == 1:
                    pan_weight[i][j] += 5
                    pan_weight[i][j + 3] += 5

        for i in range(12):
            for j in range(12):
                if pan[i][j] == pan[i + 3][j + 3] == 0 and pan[i + 1][j + 1] == \
                        pan[i + 2][j + 2] == 1:
                    pan_weight[i][j] += 5
                    pan_weight[i + 3][j + 3] += 5

        for i in range(3, 15):
            for j in range(12):
                if pan[i][j] == pan[i - 3][j + 3] == 0 and pan[i - 1][j + 1] == \
                        pan[i - 2][j + 2] == 1:
                    pan_weight[i][j] += 5
                    pan_weight[i - 4][j + 4] += 5

        # ------------------------------------------------------------------------------------------------------------

        for i in range(11):
            for j in range(15):
                if pan[i][j] == pan[i + 2][j] == pan[i + 4][j] == 0 and \
                        pan[i + 1][j] == \
                        pan[i + 3][j] == 1:
                    pan_weight[i + 2][j] += 5
                    pan_weight[i][j] += 5
                    pan_weight[i + 4][j] += 5

        for i in range(15):
            for j in range(11):
                if pan[i][j] == pan[i][j + 2] == pan[i][j + 4] == 0 and pan[i][
                    j + 1] == \
                        pan[i][j + 3] == 1:
                    pan_weight[i][j + 2] += 5
                    pan_weight[i][j] += 5
                    pan_weight[i][j + 4] += 5

        for i in range(11):
            for j in range(11):
                if pan[i][j] == pan[i + 2][j + 2] == pan[i + 4][j + 4] == 0 and \
                        pan[i + 1][j + 1] == \
                        pan[i + 3][j + 3] == 1:
                    pan_weight[i + 2][j + 2] += 5
                    pan_weight[i][j] += 5
                    pan_weight[i + 4][j + 4] += 5

        for i in range(4, 15):
            for j in range(11):
                if pan[i][j] == pan[i - 2][j + 2] == pan[i - 4][j + 4] == 0 and \
                        pan[i - 1][j + 1] == \
                        pan[i - 3][j + 3] == 1:
                    pan_weight[i - 2][j + 2] += 5
                    pan_weight[i][j] += 5
                    pan_weight[i - 4][j + 4] += 5

        for i in range(15):
            for j in range(15):
                if pan[i][j] == 1:
                    if i == 0 and j == 0:
                        if pan[i + 1][j + 1] == 0:
                            pan_weight[i + 1][j + 1] += 1
                        if pan[i][j + 1] == 0:
                            pan_weight[i][j + 1] += 1
                        if pan[i + 1][j] == 0:
                            pan_weight[i + 1][j] += 1
                    elif i == 0:
                        try:
                            if pan[i + 1][j + 1] == 0:
                                pan_weight[i + 1][j + 1] += 1
                        except Exception:
                            pass
                        try:
                            if pan[i][j + 1] == 0:
                                pan_weight[i][j + 1] += 1
                        except Exception:
                            pass
                        if pan[i + 1][j] == 0:
                            pan_weight[i + 1][j] += 1
                        if pan[i + 1][j - 1] == 0:
                            pan_weight[i + 1][j - 1] += 1
                        if pan[i][j - 1] == 0:
                            pan_weight[i][j - 1] += 1
                    elif j == 0:
                        try:
                            if pan[i + 1][j + 1] == 0:
                                pan_weight[i + 1][j + 1] += 1
                        except Exception:
                            pass
                        if pan[i][j + 1] == 0:
                            pan_weight[i][j + 1] += 1
                        try:
                            if pan[i + 1][j] == 0:
                                pan_weight[i + 1][j] += 1
                        except Exception:
                            pass
                        if pan[i - 1][j] == 0:
                            pan_weight[i - 1][j] += 1
                        if pan[i - 1][j - 1] == 0:
                            pan_weight[i - 1][j - 1] += 1
                    else:
                        try:
                            if pan[i - 1][j - 1] == 0:
                                pan_weight[i - 1][j - 1] += 1
                        except Exception:
                            pass

                        try:
                            if pan[i - 1][j] == 0:
                                pan_weight[i - 1][j] += 1
                        except Exception:
                            pass

                        try:
                            if pan[i - 1][j + 1] == 0:
                                pan_weight[i - 1][j + 1] += 1
                        except Exception:
                            pass

                        try:
                            if pan[i][j - 1] == 0:
                                pan_weight[i][j - 1] += 1
                        except Exception:
                            pass

                        try:
                            if pan[i][j + 1] == 0:
                                pan_weight[i][j + 1] += 1
                        except Exception:
                            pass

                        try:
                            if pan[i + 1][j - 1] == 0:
                                pan_weight[i + 1][j - 1] += 1
                        except Exception:
                            pass

                        try:
                            if pan[i + 1][j] == 0:
                                pan_weight[i + 1][j] += 1
                        except Exception:
                            pass

                        try:
                            if pan[i + 1][j + 1] == 0:
                                pan_weight[i + 1][j + 1] += 1
                        except Exception:
                            pass

        weightmax = sum(map(sum, pan_weight))

        return weightmax


    def omok_AI(self):


        #--------------------------------------------- 백 공격 -------------------------------------------------------

        for i in range(1,12):
            for j in range(15):
                if self.omok_pan[i][j] == self.omok_pan[i+1][j] == self.omok_pan[i+2][j] == self.omok_pan[i+3][j] == 2 and self.omok_pan[i - 1][j] == 0:
                    self.omok_pan[i-1][j] = 2
                    return

        for i in range(11):
            for j in range(15):
                if self.omok_pan[i][j] == self.omok_pan[i+1][j] == self.omok_pan[i+2][j] == self.omok_pan[i+3][j] == 2 and self.omok_pan[i + 4][j] == 0:
                    self.omok_pan[i+4][j] = 2
                    return

        for i in range(15):
            for j in range(1,12):
                if self.omok_pan[i][j] == self.omok_pan[i][j+1] == self.omok_pan[i][j+2] == self.omok_pan[i][j+3] == 2 and self.omok_pan[i][j-1] == 0:
                    self.omok_pan[i][j-1] = 2
                    return

        for i in range(15):
            for j in range(11):
                if self.omok_pan[i][j] == self.omok_pan[i][j+1] == self.omok_pan[i][j+2] == self.omok_pan[i][j+3] == 2 and self.omok_pan[i][j+4] == 0:
                    self.omok_pan[i][j+4] = 2
                    return

        for i in range(1,12):
            for j in range(1,12):
                if self.omok_pan[i][j] == self.omok_pan[i+1][j+1] == self.omok_pan[i+2][j+2] == self.omok_pan[i+3][j+3] == 2 and self.omok_pan[i - 1][j - 1] == 0:
                    self.omok_pan[i-1][j - 1] = 2
                    return

        for i in range(11):
            for j in range(11):
                if self.omok_pan[i][j] == self.omok_pan[i+1][j+1] == self.omok_pan[i+2][j+2] == self.omok_pan[i+3][j+3] == 2 and self.omok_pan[i+4][j+4] == 0:
                    self.omok_pan[i+4][j+4] = 2
                    return

        for i in range(3,14):
            for j in range(12):
                if self.omok_pan[i][j] == self.omok_pan[i - 1][j + 1] == self.omok_pan[i - 2][j + 2] == self.omok_pan[i - 3][j + 3] == 2 and self.omok_pan[i + 1][j - 1] == 0:
                    self.omok_pan[i + 1][j - 1] = 2
                    return

        for i in range(4, 15):
            for j in range(11):
                if self.omok_pan[i][j] == self.omok_pan[i - 1][j + 1] == self.omok_pan[i - 2][j + 2] == self.omok_pan[i - 3][j + 3] == 2 and self.omok_pan[i - 4][j + 4] == 0:
                    self.omok_pan[i - 4][j + 4] = 2
                    return


        #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------


        for i in range(11):
            for j in range(15):
                if self.omok_pan[i][j] == self.omok_pan[i+1][j] == self.omok_pan[i+2][j] == self.omok_pan[i+4][j] == 2 and self.omok_pan[i+3][j] == 0:
                    self.omok_pan[i+3][j] = 2
                    return

        for i in range(15):
            for j in range(11):
                if self.omok_pan[i][j] == self.omok_pan[i][j+1] == self.omok_pan[i][j+2] == self.omok_pan[i][j+4] == 2 and self.omok_pan[i][j+3] == 0:
                    self.omok_pan[i][j+3] = 2
                    return

        for i in range(11):
            for j in range(11):
                if self.omok_pan[i][j] == self.omok_pan[i+1][j+1] == self.omok_pan[i+2][j+2] == self.omok_pan[i+4][j+4] == 2 and self.omok_pan[i+3][j+3] == 0:
                    self.omok_pan[i+3][j+3] = 2
                    return

        for i in range(4,15):
            for j in range(11):
                if self.omok_pan[i][j] == self.omok_pan[i-1][j+1] == self.omok_pan[i-2][j+2] == self.omok_pan[i-4][j+4] == 2 and self.omok_pan[i-3][j+3] == 0:
                    self.omok_pan[i-3][j+3] = 2
                    return



        # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------



        for i in range(11):
            for j in range(15):
                if self.omok_pan[i][j] == self.omok_pan[i + 1][j] == self.omok_pan[i + 3][j] == \
                        self.omok_pan[i + 4][j] == 2 and self.omok_pan[i + 2][j] == 0:
                    self.omok_pan[i + 2][j] = 2
                    return

        for i in range(15):
            for j in range(11):
                if self.omok_pan[i][j] == self.omok_pan[i][j + 1] == self.omok_pan[i][j + 3] == \
                        self.omok_pan[i][j + 4] == 2 and self.omok_pan[i][j + 2] == 0:
                    self.omok_pan[i][j + 2] = 2
                    return

        for i in range(11):
            for j in range(11):
                if self.omok_pan[i][j] == self.omok_pan[i + 1][j + 1] == self.omok_pan[i + 3][j + 3] == \
                        self.omok_pan[i + 4][j + 4] == 2 and self.omok_pan[i + 2][j + 2] == 0:
                    self.omok_pan[i + 2][j + 2] = 2
                    return

        for i in range(4, 15):
            for j in range(11):
                if self.omok_pan[i][j] == self.omok_pan[i - 1][j + 1] == self.omok_pan[i - 3][j + 3] == \
                        self.omok_pan[i - 4][j + 4] == 2 and self.omok_pan[i - 2][j + 2] == 0:
                    self.omok_pan[i - 2][j + 2] = 2
                    return



        # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------



        for i in range(11):
            for j in range(15):
                if self.omok_pan[i][j] == self.omok_pan[i + 2][j] == self.omok_pan[i + 3][j] == \
                        self.omok_pan[i + 4][j] == 2 and self.omok_pan[i + 1][j] == 0:
                    self.omok_pan[i + 1][j] = 2
                    return

        for i in range(15):
            for j in range(11):
                if self.omok_pan[i][j] == self.omok_pan[i][j + 2] == self.omok_pan[i][j + 3] == \
                        self.omok_pan[i][j + 4] == 2 and self.omok_pan[i][j + 1] == 0:
                    self.omok_pan[i][j + 1] = 2
                    return

        for i in range(11):
            for j in range(11):
                if self.omok_pan[i][j] == self.omok_pan[i + 2][j + 2] == self.omok_pan[i + 3][j + 3] == \
                        self.omok_pan[i + 4][j + 4] == 2 and self.omok_pan[i + 1][j + 1] == 0:
                    self.omok_pan[i + 1][j + 1] = 2
                    return

        for i in range(4, 15):
            for j in range(11):
                if self.omok_pan[i][j] == self.omok_pan[i - 2][j + 2] == self.omok_pan[i - 3][j + 3] == \
                        self.omok_pan[i - 4][j + 4] == 2 and self.omok_pan[i - 1][j + 1] == 0:
                    self.omok_pan[i - 1][j + 1] = 2
                    return



        #------------------------------------ 흑 막기 -----------------------------------------------

        for i in range(1,12):
            for j in range(15):
                if self.omok_pan[i][j] == self.omok_pan[i + 1][j] == self.omok_pan[i + 2][j] == self.omok_pan[i + 3][
                    j] == 1 and self.omok_pan[i - 1][j] == 0:
                    self.omok_pan[i - 1][j] = 2
                    return

        for i in range(11):
            for j in range(15):
                if self.omok_pan[i][j] == self.omok_pan[i + 1][j] == self.omok_pan[i + 2][j] == self.omok_pan[i + 3][
                    j] == 1 and self.omok_pan[i + 4][j] == 0:
                    self.omok_pan[i + 4][j] = 2
                    return

        for i in range(15):
            for j in range(1,12):
                if self.omok_pan[i][j] == self.omok_pan[i][j + 1] == self.omok_pan[i][j + 2] == self.omok_pan[i][
                    j + 3] == 1 and self.omok_pan[i][j - 1] == 0:
                    self.omok_pan[i][j - 1] = 2
                    return

        for i in range(15):
            for j in range(11):
                if self.omok_pan[i][j] == self.omok_pan[i][j + 1] == self.omok_pan[i][j + 2] == self.omok_pan[i][
                    j + 3] == 1 and self.omok_pan[i][j + 4] == 0:
                    self.omok_pan[i][j + 4] = 2
                    return

        for i in range(1,12):
            for j in range(1,12):
                if self.omok_pan[i][j] == self.omok_pan[i + 1][j + 1] == self.omok_pan[i + 2][j + 2] == \
                        self.omok_pan[i + 3][j + 3] == 1 and self.omok_pan[i - 1][j - 1] == 0:
                    self.omok_pan[i - 1][j - 1] = 2
                    return

        for i in range(11):
            for j in range(11):
                if self.omok_pan[i][j] == self.omok_pan[i + 1][j + 1] == self.omok_pan[i + 2][j + 2] == \
                        self.omok_pan[i + 3][j + 3] == 1 and self.omok_pan[i + 4][j + 4] == 0:
                    self.omok_pan[i + 4][j + 4] = 2
                    return

        for i in range(3, 14):
            for j in range(12):
                if self.omok_pan[i][j] == self.omok_pan[i - 1][j + 1] == self.omok_pan[i - 2][j + 2] == \
                        self.omok_pan[i - 3][j + 3] == 1 and self.omok_pan[i + 1][j - 1] == 0:
                    self.omok_pan[i + 1][j - 1] = 2
                    return

        for i in range(4, 15):
            for j in range(11):
                if self.omok_pan[i][j] == self.omok_pan[i - 1][j + 1] == self.omok_pan[i - 2][j + 2] == \
                        self.omok_pan[i - 3][j + 3] == 1 and self.omok_pan[i - 4][j + 4] == 0:
                    self.omok_pan[i - 4][j + 4] = 2
                    return

        # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        for i in range(11):
            for j in range(15):
                if self.omok_pan[i][j] == self.omok_pan[i + 1][j] == self.omok_pan[i + 2][j] == self.omok_pan[i + 4][
                    j] == 1 and self.omok_pan[i + 3][j] == 0:
                    self.omok_pan[i + 3][j] = 2
                    return

        for i in range(15):
            for j in range(11):
                if self.omok_pan[i][j] == self.omok_pan[i][j + 1] == self.omok_pan[i][j + 2] == self.omok_pan[i][
                    j + 4] == 1 and self.omok_pan[i][j + 3] == 0:
                    self.omok_pan[i][j + 3] = 2
                    return

        for i in range(11):
            for j in range(11):
                if self.omok_pan[i][j] == self.omok_pan[i + 1][j + 1] == self.omok_pan[i + 2][j + 2] == \
                        self.omok_pan[i + 4][j + 4] == 1 and self.omok_pan[i + 3][j + 3] == 0:
                    self.omok_pan[i + 3][j + 3] = 2
                    return

        for i in range(4, 15):
            for j in range(11):
                if self.omok_pan[i][j] == self.omok_pan[i - 1][j + 1] == self.omok_pan[i - 2][j + 2] == \
                        self.omok_pan[i - 4][j + 4] == 1 and self.omok_pan[i - 3][j + 3] == 0:
                    self.omok_pan[i - 3][j + 3] = 2
                    return

        # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        for i in range(11):
            for j in range(15):
                if self.omok_pan[i][j] == self.omok_pan[i + 1][j] == self.omok_pan[i + 3][j] == \
                        self.omok_pan[i + 4][j] == 1 and self.omok_pan[i + 2][j] == 0:
                    self.omok_pan[i + 2][j] = 2
                    return

        for i in range(15):
            for j in range(11):
                if self.omok_pan[i][j] == self.omok_pan[i][j + 1] == self.omok_pan[i][j + 3] == \
                        self.omok_pan[i][j + 4] == 1 and self.omok_pan[i][j + 2] == 0:
                    self.omok_pan[i][j + 2] = 2
                    return

        for i in range(11):
            for j in range(11):
                if self.omok_pan[i][j] == self.omok_pan[i + 1][j + 1] == self.omok_pan[i + 3][j + 3] == \
                        self.omok_pan[i + 4][j + 4] == 1 and self.omok_pan[i + 2][j + 2] == 0:
                    self.omok_pan[i + 2][j + 2] = 2
                    return

        for i in range(4, 15):
            for j in range(11):
                if self.omok_pan[i][j] == self.omok_pan[i - 1][j + 1] == self.omok_pan[i - 3][j + 3] == \
                        self.omok_pan[i - 4][j + 4] == 1 and self.omok_pan[i - 2][j + 2] == 0:
                    self.omok_pan[i - 2][j + 2] = 2
                    return

        # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        for i in range(11):
            for j in range(15):
                if self.omok_pan[i][j] == self.omok_pan[i + 2][j] == self.omok_pan[i + 3][j] == \
                        self.omok_pan[i + 4][j] == 1 and self.omok_pan[i + 1][j] == 0:
                    self.omok_pan[i + 1][j] = 2
                    return

        for i in range(15):
            for j in range(11):
                if self.omok_pan[i][j] == self.omok_pan[i][j + 2] == self.omok_pan[i][j + 3] == \
                        self.omok_pan[i][j + 4] == 1 and self.omok_pan[i][j + 1] == 0:
                    self.omok_pan[i][j + 1] = 2
                    return

        for i in range(11):
            for j in range(11):
                if self.omok_pan[i][j] == self.omok_pan[i + 2][j + 2] == self.omok_pan[i + 3][j + 3] == \
                        self.omok_pan[i + 4][j + 4] == 1 and self.omok_pan[i + 1][j + 1] == 0:
                    self.omok_pan[i + 1][j + 1] = 2
                    return

        for i in range(4, 15):
            for j in range(11):
                if self.omok_pan[i][j] == self.omok_pan[i - 2][j + 2] == self.omok_pan[i - 3][j + 3] == \
                        self.omok_pan[i - 4][j + 4] == 1 and self.omok_pan[i - 1][j + 1] == 0:
                    self.omok_pan[i - 1][j + 1] = 2
                    return




        #----------------------------------------------- 백 공격 -----------------------------------------------





        for i in range(11):
            for j in range(15):
                if self.omok_pan[i][j] == self.omok_pan[i+4][j] == 0 and self.omok_pan[i+1][j] == self.omok_pan[i+2][j] == self.omok_pan[i+3][j] == 2:
                    self.omok_pan[i][j] = 2
                    return

        for i in range(15):
            for j in range(11):
                if self.omok_pan[i][j] == self.omok_pan[i][j+4] == 0 and self.omok_pan[i][j+1] == self.omok_pan[i][j+2] == self.omok_pan[i][j+3] == 2:
                    self.omok_pan[i][j] = 2
                    return

        for i in range(11):
            for j in range(11):
                if self.omok_pan[i][j] == self.omok_pan[i+4][j+4] == 0 and self.omok_pan[i+1][j+1] == self.omok_pan[i+2][j+2] == self.omok_pan[i+3][j+3] == 2:
                    self.omok_pan[i][j] = 2
                    return

        for i in range(4,15):
            for j in range(11):
                if self.omok_pan[i][j] == self.omok_pan[i-4][j+4] == 0 and self.omok_pan[i-1][j+1] == self.omok_pan[i-2][j+2] == self.omok_pan[i-3][j+3] == 2:
                    self.omok_pan[i][j] = 2
                    return




        #------------------------------------------------------------------------------------------------------------



        for i in range(10):
            for j in range(15):
                if self.omok_pan[i][j] == self.omok_pan[i + 3][j] == self.omok_pan[i+5][j] == 0 and self.omok_pan[i + 1][j] == \
                        self.omok_pan[i + 2][j] == self.omok_pan[i + 4][j] == 2:
                    self.omok_pan[i+3][j] = 2
                    return

        for i in range(15):
            for j in range(10):
                if self.omok_pan[i][j] == self.omok_pan[i][j + 3] == self.omok_pan[i][j+5] == 0 and self.omok_pan[i][j+1] == \
                        self.omok_pan[i][j+2] == self.omok_pan[i][j+4] == 2:
                    self.omok_pan[i][j+3] = 2
                    return

        for i in range(10):
            for j in range(10):
                if self.omok_pan[i][j] == self.omok_pan[i + 3][j + 3] == self.omok_pan[i+5][j+5] == 0 and self.omok_pan[i + 1][j + 1] == \
                        self.omok_pan[i + 2][j + 2] == self.omok_pan[i + 4][j + 4] == 2:
                    self.omok_pan[i+3][j + 3] = 2
                    return

        for i in range(5,15):
            for j in range(10):
                if self.omok_pan[i][j] == self.omok_pan[i - 3][j + 3] == self.omok_pan[i-5][j+5] == 0 and self.omok_pan[i - 1][j + 1] == \
                        self.omok_pan[i - 2][j + 2] == self.omok_pan[i - 4][j + 4] == 2:
                    self.omok_pan[i-3][j + 3] = 2
                    return

        # ------------------------------------------------------------------------------------------------------------

        for i in range(10):
            for j in range(15):
                if self.omok_pan[i][j] == self.omok_pan[i + 2][j] == self.omok_pan[i + 5][j] == 0 and \
                        self.omok_pan[i + 1][j] == \
                        self.omok_pan[i + 3][j] == self.omok_pan[i + 4][j] == 2:
                    self.omok_pan[i + 2][j] = 2
                    return

        for i in range(15):
            for j in range(10):
                if self.omok_pan[i][j] == self.omok_pan[i][j + 2] == self.omok_pan[i][j + 5] == 0 and \
                        self.omok_pan[i][j + 1] == \
                        self.omok_pan[i][j + 3] == self.omok_pan[i][j + 4] == 2:
                    self.omok_pan[i][j + 2] = 2
                    return

        for i in range(10):
            for j in range(10):
                if self.omok_pan[i][j] == self.omok_pan[i + 2][j + 2] == self.omok_pan[i + 5][j + 5] == 0 and \
                        self.omok_pan[i + 1][j + 1] == \
                        self.omok_pan[i + 3][j + 3] == self.omok_pan[i + 4][j + 4] == 2:
                    self.omok_pan[i + 2][j + 2] = 2
                    return

        for i in range(5, 15):
            for j in range(10):
                if self.omok_pan[i][j] == self.omok_pan[i - 2][j + 2] == self.omok_pan[i - 5][j + 5] == 0 and \
                        self.omok_pan[i - 1][j + 1] == \
                        self.omok_pan[i - 3][j + 3] == self.omok_pan[i - 4][j + 4] == 2:
                    self.omok_pan[i - 2][j + 2] = 2
                    return



        #----------------------------------------------- 흑 방어 ---------------------------------------------------------

        aList = []
        bList = []

        for i in range(11):
            for j in range(15):
                if self.omok_pan[i][j] == self.omok_pan[i + 4][j] == 0 and self.omok_pan[i + 1][j] == \
                        self.omok_pan[i + 2][j] == self.omok_pan[i + 3][j] == 1:
                    aList.append(self.weight_AI(i,j));bList.append((i,j))
                    aList.append(self.weight_AI(i+4,j));bList.append((i+4,j))

        for i in range(15):
            for j in range(11):
                if self.omok_pan[i][j] == self.omok_pan[i][j + 4] == 0 and self.omok_pan[i][j + 1] == self.omok_pan[i][
                    j + 2] == self.omok_pan[i][j + 3] == 1:
                    aList.append(self.weight_AI(i,j));bList.append((i,j))
                    aList.append(self.weight_AI(i,j+4));bList.append((i,j+4))

        for i in range(11):
            for j in range(11):
                if self.omok_pan[i][j] == self.omok_pan[i + 4][j + 4] == 0 and self.omok_pan[i + 1][j + 1] == \
                        self.omok_pan[i + 2][j + 2] == self.omok_pan[i + 3][j + 3] == 1:
                    aList.append(self.weight_AI(i,j));bList.append((i,j))
                    aList.append(self.weight_AI(i+4,j+4));bList.append((i+4,j+4))

        for i in range(4, 15):
            for j in range(11):
                if self.omok_pan[i][j] == self.omok_pan[i - 4][j + 4] == 0 and self.omok_pan[i - 1][j + 1] == \
                        self.omok_pan[i - 2][j + 2] == self.omok_pan[i - 3][j + 3] == 1:
                    aList.append(self.weight_AI(i,j));bList.append((i,j))
                    aList.append(self.weight_AI(i-4,j+4));bList.append((i-4,j+4))


        # ------------------------------------------------------------------------------------------------------------


        for i in range(10):
            for j in range(15):
                if self.omok_pan[i][j] == self.omok_pan[i + 3][j] == self.omok_pan[i + 5][j] == 0 and \
                        self.omok_pan[i + 1][j] == \
                        self.omok_pan[i + 2][j] == self.omok_pan[i + 4][j] == 1:
                    aList.append(self.weight_AI(i+3,j));bList.append((i+3,j))
                    aList.append(self.weight_AI(i,j));bList.append((i,j))
                    aList.append(self.weight_AI(i+5,j));bList.append((i+5,j))

        for i in range(15):
            for j in range(10):
                if self.omok_pan[i][j] == self.omok_pan[i][j + 3] == self.omok_pan[i][j + 5] == 0 and self.omok_pan[i][
                    j + 1] == \
                        self.omok_pan[i][j + 2] == self.omok_pan[i][j + 4] == 1:
                    aList.append(self.weight_AI(i,j+3));bList.append((i,j+3))
                    aList.append(self.weight_AI(i,j));bList.append((i,j))
                    aList.append(self.weight_AI(i,j+5));bList.append((i,j+5))

        for i in range(10):
            for j in range(10):
                if self.omok_pan[i][j] == self.omok_pan[i + 3][j + 3] == self.omok_pan[i + 5][j + 5] == 0 and \
                        self.omok_pan[i + 1][j + 1] == \
                        self.omok_pan[i + 2][j + 2] == self.omok_pan[i + 4][j + 4] == 1:
                    aList.append(self.weight_AI(i+3,j+3));bList.append((i+3,j+3))
                    aList.append(self.weight_AI(i,j));bList.append((i,j))
                    aList.append(self.weight_AI(i+5,j+5));bList.append((i+5,j+5))

        for i in range(5, 15):
            for j in range(10):
                if self.omok_pan[i][j] == self.omok_pan[i - 3][j + 3] == self.omok_pan[i - 5][j + 5] == 0 and \
                        self.omok_pan[i - 1][j + 1] == \
                        self.omok_pan[i - 2][j + 2] == self.omok_pan[i - 4][j + 4] == 1:
                    aList.append(self.weight_AI(i-3,j+3));bList.append((i-3,j+3))
                    aList.append(self.weight_AI(i,j));bList.append((i,j))
                    aList.append(self.weight_AI(i-5,j+5));bList.append((i-5,j+5))



        # ------------------------------------------------------------------------------------------------------------




        for i in range(10):
            for j in range(15):
                if self.omok_pan[i][j] == self.omok_pan[i + 2][j] == self.omok_pan[i + 5][j] == 0 and \
                        self.omok_pan[i + 1][j] == \
                        self.omok_pan[i + 3][j] == self.omok_pan[i + 4][j] == 1:
                    aList.append(self.weight_AI(i+2,j));bList.append((i+2,j))
                    aList.append(self.weight_AI(i,j));bList.append((i,j))
                    aList.append(self.weight_AI(i+5,j));bList.append((i+5,j))

        for i in range(15):
            for j in range(10):
                if self.omok_pan[i][j] == self.omok_pan[i][j + 2] == self.omok_pan[i][j + 5] == 0 and \
                        self.omok_pan[i][j + 1] == \
                        self.omok_pan[i][j + 3] == self.omok_pan[i][j + 4] == 1:
                    aList.append(self.weight_AI(i,j+2));bList.append((i,j+2))
                    aList.append(self.weight_AI(i,j));bList.append((i,j))
                    aList.append(self.weight_AI(i,j+5));bList.append((i,j+5))

        for i in range(10):
            for j in range(10):
                if self.omok_pan[i][j] == self.omok_pan[i + 2][j + 2] == self.omok_pan[i + 5][j + 5] == 0 and \
                        self.omok_pan[i + 1][j + 1] == \
                        self.omok_pan[i + 3][j + 3] == self.omok_pan[i + 4][j + 4] == 1:
                    aList.append(self.weight_AI(i+2,j+2));bList.append((i+2,j+2))
                    aList.append(self.weight_AI(i,j));bList.append((i,j))
                    aList.append(self.weight_AI(i+5,j+5));bList.append((i+5,j+5))

        for i in range(5, 15):
            for j in range(10):
                if self.omok_pan[i][j] == self.omok_pan[i - 2][j + 2] == self.omok_pan[i - 5][j + 5] == 0 and \
                        self.omok_pan[i - 1][j + 1] == \
                        self.omok_pan[i - 3][j + 3] == self.omok_pan[i - 4][j + 4] == 1:
                    aList.append(self.weight_AI(i-2,j+2));bList.append((i-2,j+2))
                    aList.append(self.weight_AI(i,j));bList.append((i,j))
                    aList.append(self.weight_AI(i-5,j+5));bList.append((i-5,j+5))

        if len(aList) > 0:
            weightmax = max(aList)
            inx = bList[aList.index(max(aList))]
            print('가중치')
            self.omok_pan[inx[0]][inx[1]] = 2
            return


        #-------------------------------------------------- 딥러닝 MOVE ------------------------------------------


        q = self.omok_pan[:]

        xhat = np.array(q)

        #predict = [[0 for i in range(11)] for j in range(11)]
        xhat = xhat.reshape(1,15,15,1)
        xhat = xhat.astype('float32')/2
        yhat = self.model.predict(xhat)
        predict = yhat[0].tolist()
        #print(predict)

        for i in range(15):
            for j in range(15):
                if self.omok_pan[i][j] != 0: predict[i*15+j] = 0

        """for i in range(15):
            for j in range(15):
                if q[i][j] == 0:
                    xhatcopy = xhat.copy()
                    xhatcopy[i, j] = 2
                    xhatcopy = xhatcopy.reshape(1, 15, 15, 1)
                    xhatcopy = xhatcopy.astype('float32') / 2
                    yhat = self.model.predict(xhatcopy)
                    #print(yhat)
                    predict[i][j] = yhat[0][1]"""

        y, x = self.findMaxIndex(predict)
        self.omok_pan[y][x] = 2




    def victory_condition(self):
        cont = 0
        
        for i in range(15):
            for j in range(15):
                if self.omok_pan[i][j] == 0:
                    cont += 1
                    
        if cont == 0:
            print("무승부 입니다.")
            return 1
                
        for i in range(11):
            for j in range(11):
                last = self.omok_pan[i][j]
                cnt = 1
                for z in range(1, 5):
                    if self.omok_pan[i + z][j + z] == last and self.omok_pan[i + z][j + z] != 0:
                        cnt += 1
                    else:
                        break

                if cnt == 5:
                    if last == 1:
                        print("흑돌 승리")
                        return 1
                    elif last == 2:
                        print("백돌 승리")
                        return 1

        for i in range(4,15):
            for j in range(11):
                last = self.omok_pan[i][j]
                cnt = 1
                for z in range(1, 5):
                    if self.omok_pan[i - z][j + z] == last and self.omok_pan[i - z][j + z] != 0:
                        cnt += 1
                    else:
                        break

                if cnt == 5:
                    if last == 1:
                        print("흑돌 승리")
                        return 1
                    elif last == 2:
                        print("백돌 승리")
                        return 1
                        
        for i in range(15):
            for j in range(11):
                last = self.omok_pan[i][j]
                cnt = 1
                for z in range(1, 5):
                    if self.omok_pan[i][j + z] == last and self.omok_pan[i][j + z] != 0:
                        cnt += 1
                    else:
                        break

                if cnt == 5:
                    if last == 1:
                        print("흑돌 승리")
                        return 1
                    elif last == 2:
                        print("백돌 승리")
                        return 1

        for i in range(11):
            for j in range(15):
                last = self.omok_pan[i][j]
                cnt = 1
                for z in range(1, 5):
                    if self.omok_pan[i + z][j] == last and self.omok_pan[i + z][j] != 0:
                        cnt += 1
                    else:
                        break

                if cnt == 5:
                    if last == 1:
                        print("흑돌 승리")
                        return 1
                    elif last == 2:
                        print("백돌 승리")
                        return 1

        return 0

    def check_6(self,y, x):
        count = 0

        q = copy.deepcopy(self.omok_pan)
        q[y][x] = 1

        cnt = 0

        for i in range(x,15):
            if q[y][i] == 1:
                cnt+=1
            else:
                break

        for i in range(x-1,-1,-1):
            if q[y][i] == 1:
                cnt+=1
            else:
                break

        if cnt >= 6: count += 1

        #-------------------------------------------------------------------------------

        cnt = 0

        for i in range(y,15):
            if q[i][x] == 1:
                cnt+=1
            else:
                break

        for i in range(y-1,-1,-1):
            if q[i][x] == 1:
                cnt+=1
            else:
                break

        if cnt >= 6: count += 1

        #-------------------------------------------------------------------------

        cnt = 0
        inx = 0

        while y+inx < 15 and x+inx < 15:
            if q[y+inx][x+inx] == 1:
                cnt+=1
            else:
                break
            inx += 1

        inx = 1
        while y-inx >= 0 and x-inx >= 0:
            if q[y-inx][x-inx] == 1:
                cnt+=1
            else:
                break
            inx += 1

        if cnt >= 6: count += 1

        #--------------------------------------------------------------

        cnt = 0
        inx = 0

        while y-inx >= 0 and x+inx < 15:
            if q[y-inx][x+inx] == 1:
                cnt+=1
            else:
                break
            inx += 1

        inx = 1

        while y+inx < 15 and x-inx >= 0:
            if q[y+inx][x-inx] == 1:
                cnt+=1
            else:
                break
            inx += 1

        if cnt >= 6: count += 1

        if count > 1:
            return True
        else:
            return False

    def check_44(self,y, x):
        count = 0

        if y == 14 or y == 0 or x == 14 or x == 0:
            return False

        q = copy.deepcopy(self.omok_pan)
        q[y][x] = 1

        Nope = False
        cnt = 0
        blank_cnt = 0

        for i in range(x, 15):
            if q[y][i] == 2:
                if q[y][i - 1] == 1:
                    Nope = True
                break
            if q[y][i] == 0:
                if blank_cnt == 1:
                    if q[y][i - 1] == 0:
                        blank_cnt = 0
                    break
                else:
                    blank_cnt += 1
            if q[y][i] == 1:
                cnt += 1

        for i in range(x - 1, -1, -1):
            if q[y][i] == 2:
                if q[y][i + 1] == 1:
                    Nope = True
                break
            if q[y][i] == 0:
                if blank_cnt == 1:
                    if q[y][i - 1] == 0:
                        blank_cnt = 0
                    break
                else:
                    blank_cnt += 1
            if q[y][i] == 1:
                cnt += 1

        if cnt == 4 and not Nope: count += 1

        # -------------------------------------------------------------------------------

        Nope = False
        cnt = 0
        blank_cnt = 0
        for i in range(y, 15):
            if q[i][x] == 2:
                if q[i - 1][x] == 1:
                    Nope = True
                break
            if q[i][x] == 0:
                if blank_cnt == 1:
                    if q[i - 1][x] == 0:
                        blank_cnt = 0
                    break
                else:
                    blank_cnt += 1
            if q[i][x] == 1:
                cnt += 1

        for i in range(y - 1, -1, -1):
            if q[i][x] == 2:
                if q[i + 1][x] == 1:
                    Nope = True
                break
            if q[i][x] == 0:
                if blank_cnt == 1:
                    if q[i - 1][x] == 0:
                        blank_cnt = 0
                    break
                else:
                    blank_cnt += 1
            if q[i][x] == 1:
                cnt += 1

        if cnt == 4 and not Nope: count += 1
        # print(cnt)

        # -------------------------------------------------------------------------

        Nope = False
        cnt = 0
        blank_cnt = 0

        inx = 0
        while y + inx < 15 and x + inx < 15:
            if q[y + inx][x + inx] == 2:
                if q[y + inx - 1][x + inx - 1] == 1:
                    Nope = True
                break
            if q[y + inx][x + inx] == 0:
                if blank_cnt == 1:
                    if q[y + inx - 1][x + inx - 1] == 0:
                        blank_cnt = 0
                    break
                else:
                    blank_cnt += 1
            if q[y + inx][x + inx] == 1:
                cnt += 1
            inx += 1

        inx = 1
        while y - inx >= 0 and x - inx >= 0:
            if q[y - inx][x - inx] == 2:
                if q[y - inx + 1][x - inx + 1] == 1:
                    Nope = True
                break
            if q[y - inx][x - inx] == 0:
                if blank_cnt == 1:
                    if q[y - inx + 1][x - inx + 1] == 0:
                        blank_cnt = 0
                    break
                else:
                    blank_cnt += 1
            if q[y - inx][x - inx] == 1:
                cnt += 1
            inx += 1

        if cnt == 4 and not Nope: count += 1
        # print(cnt)

        # --------------------------------------------------------------

        Nope = False
        cnt = 0
        blank_cnt = 0

        inx = 0
        while y - inx >= 0 and x + inx < 15:
            if q[y - inx][x + inx] == 2:
                if q[y - inx + 1][x + inx - 1] == 1:
                    Nope = True
                break
            if q[y - inx][x + inx] == 0:
                if blank_cnt == 1:
                    if q[y - inx + 1][x + inx - 1] == 1:
                        blank_cnt = 0
                    break
                else:
                    blank_cnt += 1
            if q[y - inx][x + inx] == 1:
                cnt += 1
            inx += 1

        inx = 1

        while y + inx < 15 and x - inx >= 0:
            if q[y + inx][x - inx] == 2:
                if q[y + inx - 1][x - inx + 1] == 1:
                    Nope = True
                break
            if q[y + inx][x - inx] == 0:
                if blank_cnt == 1:
                    if q[y + inx - 1][x - inx + 1] == 1:
                        blank_cnt = 0
                    break
                else:
                    blank_cnt += 1
            if q[y + inx][x - inx] == 1:
                cnt += 1
            inx += 1

        if cnt == 4 and not Nope: count += 1
        # print(cnt)

        if count > 1:
            return True
        else:
            return False

    def check_33(self,y, x):
        count = 0

        if y == 14 or y == 0 or x == 14 or x == 0:
            return False

        q = copy.deepcopy(self.omok_pan)
        q[y][x] = 1

        Nope = False
        cnt = 0
        blank_cnt = 0

        for i in range(x,15):
            if q[y][i] == 2:
                if q[y][i-1] == 1:
                    Nope = True
                break
            if q[y][i] == 0:
                if blank_cnt == 1:
                    if q[y][i - 1] == 0:
                        blank_cnt = 0
                    break
                else:
                    blank_cnt += 1
            if q[y][i] == 1:
                cnt+=1

        for i in range(x-1,-1,-1):
            if q[y][i] == 2:
                if q[y][i+1] == 1:
                    Nope = True
                break
            if q[y][i] == 0:
                if blank_cnt == 1:
                    if q[y][i - 1] == 0:
                        blank_cnt = 0
                    break
                else:
                    blank_cnt += 1
            if q[y][i] == 1:
                cnt+=1

        if cnt == 3 and not Nope: count += 1

        #-------------------------------------------------------------------------------

        Nope = False
        cnt = 0
        blank_cnt = 0
        for i in range(y,15):
            if q[i][x] == 2:
                if q[i-1][x] == 1:
                    Nope = True
                break
            if q[i][x] == 0:
                if blank_cnt == 1:
                    if q[i - 1][x] == 0:
                        blank_cnt = 0
                    break
                else:
                    blank_cnt += 1
            if q[i][x] == 1:
                cnt+=1

        for i in range(y-1,-1,-1):
            if q[i][x] == 2:
                if q[i+1][x] == 1:
                    Nope = True
                break
            if q[i][x] == 0:
                if blank_cnt == 1:
                    if q[i - 1][x] == 0:
                        blank_cnt = 0
                    break
                else:
                    blank_cnt += 1
            if q[i][x] == 1:
                cnt+=1

        if cnt == 3 and not Nope: count += 1
        #print(cnt)

        #-------------------------------------------------------------------------

        Nope = False
        cnt = 0
        blank_cnt = 0

        inx = 0
        while y+inx < 15 and x+inx < 15:
            if q[y+inx][x+inx] == 2:
                try:
                    if q[y+inx-1][x+inx-1] == 1:
                        Nope = True
                except Exception:
                    pass
                break
            if q[y+inx][x+inx] == 0:
                if blank_cnt == 1:
                    if q[y + inx - 1][x + inx - 1] == 0:
                        blank_cnt = 0
                    break
                else:
                    blank_cnt += 1
            if q[y+inx][x+inx] == 1:
                cnt+=1
            inx += 1

        inx = 1
        while y-inx >= 0 and x-inx >= 0:
            if q[y-inx][x-inx] == 2:
                try:
                    if q[y-inx+1][x-inx+1] == 1:
                        Nope = True
                except Exception:
                    pass
                break
            if q[y-inx][x-inx] == 0:
                if blank_cnt == 1:
                    if q[y - inx + 1][x - inx + 1] == 0:
                        blank_cnt = 0
                    break
                else:
                    blank_cnt += 1
            if q[y-inx][x-inx] == 1:
                cnt+=1
            inx += 1

        if cnt == 3 and not Nope: count += 1

        #--------------------------------------------------------------

        Nope = False
        cnt = 0
        blank_cnt = 0

        inx = 0
        while y-inx >= 0 and x+inx < 15:
            if q[y-inx][x+inx] == 2:
                try:
                    if q[y-inx+1][x+inx-1] == 1:
                        Nope = True
                except Exception:
                    pass
                break
            if q[y-inx][x+inx] == 0:
                if blank_cnt == 1:
                    if q[y - inx + 1][x + inx - 1] == 1:
                        blank_cnt = 0
                    break
                else:
                    blank_cnt += 1
            if q[y-inx][x+inx] == 1:
                cnt+=1
            inx += 1

        inx = 1

        while y+inx < 15 and x-inx >= 0:
            if q[y+inx][x-inx] == 2:
                try:
                    if q[y+inx-1][x-inx+1] == 1:
                        Nope = True
                except Exception:
                    pass
                break
            if q[y+inx][x-inx] == 0:
                if blank_cnt == 1:
                    if q[y + inx - 1][x - inx + 1] == 1:
                        blank_cnt = 0
                    break
                else:
                    blank_cnt += 1
            if q[y+inx][x-inx] == 1:
                cnt+=1
            inx += 1

        if cnt == 3 and not Nope: count += 1
        #print(cnt)

        if count > 1:
            return True
        else:
            return False

    def draw(self):
        for i in range(15):
            for j in range(15):
                if self.omok_pan[i][j] == 1:
                    label = QLabel(self)
                    label.setGeometry(QtCore.QRect(j*40, i*40, 40, 40))
                    label.setPixmap(QPixmap("./black.png").scaled(40,40))
                    label.show()
                elif self.omok_pan[i][j] == 2:
                    label = QLabel(self)
                    label.setGeometry(QtCore.QRect(j*40, i*40, 40, 40))
                    label.setPixmap(QPixmap("./white.png").scaled(40,40))
                    label.show()

    def findMaxIndex(self,lst):
        a = lst.index(max(lst))
        return (a//15,a%15)

        """a = max(map(max,lst))

        for i in range(len(lst)):
            for j in range(len(lst[i])):
                if lst[i][j] == a:
                    return (i,j)"""

    def mousePressEvent(self, event):
        if event.buttons() & Qt.LeftButton and not self.Finish:

            a, b = event.y()//40,event.x()//40

            if self.omok_pan[a][b] != 0:
                print("이미 자리에 돌이 있습니다.")
                return
            else:
                if self.check_33(a, b) or self.check_44(a,b) or self.check_6(a,b):
                    print("놓을수 없는 위치입니다.")
                    return
                else:
                    self.omok_pan[a][b] = 1

            self.draw()

            status = self.victory_condition()

            if status == 1:
                self.Finish = True
            else:
                self.omok_AI()
                self.draw()
                status = self.victory_condition()

                if status == 1:
                    self.Finish = True


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    win = Main()
    sys.exit(app.exec_())
