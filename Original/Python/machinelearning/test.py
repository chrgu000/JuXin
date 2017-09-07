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


from numpy import arange, sin, pi

import matplotlib

# uncomment the following to use wx rather than wxagg
#matplotlib.use('WX')
#from matplotlib.backends.backend_wx import FigureCanvasWx as FigureCanvas

# comment out the following to use wx rather than wxagg
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas

from matplotlib.backends.backend_wx import NavigationToolbar2Wx

from matplotlib.figure import Figure

import wx
import wx.lib.mixins.inspection as WIT


class CanvasFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1,
                          'CanvasFrame', size=(550, 350))

        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        t = arange(0.0, 3.0, 0.01)
        s = sin(2 * pi * t)

        self.axes.plot(t, s)
        self.canvas = FigureCanvas(self, -1, self.figure)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.EXPAND)
        self.SetSizer(self.sizer)
        self.Fit()

        self.add_toolbar()  # comment this out for no toolbar

    def add_toolbar(self):
        self.toolbar = NavigationToolbar2Wx(self.canvas)
        self.toolbar.Realize()
        # By adding toolbar in sizer, we are able to put it at the bottom
        # of the frame - so appearance is closer to GTK version.
        self.sizer.Add(self.toolbar, 0, wx.LEFT | wx.EXPAND)
        # update the axes menu on the toolbar
        self.toolbar.update()


# alternatively you could use
#class App(wx.App):
class App(WIT.InspectableApp):
    def OnInit(self):
        'Create the main window and insert the custom frame'
        self.Init()
        frame = CanvasFrame()
        frame.Show(True)

        return True

app = App(0)
app.MainLoop()



