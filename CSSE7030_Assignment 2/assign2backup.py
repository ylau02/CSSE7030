
###################################################################
#
#   CSSE1001/7030 - Assignment 2
#
#   Student Number: 42377029
#
#   Student Name: Joyce Wing Yan Lau
#
###################################################################

#####################################
# Support given below - DO NOT CHANGE
#####################################

from assign2_support import *

#####################################
# End of support 
#####################################

# Add your code here

import tkinter as tk
import os.path
from tkinter import filedialog
from tkinter import messagebox

class TemperatureData(object):
    def __init__(self):
        self._stations = []
        self._data = {}
        self._toggle = []
    def load_data(self,stationfile):
        stationdata = Station(stationfile)
        self._data.update({stationdata.get_name():stationdata})
        self._toggle.append(True)
        self._stations.append(stationdata.get_name())
    def get_data(self):
        return self._data
    def get_stations(self):
        return self._stations
    def is_selected(self,i):
        return self._toggle[i]
    def toggle_selected(self,i):
        self._toggle[i] = not self._toggle[i]
    def get_ranges(self):
        temperatures = []
        years = []
        temperaturelist = []
        yearlist = []
        try:
            for i in self._stations:
                yearlist.append(self._data[i].get_year_range())
                temperaturelist.append(self._data[i].get_temp_range())
            for i in yearlist:
                for n in i:
                    years.append(n)
            for i in temperaturelist:
                for n in i:
                    temperatures.append(n)
            temp_range = (min(years), max(years),\
                       min(temperatures),max(temperatures))
            return temp_range
        except ValueError:
            pass

        

class Plotter(tk.Canvas):
    def __init__(self,master,data):
        super().__init__(master, bg="white")
        master.title("Plotter")
        self._data = data
        self._stations = self._data.get_stations()
        self._coord = []
        self._ranges = ()
        self._width = None
        self._height = None
        self._line = None
##        self._bestfitline = None
        self._bfcoords = []

        self._year = None
        self._temps = []
        self._yearlist = []
    def get_coords(self):
        try:
            self._ranges = self._data.get_ranges()
            self._width = self.winfo_width()
            self._height = self.winfo_height()
            self._coord = CoordinateTranslator(self._width,\
                                               self._height,\
                                               self._ranges[0],\
                                               self._ranges[1],\
                                               self._ranges[2],\
                                               self._ranges[3])
            self._stations = self._data.get_stations()
        except TypeError:
            pass
        

        
    def plot(self,station,colour):
        datapoints = []
        tempcoords = []
        station_data = self._data.get_data().get(station)
        datapoints = station_data.get_data_points()
        self.get_coords()
        for i in datapoints:
            tempcoords.append(self._coord.temperature_coords(i[0],i[1]))       
        self.create_line(tempcoords,fill=colour)

    def get_year(self,e):
        self._year = self._coord.get_year(e.x)
        print(self._year)
        return self._year

    def get_temps(self):
        self._temps = []
        for station in self._stations:
            station_data = self._data.get_data().get(station)
            self._temps.append(station_data.get_temp(self._year))
        print(self._temps)
        return self._temps
    
    def draw_line(self,e):

        if self._line is not None:
            self.delete(self._line)
            self._line = None
            
        if 0 <= e.x < self._width:
            coords = [(e.x, 0), (e.x, self._height)]

            self._line = self.create_line(coords)
        self.get_year(e)
        self.get_temps()


    def appendyear(self,e):
        if len(self._yearlist) == 2:
            self._yearlist.clear()
        if len(self._yearlist) < 2:
            self._yearlist.append(self._year)
            self.redraw()
            self.draw_line(e)



    def get_bfcoords(self,station):
        self._bfcoords = []
        station_data = self._data.get_data().get(station)
        datapoints = station_data.get_data_points()
        for datatuple in datapoints:
            for n,i in enumerate(datatuple):
                for y in self._yearlist:
                    if y == i:
                        self._bfcoords.append(self._coord.temperature_coords\
                                          (datatuple[0],datatuple[1]))


    
    def bestfit(self):
        try:
            
            for n, station in enumerate(self._stations):
                self.get_bfcoords(station)
                if self._data.is_selected(n) == True:
                    bfcoords = best_fit(self._bfcoords)
                    self._bestfitline = self.create_line(bfcoords,\
                                                     fill = COLOURS[n % len(COLOURS)]\
                                                     ,width = 2)
        except ZeroDivisionError:
            pass            
    
        
    def redraw(self):
        self.get_coords()
        self.delete(tk.ALL)
        for i, station in enumerate(self._stations):
            if self._data.is_selected(i) == True:
                self.plot(station, COLOURS[i % len(COLOURS)])
                self.bestfit()


        
class SelectionFrame(tk.Frame):
    def __init__(self,master,data,plot):
        super().__init__(master)
        self._master = master
        self._stationselect = tk.Label(master,text="Station Selection: ")
        self._stationselect.pack(side=tk.LEFT,anchor=tk.SW)
        self._data = data
        self._chk = ""
        self._chklist = []
        self._plotter = plot
        

        
    def checkbutton(self,station,colour,i):
        self._chk = tk.Checkbutton(self._master, text=station,fg=colour,\
                                   command = lambda: self.toggle(i))
        self._chk.select()
        self._chk.pack(side=tk.LEFT,anchor=tk.SW)
      
              
    def toggle(self,i):
        self._data.toggle_selected(i)
        self._plotter.redraw()
        print(self._data.is_selected(i))
        print(self._data._toggle)


            
            
class DataFrame(tk.Frame):
    def __init__(self,master,data):
        super().__init__(master)
        self._data = data
        self._stations = self._data.get_stations()
        self._year = None
        self._year = tk.Label(master)
        self._year.pack(side = tk.TOP, anchor = tk.NW)
        self._templist = []
        self._alreadyloaded = []
            
        
    def display_year(self,year):

        self._year.config(text = "Data for " + str(year)+":")

        
    def add_label(self):

        for n,i in enumerate(self._stations):
            if i not in self._alreadyloaded:
                self._alreadyloaded.append(i)
                self._temp = tk.Label(self,text = "",fg=COLOURS[n%len(COLOURS)])
                self._temp.pack(side = tk.LEFT)
                self._templist.append(self._temp)



        
    def display_temps(self,temps):       
        self.add_label()
        for n,s in enumerate(self._stations):
            self._templist[n].config(text=temps[n])

        
        
class TemperaturePlotApp(object):
    def __init__(self, master):
        self._master = master
        master.title("Temperature Plot Application")
        self._temperatureData = TemperatureData()
        self._stations = self._temperatureData.get_stations()
        
        menubar = tk.Menu(master)
        master.config(menu=menubar)
        filemenu = tk.Menu(menubar)
        menubar.add_cascade(label="File",menu=filemenu)
        filemenu.add_command(label="Open",command=self.open)
        filemenu.add_command(label="Exit",command=self.close)

        master.protocol("WM_DELETE_WINDOW",self.close)
        
        self._plotter = Plotter(master,self._temperatureData)
        self._plotter.pack(expand=1,fill=tk.BOTH, side=tk.TOP)
        self._plotter.bind("<Button-1>",self.draw_line)
        self._plotter.bind("<Configure>",self.resize_window)
        self._plotter.bind("<Button-3>",self._plotter.appendyear)

        self._dataframe = DataFrame(master,self._temperatureData)
        self._dataframe.pack(side = tk.TOP,anchor=tk.NW)

        self._selectionframe = SelectionFrame(self._master,\
                                              self._temperatureData,\
                                              self._plotter)
        self._selectionframe.pack(expand=1, side=tk.TOP,anchor = tk.SW)


        self._alreadyloaded = []

    
    def open(self):
        filename = filedialog.askopenfilename()
        if filename:
            self._temperatureData.load_data(filename)
            self.checkbox()
            self._plotter.redraw()

        
    def checkbox(self):
        for n,station in enumerate(self._stations):
            if station not in self._alreadyloaded:
                self._alreadyloaded.append(station)
                self._selectionframe.checkbutton(station,\
                                                 COLOURS[n % len(COLOURS)],n)
              
    def draw_line(self,e):
        self._plotter.draw_line(e)
        self._dataframe.display_year(self._plotter._year)
        self._dataframe.display_temps(self._plotter._temps)

      
    def resize_window(self,e):
        self._plotter.redraw()
        
    def close(self):
            self._master.destroy()

#resize window

##################################################
# !!!!!! Do not change (or add to) the code below !!!!!
###################################################

def main():
    root = tk.Tk()
    app = TemperaturePlotApp(root)
    root.geometry("800x400")
    root.mainloop()

if __name__ == '__main__':
    main()
