from assign2_support import *

#####################################
# End of support 
#####################################

# Add your code here

class TemperatureData():
    def __init__(self):
        self._data = {}
        self._stations = []
    def load_data(self, stationfile):
        a = Station(stationfile+".txt")
        return a
    def get_stations(self):
        stations = Station.get_name(self)
        self._stations.append(stations)
        print(self._stations)
    def get_data(self):
        pass
    def toggle_selected(self,i):
        """toggles the flag for displaying the station at index i"""
        pass
    def is_selected(self,i):
        """returns a boolean used to determine whether or not to display i"""
        pass
    def get_ranges(self):
        """returns 4 tuple form - min_year, max_year, min_temp, max_temp)"""
##        a = Station.get_year_range(self)
##        b = Station.
        pass
    
        


superAwesomeObject = Station("Brisbane.txt")
