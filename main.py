#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


import copy
import sys

from PyQt4 import QtGui, QtCore


class GameLife(object):
    def __init__(self, newWidth=0, newHeight=0, newMatrix=None):
        self.width = newWidth
        self.height = newHeight
        self.numberIter = 0
        self.setCleanCard()
        if newMatrix is not None:
            self.fillingCard(newMatrix)

    def setCleanCard(self):
        self.cardGame = []
        for i in range(self.height + 2):
            self.cardGame.append([])
            for j in range(self.width + 2):
                self.cardGame[i].append(0)

    def fillingCard(self, matrix):
        for i in range(self.height):
            for j in range(self.width):
                self.cardGame[i + 1][j + 1] = matrix[i][j]

    def iteration(self, step=1):
        nextNumberIter = self.numberIter + step
        while self.numberIter < nextNumberIter:
            self.tempCard = copy.deepcopy(self.cardGame)
            for i in range(1, self.height + 1):
                for j in range(1, self.width + 1):
                    self.cellRenewal(i, j)
            self.numberIter += 1

    def cellRenewal(self, i, j):
        temp = self.getCellValue(i, j)
        if self.cardGame[i][j] == 0 and temp == 3:
            self.cardGame[i][j] = 1
            return
        if self.cardGame[i][j] == 1 and (temp < 2 or temp > 3):
            self.cardGame[i][j] = 0
            return

    def getCellValue(self, i, j):
        temp = self.tempCard[i + 1][j + 1] + self.tempCard[i][j + 1] + self.tempCard[i + 1][j] + \
               self.tempCard[i - 1][j - 1] + self.tempCard[i - 1][j] + self.tempCard[i][j - 1] + \
               self.tempCard[i - 1][j + 1] + self.tempCard[i + 1][j + 1]
        return temp


class Life(QtGui.QWidget):
    def __init__(self, tempGame):
        super(Life, self).__init__()
        self.sizeX = 800
        self.sizeY = 700
        self.setGeometry(150, 0, self.sizeX, self.sizeY)
        self.myGame = tempGame
        self.speed = 1
        self.step = 1
        self.stepTime = 1000
        self.flagPause = False
        self.sizeItem = self.sizeY / max(tempGame.width, tempGame.height)
        self.setWindowTitle('Life')

        self.pauseButton = QtGui.QPushButton('Pause', self)
        self.pauseButton.setGeometry(self.sizeY, 100, 100, 50)
        self.pauseButton.clicked.connect(self.setPause)
        self.pauseButton.show()

        self.speed1Button = QtGui.QPushButton('speed = 1', self)
        self.speed1Button.setGeometry(self.sizeY, 200, 100, 50)
        self.speed1Button.clicked.connect(self.setSpeed1)
        self.speed1Button.show()

        self.speed2Button = QtGui.QPushButton('speed = 2', self)
        self.speed2Button.setGeometry(self.sizeY, 250, 100, 50)
        self.speed2Button.clicked.connect(self.setSpeed2)
        self.speed2Button.show()

        self.speed4Button = QtGui.QPushButton('speed = 4', self)
        self.speed4Button.setGeometry(self.sizeY, 300, 100, 50)
        self.speed4Button.clicked.connect(self.setSpeed4)
        self.speed4Button.show()

        self.show()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.on_timer)
        self.timer.start(self.sizeX)

    def mousePressEvent(self, event):
        self.emit(QtCore.SIGNAL('ourSignal()'))
        if self.flagPause is True:
            y = event.pos().x()
            x = event.pos().y()
            if x > 0 and x < self.sizeY and y > 0 and y < self.sizeY:
                x = int(x / self.sizeItem)
                y = int(y / self.sizeItem)
                self.myGame.cardGame[x + 1][y + 1] = (self.myGame.cardGame[x + 1][y + 1] + 1) % 2
        self.repaint()

    def setPause(self):
        if self.flagPause:
            self.flagPause = False
            self.timer.start(self.stepTime)
        else:
            self.flagPause = True
            self.timer.stop()

    def setSpeed1(self):
        self.speed = 1
        self.timer.stop()
        self.timer.start(self.stepTime / self.speed)

    def setSpeed2(self):
        self.speed = 2
        self.timer.stop()

        self.timer.start(self.stepTime / self.speed)

    def setSpeed4(self):
        self.speed = 4
        self.timer.stop()
        self.timer.start(self.stepTime / self.speed)

    def on_timer(self):
        self.myGame.iteration(self.step)
        self.repaint()

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.showCard(qp)
        qp.end()

    def showCard(self, qp):
        for i in range(1, self.myGame.height + 1):
            for j in range(1, self.myGame.width + 1):
                self.drawRectangles(qp, i, j)

    def drawRectangles(self, qp, i, j):
        if self.myGame.cardGame[i][j] == 1:
            qp.setBrush(QtGui.QColor(0, 0, 255))
        else:
            qp.setBrush(QtGui.QColor(250, 250, 250))
        qp.drawRect((j - 1) * self.sizeItem, (i - 1) * self.sizeItem, self.sizeItem, self.sizeItem)


def main():
    f = open('input', 'r')
    height, width = f.readline().split(' ')
    height = int(height)
    width = int(width)
    matrix = []
    for i in range(width):
        matrix.append(list(map(lambda x: int(x), f.readline().split((' ')))))
    f.close()
    myGame = GameLife(height, width, matrix)
    app = QtGui.QApplication(sys.argv)
    life = Life(myGame)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
