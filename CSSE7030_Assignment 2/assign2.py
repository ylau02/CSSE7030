
###################################################################
#
#   CSSE1001/7030 - Assignment 2
#
#   Student Number: 42377***
#
#   Student Name: Joyce Lau
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
    """
    A class for loading data from a .txt file
    and for returning the data in a usable format

    
    """
    def __init__(self):
        """Constructor: TemperatureData() """
        self._stations = []
        self._data = {}
        self._toggle = []
        
    def load_data(self,stationfile):
        """
        Loads data from a selected txt file and appends
        data to the necessary lists
        load_data(str) --> None
        """
        try:
            stationdata = Station(stationfile)
            self._data.update({stationdata.get_name():stationdata})
            self._toggle.append(True)
            self._stations.append(stationdata.get_name())
        except IndexError:
            messagebox.showerror("Error",\
                                 "This file doesn't have the right data")
    def get_data(self):
        """
        Returns a dictionary of data

        get_data() --> {Station:Station(Station)}
        """
        return self._data
    def get_stations(self):
        """
        Returns a list of stations in the order loaded

        get_stations() --> [Str,str...str]
        """
        return self._stations
    def is_selected(self,i):
        """
        Returns the Boolean value of whether or not station is selected
        at the selected index 
        is_selected(i) --> Boolean Value
        """
        return self._toggle[i]
    def toggle_selected(self,i):
        """
        Toggles Boolean value of a selected station at the selected index

        toggle_selected(i) --> None
        """
        self._toggle[i] = not self._toggle[i]
    def get_ranges(self):
        """
        Returns a tuple containing the minimum year, maximum year,
        minimum temperature, maximum temperature ranges of the loaded station

        get_ranges() --> (int,int,int,int)
        """
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
    """
    A class that inherits from the Tkinter class of Canvas.

    This class allows the plotting of graphs in the application
    and retrieves the temperature and year for a given set of
    co-ordinates. It also draws a line of best fit between two
    selected years. 

    """
    def __init__(self,master,data):  
        """ Constructor: Plotter(master, data)"""
        super().__init__(master, bg="white")
        master.title("Plotter")
        #self._data is loaded with data when TemperatureData()
        #is called in the TemperaturePlotApp Class
        self._data = data
        self._stations = self._data.get_stations()
        #stores the coordinatetranslator application data
        self._coord = []
        self._ranges = ()
        self._width = None
        self._height = None
        self._bfcoords = []
        self._year = None
        self._temps = []
        self._yearlist = []
    def get_coords(self):
        """
        Assigns a variable to the CoordinateTranslator app so that it can be
        called later in the class

        get_coords() --> None
        """
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
        """
        Plots the given station with the given colour.

        Plot(station,colour) --> Create Line on canvas
        """
        try:
            datapoints = []
            tempcoords = []
            station_data = self._data.get_data().get(station)
            datapoints = station_data.get_data_points()
            self.get_coords()
            for i in datapoints:
                tempcoords.append(self._coord.temperature_coords(i[0],i[1]))       
            self.create_line(tempcoords,fill=colour)
        except IndexError:
            messagebox.showerror("Index Error", "This file is out of range")

    def get_year(self,e):
        """
        Returns the given year at the selected co-ordinates\
        
        get_year(e) --> int
        """
        self._year = self._coord.get_year(e.x)
        return self._year

    def get_temps(self):
        """
        Returns the given temperatures for all loaded stations at the selected year

        get_temps() --> list(int,int...int)
        """
        self._temps = []
        for station in self._stations:
            station_data = self._data.get_data().get(station)
            self._temps.append(station_data.get_temp(self._year))
        return self._temps
    
    def draw_line(self,e):
        """
        Draws a line along the y axis at the chosen co-ordinate

        draw_line(event) --> draws a vertical line at the user's
        chosen position
        """
        try:
            self.redraw()
            coords = [(e.x, 0), (e.x, self._height)]
            self._line = self.create_line(coords)
            self.get_year(e)
            self.get_temps()
        except AttributeError:
            messagebox.showerror("Error","There is no data to display")


    def appendyear(self,e):
        """
        Appends the year at the user's chosen position to a list
        and creates a line of best fit

        appendyear(event) --> creates line of best fit
        between the specified years
        """
        if len(self._yearlist) == 2:
            self._yearlist.clear()
        if len(self._yearlist) < 2:
            self._yearlist.append(self._year)
            self.redraw()
            self.draw_line(e)



    def get_bfcoords(self,station):
        """
        Returns the coordinates required for a line of best fit

        get_bfcoords(str) --> (float,float)
        """
        self._bfcoords = []
        station_data = self._data.get_data().get(station)
        datapoints = station_data.get_data_points()
        for datatuple in datapoints:
            for n,i in enumerate(datatuple):
                for y in self._yearlist:
                    if y == i:
                        self._bfcoords.append(self._coord.temperature_coords\
                                          (datatuple[0],datatuple[1]))
        return self._bfcoords

    
    def bestfit(self):
        """
        Draw a line of best fit between two years

        bestfit() --> creates a line between two points on the canvas
        """
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
        """
        Clears the canvas and redraws stations that are TRUE

        redraw() --> deletes the canvas and replots all stations
        that are true
        """
        try:
            self.get_coords()
            self.delete(tk.ALL)
            for i, station in enumerate(self._stations):
                if self._data.is_selected(i) == True:
                    self.plot(station, COLOURS[i % len(COLOURS)])
                    self.bestfit()
        except IndexError:
            messagebox.showerror("Error","There is an Index Error")


        
class SelectionFrame(tk.Frame):
    """
    This class inherits from tkinter Frame class
    It holds the checkbuttons responsible for toggling
    each station's Boolean value
    """
    def __init__(self,master,data,plot):
        """Constructor: SelectionFrame(master,data,plot)"""
        super().__init__(master)
        self._master = master
        self._stationselect = tk.Label(master,text="Station Selection: ")
        self._stationselect.pack(side=tk.LEFT,anchor=tk.SW, pady = 20)
        #self._data is loaded with data when TemperatureData()
        #is called in the TemperaturePlotApp Class
        self._data = data
        #self._plotter is loaded when the plotter class is called
        #in the TemperaturePlotApp Class
        self._plotter = plot
        self._chk = ""
        
        

        
    def checkbutton(self,station,colour,i):
        """
       Creates a checkbutton that toggles the station's Boolean value
       and redraws the canvas to only show the True stations

       checkbutton(self,station,color,index) --> creates a checkbutton
       """
        self._chk = tk.Checkbutton(self._master, text=station,fg=colour,\
                                   command = lambda: self.toggle(i))
        self._chk.select()
        self._chk.pack(side=tk.LEFT,anchor=tk.SW, pady = 20)
      
              
    def toggle(self,i):
        """
        Calls the toggle_selected function from TemperatureData class
        to toggle the Boolean value of a station at the specified index.
        Also calls the redraw() function in the Plotter class to only
        plot stations that are TRUE.

        toggle(index) --> None
        """
        self._data.toggle_selected(i)
        self._plotter.redraw()
          
            
class DataFrame(tk.Frame):
    """
    This class inherits from the tkinter Frame class.
    This class stores the labels for the year and temperature
    at the user's specified co-ordinates.
    """
    def __init__(self,master,data):
        """Constructor: DataFrame(master,data)"""
        super().__init__(master)
        self._data = data
        self._stations = self._data.get_stations()
        #self._alreadyloaded stores a list of stations
        #that have already been loaded
        self._alreadyloaded = []
        self._year = tk.Label(master)
        self._year.pack(side = tk.TOP, anchor = tk.NW)
        self._templist = []

            
        
    def display_year(self,year):
        """
        Creates a label for the specified year

        display_year(year) --> Label for year
        """
        self._year.config(text = "Data for " + str(year)+":")

        
    def add_label(self):
        """
        Creates an empty label for each temperature at the specified year
        with its corresponding colour.
        This is dependent on how many stations have been loaded.

        add_label() --> Label for temperature
        """
        for n,s in enumerate(self._stations):
            if s not in self._alreadyloaded:
                self._alreadyloaded.append(s)
                self._temp = tk.Label(self,text = "",\
                                      fg=COLOURS[n%len(COLOURS)])
                self._temp.pack(side = tk.TOP, anchor = tk.NW)
                self._templist.append(self._temp)



        
    def display_temps(self,temps):
        """
        Changes each temperature label to display the temperature at a
        specified year and also changes the label when the user selects
        a new year.

        display_temps(temps) --> Changes the label to show new temperature
        """
        self.add_label()
        for n,s in enumerate(self._stations):
            if temps[n] == None:
                self._templist[n].config(text = "")
            self._templist[n].config(text=temps[n])
            self._templist[n].pack_configure(side=tk.LEFT)

        
        
class TemperaturePlotApp(object):
    """
    This class is the top level class for the GUI
    """
    def __init__(self, master):
        self._master = master
        master.title("Temperature Plot Application")
        #load station data from the txt file
        self._temperatureData = TemperatureData()
        self._stations = self._temperatureData.get_stations()
        #creates a drop down file menu in the GUI
        menubar = tk.Menu(master)
        master.config(menu=menubar)
        filemenu = tk.Menu(menubar)
        menubar.add_cascade(label="File",menu=filemenu)
        filemenu.add_command(label="Open",command=self.open)
        filemenu.add_command(label="Exit",command=self.close)

        master.protocol("WM_DELETE_WINDOW",self.close)
        #packs all relevant classes for the GUI
        #and organises them into the specified locations
        self._plotter = Plotter(master,self._temperatureData)
        self._plotter.pack(expand=1,fill=tk.BOTH, side=tk.TOP)
        self._plotter.bind("<Button-1>",self.draw_line)
        self._plotter.bind("<Configure>",self.resize_window)
        self._plotter.bind_all("<Key>",self._plotter.appendyear)

        self._dataframe = DataFrame(master,self._temperatureData)
        self._dataframe.pack(side = tk.TOP, anchor=tk.NW,expand=True)

        self._selectionframe = SelectionFrame(self._master,\
                                              self._temperatureData,\
                                              self._plotter)
        self._selectionframe.pack(side=tk.BOTTOM,anchor = tk.SW,expand = True)

        #stores a list of stations that have already been loaded
        self._alreadyloaded = []

    
    def open(self):
        """
        Opens a file dialog for the user to select the file.
        Calls self.checkbox() to create the checkbutton.
        for the selected file.
        Plots the data from the selected file.

        open() --> opens file dialog
        """
        try:
            filename = filedialog.askopenfilename()
            if filename:
                self._temperatureData.load_data(filename)
                self.checkbox()
                self._plotter.redraw()
        except UnicodeDecodeError:
            messagebox.showerror("Error","This file format is not supported: "\
                                 +filename)

        
    def checkbox(self):
        """
        Calls the checkbutton function from the SelectionFrame class to
        create checkbutton for the station that has been loaded
        and skips over stations that have already been loaded.

        checkbox() --> creates a checkbutton
        """
        for n,station in enumerate(self._stations):
            if station not in self._alreadyloaded:
                self._alreadyloaded.append(station)
                self._selectionframe.checkbutton(station,\
                                                 COLOURS[n % len(COLOURS)],n)
              
    def draw_line(self,e):
        """
        Calls the draw_line(event) function from the Plotter class
        to draw a line where the user specifies.
        Also creates the corresponding labels for the year and temperature
        at the specified coordinates.
        This function is bound to "<Button-1>" which is the left
        mouse click. This may require a double click when the program first
        opens.

        draw_line(event) --> draws a verticle line at specified point
        """
        self._plotter.draw_line(e)
        self._dataframe.display_year(self._plotter._year)
        self._dataframe.display_temps(self._plotter._temps)

      
    def resize_window(self,e):
        """
        Calls the redraw function from the Plotter class to
        delete everything in the canvas and redraw to fit the window
        when the user resizes the window. This is bound to "<Configure>".

        resize_window(event) --> deletes canvas and redraws to fit new coordinates
        """
        self._plotter.redraw()
              
        
    def close(self):
        """
        Closes the window when called

        close() --> close application
        """
        self._master.destroy()


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
