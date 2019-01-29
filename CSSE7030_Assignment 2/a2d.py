from assign2_support import *

#####################################
# End of support 
#####################################

# Add your code here

class TemperatureData():
    def __init__(self):
        self._loaddata = []
        self._stations = []
        self._data = {}
        self._selected = True
        self._years = []
        self._temp = []
    def load_data(self,stationfile):
        self._loaddata.append(Station(stationfile+".txt"))
    def get_data(self):
        for i, n in enumerate(self._loaddata):
            self._data.update({self._loaddata[i].get_name():self._loaddata[i]})
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
        return (min(self._years), max(self._years),min(self._temp),\
                max(self._temp))
    def toggle_selected(self,i):
        pass
    def is_selected(self,i):
        pass

class Plotter(tk.Canvas):
    def __init__(self):
        super().__init__(self,master=None,cnf={},**kw)
    pass
