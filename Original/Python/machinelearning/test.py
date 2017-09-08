#from sklearn import cluster
#import TrainModel
#TM=TrainModel.TrainModel('test')
##
#k_means=cluster.KMeans(n_clusters=2)
#k_means.fit(Matrix[:,[0,1]])
#flag1=np.array(k_means.labels_)
#k_means.fit(Matrix[:,[6,20]])
#flag2=np.array(k_means.labels_)
#k_means.fit(Matrix[:,[8,9]])
#flag3=np.array(k_means.labels_)

#flags=(flag1>0)*(flag2>0)*(flag3<1)
#matrix=Matrix[:,0:2]
#from sklearn.mixture import GMM 
#gmm = GMM(n_components=2).fit(matrix) 
#flags = gmm.predict(matrix) 


#TM.ReFig([Re[(flag1<1)*(flag2<1)],Re[(flag1<1)*(flag3<1)],Re[(flag1<1)*(flag2<1)*(flag3<1)]],['flag1','flag2','flag3'])

#flagU=np.unique(flags)
#re=[]
#titleFig=[]
#for i in range(len(flagU)):
#    re.append(Re[flags==flagU[i]])
#    titleFig.append(str(flagU[i]))
#    
#plt.figure()
#TM.ReFig(re,titleFig)


import sys
from PyQt5 import QtWidgets
 
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
 
import random
 
class Window(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
 
        self.figure = plt.figure()
        self.axes = self.figure.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)
        self.canvas = FigureCanvas(self.figure)
 
         
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar.hide()
 
        # Just some button 
        self.button1 = QtWidgets.QPushButton('Plot')
        self.button1.clicked.connect(self.plot)
 
        self.button2 = QtWidgets.QPushButton('Zoom')
        self.button2.clicked.connect(self.zoom)
         
        self.button3 = QtWidgets.QPushButton('Pan')
        self.button3.clicked.connect(self.pan)
         
        self.button4 = QtWidgets.QPushButton('Home')
        self.button4.clicked.connect(self.home)
 
 
        # set the layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        
        btnlayout = QtWidgets.QHBoxLayout()
        btnlayout.addWidget(self.button1)
        btnlayout.addWidget(self.button2)
        btnlayout.addWidget(self.button3)
        btnlayout.addWidget(self.button4)
        qw = QtWidgets.QWidget(self)
        qw.setLayout(btnlayout)
        layout.addWidget(qw)
        
        self.setLayout(layout)
 
    def home(self):
        self.toolbar.home()
    def zoom(self):
        self.toolbar.zoom()
    def pan(self):
        self.toolbar.pan()
         
    def plot(self):
        ''' plot some random stuff '''
        data = [random.random() for i in range(25)]
        self.axes.plot(data, '*-')
        self.canvas.draw()
 
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
 
    main = Window()
    main.setWindowTitle('Simple QTpy and MatplotLib example with Zoom/Pan')
    main.show()
 
    sys.exit(app.exec_())