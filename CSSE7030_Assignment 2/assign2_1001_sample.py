###################################################################
#
#   CSSE1001/7030 - Assignment 2
#
#   Student Number: 
#
#   Student Name: 
#
###################################################################

#
# Do not change the following import
#

from assign2_support import *

####################################################################
#
# Insert your code below
#
####################################################################

class PVData(object): 
    """
    Holds the PV data for a given date.
    """

    def __init__(self):
        """
        Initializes the PV data to use yesterday's data.

        Constructor: PVData.__init__()
        """

        self._date = None
        self.change_date(yesterday())


    def change_date(self, date):
        """
        Changes the data to be for the given date (making this date the 'current date').

        PVData.change_date(str) -> None
        """

        # Do nothing if the date has not changed.
        if date == self._date:
            return

        data = load_data(date)

        # Process data
        self._times = times = []
        self._temperatures = temperatures = []
        self._sunlights = sunlights = []
        self._powers = powers = {}

        for array in ARRAYS:
            powers[array] = []

        for time, temp, sun, power in data:
            times.append(time)
            temperatures.append(temp)
            sunlights.append(sun)

            for i, array_power in enumerate(power):
                array = ARRAYS[i]
                powers[array].append(array_power)

        self._date = date

    def get_date(self):
        """
        Returns the date for the stored data.

        PVData.get_date() -> str
        """

        return self._date

    def get_time(self, time_index):
        """
        Returns the time for the given index of the time data.

        PVData.get_time(int) -> str

        Precondition: time_index is a valid index in the range of the data.
        """

        return self._times[time_index]

    def get_temperature(self):
        """
        Returns the list of temperature values for the current date.

        PVData.get_temperature() -> [float]
        """

        return self._temperatures

    def get_sunlight(self):
        """
        Returns the list of sunlight values for the current date.

        PVData.get_sunlight() -> [float]
        """

        return self._sunlights

    def get_power(self, array):
        """
        Returns the list of power output for the current date and the the given
        array (the array name).

        PVData.get_power(str) -> [int]

        Precondition: array is exists in the list of ARRAYS.
        """

        return self._powers[array]

class Plotter(Canvas):
    """
    Handles plotting of PV data on-screen.
    """

    def __init__(self, master, pvd, line_fn):
        """
        Initializes the Plotter.

        Constructor: Plotter.__init__(Frame, PVData, function)
        """

        # Perform Canvas setup
        Canvas.__init__(self, master)

        self._pvd = pvd

        # Initialize the coordinate translator
        self._ct = CoordinateTranslator(self.winfo_width(), self.winfo_height(),
                len(pvd.get_temperature()))

        self._line = None

        # Bind to mouse events
        self.bind("<Button-1>", self._draw_line)
        self.bind("<B1-Motion>", self._draw_line)
        self.bind("<ButtonRelease-1>", self._clear_line)

        # Store the function to be run when the line moves (including
        # created/deleted)
        self._line_fn = line_fn

    def _draw_line(self, ev):
        """
        Draws a vertical line at the current cursor position, removing the
        previously drawn one if it exists.

        Plotter._draw_line(Event)
        """

        # Remove the line if it is on the screen
        if self._line is not None:
            self.delete(self._line)
            self._line = None

        # Ensure that cursor is on the canvas (in the x direction)
        if 0 <= ev.x < self.winfo_width():
            coords = [(ev.x, 0), (ev.x, self.winfo_height())]

            self._line = self.create_line(coords)

            self._line_fn(self._ct.get_index(ev.x))

    def _clear_line(self, ev):
        """
        Removes the vertical line at the current cursor position.

        Plotter._clear_line(Event)
        """

        self.delete(self._line)
        self._line = None

        self._line_fn()

    def refresh(self, power_on, temp_on, sun_on, array):
        """
        Refreshes the plot.

        Plotter.refresh(bool, bool, bool, str) -> None
        """

        self._ct.resize(self.winfo_width(), self.winfo_height())

        # Clear the plot
        self.delete(ALL)

        if power_on:
            self._plot_power(array)

        if temp_on:
            self._plot_temperature()

        if sun_on:
            self._plot_sunlight()

    def _plot_power(self, array):
        """
        Plots the power data.
        """

        coords = []

        for i, power in enumerate(self._pvd.get_power(array)):
            x, y = self._ct.power_coords(i, power, array)
            coords.append( (x, y) )

        width, height = self.winfo_width(), self.winfo_height()

        # Add bottom-right and bottom-left hand corner to close polygon
        coords.extend([(width, height), (0, height)])

        self.create_polygon(coords, fill='purple')
            

    def _plot_temperature(self):
        """
        Plots the temperature data.
        """

        coords = []

        for i, temp in enumerate(self._pvd.get_temperature()):
            x, y = self._ct.temperature_coords(i, temp)
            coords.append( (x, y) )

        self.create_line(coords, fill='red')

    def _plot_sunlight(self):
        """
        Plots the sunlight data.
        """

        coords = []

        for i, sun in enumerate(self._pvd.get_sunlight()):
            x, y = self._ct.sunlight_coords(i, sun)
            coords.append( (x, y) )

        self.create_line(coords, fill='orange')





class OptionsFrame(Frame):
    """
    Widget used for choosing options for displaying PV data on-screen.
    """

    def __init__(self, master, change_fn, power_on = True, temp_on = False,
            sun_on = False, date = None):
        """
        Initializes the OptionsFrame.

        Constructor: OptionsFrame.__init__(Frame, function, bool, bool, bool)
        """

        # Perform Frame setup
        Frame.__init__(self, master)

        # Remember the change handling function
        self._change_fn = change_fn


        # Create the widgets

        frame1 = Frame(self)
        frame2 = Frame(self)

        # Setup the power checkbutton
        # Create a variable to store the state of the checkbutton.
        self._power = power = BooleanVar(value = power_on)
        # Create the checkbutton
        self._power_btn = power_btn = Checkbutton(frame1, text = 'Power',
                variable = power, command = self._handle_change)

        # Setup the temperature checkbutton
        self._temp = temp = BooleanVar(value = temp_on)
        self._temp_btn = temp_btn = Checkbutton(frame1,
                text = 'Temperature', variable = temp,
                command = self._handle_change)

        # Setup the sunlight checkbutton
        self._sun = sun = BooleanVar(value = sun_on)
        self._sun_btn = sun_btn = Checkbutton(frame1,
                text = 'Sunlight', variable = sun,
                command = self._handle_change)

        power_btn.pack(side = LEFT)
        temp_btn.pack(side = LEFT)
        sun_btn.pack(side = LEFT)

        self._date = date = StringVar(value = date)
        self._date_ent = date_ent = Entry(frame2, textvariable = date)

        date_lbl = Label(frame2, text = 'Choose Date: ')
        date_btn = Button(frame2, text = 'Apply',
                command = self._handle_date_change)

        self._array = array = StringVar(value = ARRAYS[-1])
        self._array_menu = array_menu = OptionMenu(frame2, array, *ARRAYS,
                command = self._handle_change)


        date_lbl.pack(side = LEFT)
        date_ent.pack(side = LEFT)
        date_btn.pack(side = LEFT)
        array_menu.pack(side = RIGHT)


        frame1.pack(side = TOP, anchor = N)
        frame2.pack(side = TOP, expand = True, fill = X)



    def _handle_change(self, ev = None):
        # Note: ev = None allows function to be used as op._handle_change() or
        # op._handle_change(ev) without throwing an error for invalid number of
        # arguments, so this callback can be used for the checkbuttons and the
        # optionsmenu.
        """
        Handles a change in one of the options widgets.

        OptionsFrame._handle_change(Event) -> None
        """

        self._change_fn()

    def _handle_date_change(self):
        """
        Handles an attempt to apply a new date.

        OptionsFrame._handle_date_change(Event) -> None
        """
        
        self._change_fn(self._date.get())


    def get_state(self):
        """
        Returns the current configuration state of the OptionsFrame, in the
        form (power_on, temp_on, sun_on, array).

        OptionsFrame.get_state() -> (bool, bool, bool, str)
        """

        power_on = self._power.get()
        temp_on = self._temp.get()
        sun_on = self._sun.get()
        array = self._array.get()

        return (power_on, temp_on, sun_on, array)


class PVPlotApp(object):
    """
    Top-level class for the GUI.
    """
    def __init__(self, master):
        """
        Initializes the PVPlotApp

        Constructor: PVPlotApp.__init__()
        """

        self._master = master

        master.minsize(600, 400)

        self._pvd = pvd = PVData()

        self._info_label = info_label = Label(master)
        self._optframe = optframe = OptionsFrame(master, self._handle_change,
                date = pvd.get_date())
        self._plotter = plotter = Plotter(master, pvd,
                self._update_date_label)

        info_label.pack(side=TOP, anchor=W)
        plotter.pack(side=TOP, expand = True, fill = BOTH)
        optframe.pack(side=TOP, fill = BOTH)

        self._plotter.refresh(*self._optframe.get_state())
        self._update_date_label()

        plotter.bind("<Configure>", self._resize)

    def _handle_change(self, date = None):
        """
        Callback to handle change in OptionsFrame configuration and update the
        Plotter accordingly.

        PVPlotApp._handle_change(date) -> None
        """

        if date is not None:
            # Attempt to change date
            try:
                self._pvd.change_date(date)
            except ValueError as e:
                tkMessageBox.showerror('Date Error', str(e))
                return
            self._update_date_label()

        # Get the state of the OptionsFrame
        power_on, temp_on, sun_on, array = self._optframe.get_state()

        # Refresh the plotter
        self._plotter.refresh(power_on, temp_on, sun_on, array)

    def _update_date_label(self, index = None):
        """
        Updates the info label to reflect the data at the given index.

        PVPlotApp._update_date_label(date) -> None
        """

        power_on, temp_on, sun_on, array = self._optframe.get_state()

        date = self._pvd.get_date()

        if index is not None:
            time = self._pvd.get_time(index)
            power = self._pvd.get_power(array)[index] if power_on else None
            temp = self._pvd.get_temperature()[index] if temp_on else None
            sun = self._pvd.get_sunlight()[index] if sun_on else None

            text = pretty_print_data(date, time, temp, sun, power)
        else:
            text = pretty_print_data(date, None, None, None, None)
        self._info_label.configure(text = text)

    def _resize(self, ev):
        """
        Callback to refresh the plotter when the window is resized.

        PVPlotApp._resize(Event) -> None
        """

        self._plotter.refresh(*self._optframe.get_state())


####################################################################
#
# WARNING: Leave the following code at the end of your code
#
# DO NOT CHANGE ANYTHING BELOW
#
####################################################################

def main():
    root = Tk()
    app = PVPlotApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()

