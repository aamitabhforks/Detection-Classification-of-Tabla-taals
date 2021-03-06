import GUI
import audioBackend
from PyQt5 import QtGui, QtCore, QtWidgets
import sys
import numpy as np
import pyqtgraph
import time
import warnings

warnings.filterwarnings('ignore')


class ExampleApp(QtWidgets.QMainWindow, GUI.Ui_MainWindow):
    def __init__(self, parent=None):
        pyqtgraph.setConfigOption('background', 'w')  # before loading widget
        super(ExampleApp, self).__init__(parent)
        self.setupUi(self)
        self.FFT.plotItem.showGrid(True, True, 1)
        self.raw.plotItem.showGrid(True, True, 1)
        self.maxFFT = 0
        self.maxPCM = 0
        self.ear = audioBackend.PNHear(rate=44100, updatesPerSecond=50)
        self.ear.stream_start()

    def update(self):
        if not self.ear.data is None and not self.ear.fft is None:
            pcmMax = np.max(np.abs(self.ear.data))

            if pcmMax > self.maxPCM:
                self.maxPCM = pcmMax
                self.raw.plotItem.setRange(yRange=[-pcmMax, pcmMax])
            if np.max(self.ear.fft) > self.maxFFT:
                self.maxFFT = np.max(np.abs(self.ear.fft))
                self.FFT.plotItem.setRange(yRange=[0, 1])

            pen = pyqtgraph.mkPen(color='r')
            self.raw.plot(self.ear.datax, self.ear.data, pen=pen, clear=True)
            self.raw.plotItem.setLabel('left', "Amplitude")
            self.raw.plotItem.setLabel('bottom', "Time")
            # self.raw.plotItem.enableAutoScale()

            pen = pyqtgraph.mkPen(color='b')
            self.FFT.plot(self.ear.fftx, self.ear.fft/self.maxFFT, pen=pen, clear=True)
            self.FFT.plotItem.setLabel('bottom', "Frequency")
            self.FFT.plotItem.setLabel('left', "Amplitude(norm)")
            # self.FFT.plotItem.enableAutoScale()

        QtCore.QTimer.singleShot(1, self.update)  # QUICKLY repeat

if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    form = ExampleApp()
    form.show()
    form.update()  # start with something
    app.exec_()
    print("DONE")
    time.sleep(5)
    sys.exit()





