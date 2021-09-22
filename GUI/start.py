import numpy as np
from PyQt5 import QtGui, QtCore
from pyqtgraph.Qt import QtCore
import pyqtgraph as pg
import pandas as pd
from PyQt5 import QtWidgets

class SpikeData():
    def __init__(self):
        self.data_path='/media/maria/DATA1/Documents/NeuroMatchAcademy2020_dat/unzipped_files/Moniz_2017-05-15.tar'
        self.load_data()

    def load_data(self):
        data_path = self.data_path
        self.trials_intervals = np.load(data_path+'/'+'trials.intervals.npy') # in seconds
        self.spike_times = np.load(data_path+'/'+'spikes.times.npy') * 1000 # Unbinned spike times in ms
        #self.trials_gocue_times = np.load(data_path+'/'+'trials.goCue_times.npy')
        #self.trials_response_choice = np.load(data_path+'/'+'trials.response_choice.npy') # -1 left, 1, right, 0 no response
        #self.spontaneous_intervals = np.load(data_path+'/'+'spontaneous.intervals.npy')
        #self.trials_response_time = np.load(data_path+'/'+'trials.response_times.npy')
        self.spike_clusters = np.load(data_path+'/'+'spikes.clusters.npy')
        #self.site_positions = np.load(data_path+'/'+'channels.sitePositions.npy')
        #self.clusters_depths = np.load(data_path+'/'+'clusters.depths.npy')
        self.clusters_annotation = np.load(data_path+'/'+'clusters._phy_annotation.npy')
        #self.channel_sites = np.load(data_path+'/'+'channels.site.npy')
        #self.channels_brainlocation = pd.read_csv(data_path+'/'+'channels.brainLocation.tsv', sep='\t')
        #self.clusters_probes = np.load(data_path+'/'+'clusters.probes.npy')
        #self.channels_probe = np.load(data_path+'/'+'channels.probe.npy')
        #self.trials_visual_time = np.load(data_path+'/'+'trials.visualStim_times.npy')
        # Behaviour data
        #self.wheel_movement = np.load(data_path+'/'+'wheelMoves.type.npy')
        #self.wheel_intervals = np.load(data_path+'/'+'wheelMoves.intervals.npy')

    def sort_into_cells(self):
        spike_time_cells = np.empty(len(self.clusters_annotation), dtype=object) # Initalise empty object
        for i in (np.arange(len(np.unique(self.spike_clusters)))):
          # Create a spike time arrays, where each array in the array is a spike time of a cell
          spike_time_cells[i] = self.spike_times[(np.where(self.spike_clusters == i)[0])]
        np.save('spike_time_cells.npy',spike_time_cells)
        return spike_time_cells

class SpikeWindow(QtGui.QMainWindow):
    def __init__(self,parent=None):
        super(SpikeWindow, self).__init__(parent)
        self.spike_data=SpikeData()
        #self.spike_time_cells=self.spike_data.sort_into_cells()
        self.spike_time_cells=np.load('spike_time_cells.npy',allow_pickle=True)/1000
        print('Done loading data!')
        self.cwidget=QtGui.QWidget(self)
        self.setCentralWidget(self.cwidget)
        self.l0=QtGui.QGridLayout()
        self.cwidget.setLayout(self.l0)
        self.win = pg.GraphicsLayoutWidget()
        self.win.resize(5000,5000)
        self.l0.addWidget(self.win,0,0,20,20)
        #self.scatter_plot=pg.plot()
        self.scatter_plot=pg.PlotItem()
        #self.scatter_plot.addItem(self.scatter)
        self.sc_plots=pg.GraphicsLayoutWidget()
        self.sc_plots.addItem(self.scatter_plot)
        self.l0.addWidget(self.sc_plots,0,0,20,20)
        #print(self.spike_time_cells[0][:100])
        self.x=[]
        self.y=[]
        for n in range(len(self.spike_time_cells)):
            self.x+=list(self.spike_time_cells[n][(10<self.spike_time_cells[n]) & (self.spike_time_cells[n]<15)])
            self.y+=[n]*len(list(self.spike_time_cells[n][(10<self.spike_time_cells[n]) & (self.spike_time_cells[n]<15)]))
        #print(self.x)
        #print(self.y)
        print('Done parsing list!')
        self.plot_sc()

    def plot_sc(self):
        self.scatter_plot.plot(self.x, self.y, pen=None, symbol='t', symbolPen=None, symbolSize=2)
        self.win.show()

import sys
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = SpikeWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
