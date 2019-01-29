from assign2_support import *

#####################################
# End of support 
#####################################

# Add your code here

import tkinter as tk

class TemperatureData():
    def __init__(self):
        self._stations = []
        self._data = {}
        self._years = []
        self._temp = []
        self._range = ()
        self._toggle = []
    def load_data(self,stationfile):
        stationdata = Station(stationfile)
        self._data.update({stationdata.get_name():stationdata})
        self._toggle.append(True)
    def get_data(self):
        return self._data
    def get_stations(self):
        self._stations = list(self._data.keys())
        return self._stations
    def get_ranges(self):
        temperaturerange = []
        yearlist = []
        for i in self._stations:
            yearlist.append(self._data[i].get_year_range())
            temperaturerange.append(self._data[i].get_temp_range())
        for i in yearlist:
            for n in i:
                self._years.append(n)
        for i in temperaturerange:
            for n in i:
                self._temp.append(n)
        self._range = (min(self._years), max(self._years),min(self._temp),max(self._temp))
        return self._range
    def is_selected(self,i):
        return self._toggle[i]
    def toggle_selected(self,i):
        self._toggle[i] = not self._toggle[i]

        

class Plotter(tk.Canvas):
    SIZE = 230
    def __init__(self,master):
        master.title("Plot")
        super().__init__(master, bg="white", width=self.SIZE, \
                         height=self.SIZE)
        
class SelectionFrame(tk.Frame):
    def __init__(self,master):
        master.title("Selection")
        super().__init__(self, master)
    #need check boxes for each station which correlated to the toggle thing
        
class DataFrame(object):
    def __init__(self):
        pass

class TemperaturePlotApp():
    def __init__(self):
        pass
        #need a button for file
