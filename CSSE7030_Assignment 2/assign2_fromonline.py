



###################################################################
#
#   CSSE1001 - Assignment 2
#
#   Student Number: 43229161
#
#   Student Name: Jason Ho
#
###################################################################


#
# Do not change the following import
#

import MazeGenerator

####################################################################
#
# Insert your code below
#
####################################################################

from Tkinter import *
import tkFileDialog
import tkMessageBox

class MazeApp(Frame):  
    def __init__(self, master):
        """
        """
        self._mazeGene = MazeGenerator.MazeGenerator()
        
        Frame.__init__(self, master)

        master.title("Maze Solver")
        master.minsize(300, 300)

        master.bind(self, "<Up>", self.moveplace)
        master.bind(self, "<Down>", self.moveplace)
        master.bind(self, "<Left>", self.moveplace)
        master.bind(self, "<Right>", self.moveplace)


        #Menu
        menubar = Menu(self.master)
        self.master.config(menu = menubar)
        
        File = Menu(menubar)
        menubar.add_cascade(label="File", menu=File)
        File.add_command(label="Open Maze File", command=self.openMaze)
        File.add_command(label="Save Maze File", command=self.saveMaze)
        File.add_command(label="Exit", command=self.quit)

        #Canvas

        
        self._canvas = Canvas(master, borderwidth=1,
                              relief=SUNKEN, bg = "black")
        self._canvas.pack(expand = 1, anchor = CENTER)

        #Frames and Buttons
        
        frame1 = Frame(self)
        frame2 = Frame(frame1, relief=SUNKEN, bd = 2) #borderwidth = 2
        
        self._sp = Spinbox(frame2, from_=2, to=15, width=15) #put within frame2
        self._sp.pack(side=LEFT, padx=2, pady=2)
        
        but1 = Button(frame2, text="New", command=self.new)
        but1.pack(side=LEFT, ipadx = 5)
        
        frame2.pack(side=LEFT)

        but2 = Button(frame1, text="Reset", command=self.reset)
        but2.pack(side=LEFT, ipadx = 5, padx = 20)
        
        but3 = Button(frame1, text="Quit", command=self.quit)
        but3.pack(side=LEFT, ipadx = 5, padx = 20)
     
        
        frame1.pack(side=TOP, expand=1, fill=BOTH)
        Frame.pack(self)

    def move(self, direction):
        pass

    def new(self):
        sl = int(self._sp.get())
        self._genmaze = MazeGenerator.MazeGenerator().make_maze(sl)
        Maze(self._genmaze)

    def reset(self):
        MazeGenerator.MazeGenerator()._set_square(self._mazeGene, 1, 1, 'X')
        tkMessageBox.showinfo("Reset Notification", "You have successfully reset the maze!")

    def moveplace(self): #interaction when moving for arrow keys
        pass
    
    def openMaze(self):
        filename = tkFileDialog.askopenfilename(filetypes=[('Maze File','*.txt')])
        if filename == None:
            filename = "piss off"
        else:
            fre = open(filename, "rU")
            data_list = fre.readlines() # I found this easier to work with than ''.read()
            fre.close()
            data_list = [item.rstrip('\n') for item in data_list]
            row = 0
            self._mapo = []
            for item in data_list:
                self._mapo.append(list(data_list[row]))
                row +=1
##        self.printMaze(self._mapo, (1,1))
        Maze(self._mapo)
        
    def printMaze(self, maze, position):
##        self._result = '\n'.join(''.join(str(el) for el in list) for list in maze)
##        self._result += '\n'
##        mo = list(self._result)
##        diml = (len(self._result)+1)/len(maze) #offset of last line not having \n
##        mo[diml*position[0]+position[1]] = PLAYER #position of row then column
##        self._result = ''.join(mo)
##        print self._result
        pass

    def drawMaze(self):
        
        for r in self._mapo:
            for c in self._mapo:
                self.canvas.create_rectangle(r*20, c*20, (r+1)*20, (c+1)*20)
            pass
        
##        self._canvas.create_rectangle(20,20,40,40, fill='red')
        
    def saveMaze(self): 
        pass
    
    def quit(self):
        self.master.destroy() #simple way to remove the app
        
class Maze():
    def __init__(self, string):
        """load_maze(filename)
            filename: a string of the filename of a .txt file. Eg: 'example.txt'

            Opens the .txt file, parses through, creating a list of
            lists containing the maze and symbols from the file
            This will check if it is a valid maze
        """
        #Validate Maze
        if len(string) < 3:
            try:
                raise InvalidMaze
            except Exception:
            #there may not be enough rows for
            #the player to move around in
                tkMessageBox.showwarning("Invalid Maze",
                                         "There are not enough rows to have a maze!")
##        else:
##            for list in string:
##                if len(string[0]) == len(list):
##                    pass
##                else:
##                    try:
##                        raise InvalidMaze
##                    except Exception:
##                        tkMessageBox.showwarning("Invalid Maze",
##                                             "All rows are not the same length!")
        else:
            MazeApp(self).drawMaze() # needs 2 arguments including self.
            # So what to put in MazeApp(   ) ?
        
        
    
    def __str__(self):
        print MazeApp()._result
        
    def get_size(self):
        return len(string)
    
    def get_pos(self):
        (x,y) = position
        yes = (x+DIRECTIONS[direction][0],y+DIRECTIONS[direction][1])
        return yes


class InvalidMaze(Exception):
    pass
        

    




####################################################################
#
# WARNING: Leave the following code at the end of your code
#
# DO NOT CHANGE ANYTHING BELOW
#
####################################################################

def main():
    root = Tk()
    app = MazeApp(root)
    root.mainloop()

if  __name__ == '__main__':
    main()
