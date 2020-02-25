import tkinter as tk
from tkinter import messagebox
import random

#Load main window
class mainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Landmines for all')
        self.f = field()
        self.createMenu()
    
    def createField(self):
        return field()
        
    def createMenu(self):
        menu = tk.Menu(self)
        
        difficulty = tk.Menu(self, tearoff=0)
        difficulty.add_command(label='Easy', command=lambda: self.restart(10, 10))
        difficulty.add_command(label='Medium', command=lambda: self.restart(15, 15))
        difficulty.add_command(label='Hard', command=lambda: self.restart(30, 30))
        menu.add_cascade(label='Difficulty', menu=difficulty)
        
        menu.add_command(label='Win', command=lambda: self.f.win())
        menu.add_command(label='Restart', command=lambda: self.restart(self.f.max_x, self.f.max_y))
        self['menu'] = menu
    
    def restart(self, x, y):
        for child in self.winfo_children():
            if type(child) != tk.Menu:
                child.destroy()
        del self.f
        self.f = field(x=x, y=y)
    
    def run(self):
        self.mainloop()

#Load field
class field:
    def __init__(self, x=10, y=10):
        self.numberOfMines = x*y//5
        self.squareCount = x*y
        self.max_x = x
        self.max_y = y
        self.map = []
        for i in range(self.max_x):
            row = []
            for j in range(self.max_y):
                s = square(field=self, x=i, y=j)
                s.grid(row=i, column=j)
                row.append(s)
            self.map.append(row)

        self.coordPairs = set()
        for i in range(self.max_x):
            for j in range(self.max_y):
                self.coordPairs.add((i, j))
        self.mineCoords = set()

        self.setMines()

    def getNeighborMineCount(self, x, y):
        mineCount = 0
        for i in range(max(0, x-1), min(x+2, self.max_x)):
            for j in range(max(0, y-1), min(y+2, self.max_y)):
                if self.map[i][j].mine:
                    mineCount += 1
        return mineCount

    def setMines(self):
        for _ in range(self.numberOfMines):
            i,j = random.sample(self.coordPairs, 1)[0]
            self.mineCoords.add((i,j))
            self.coordPairs.remove((i,j))
            self.map[i][j].mine = True

    def showMines(self):
        for i in range(self.max_x):
            for j in range(self.max_y):
                s = self.map[i][j]
                if s.mine:
                    s.setSquare(text='X', bg='red', fg='red')
                s.setSquare(state='disabled')
    
    def clearEmptySpace(self, x, y):
        s = self.map[x][y]
        if s['state'] == 'disabled':
            return
        self.squareCount -= 1
        neighborMineCount = self.getNeighborMineCount(x, y)
        if neighborMineCount != 0:
            s.setSquare(state='disabled', relief='flat', text=neighborMineCount)
            if self.checkIfWin():
                tk.messagebox.showinfo(message='Congrats, you won!')
            return
        
        s.setSquare(state='disabled', relief='flat', text=' ')
        
        for i in range(max(0, x-1), min(x+2, self.max_x)):
            for j in range(max(0, y-1), min(y+2, self.max_y)):
                self.clearEmptySpace(i, j)
    
    def checkIfWin(self):
        if self.squareCount == self.numberOfMines:
            for i in range(self.max_x):
                for j in range(self.max_y):
                    if self.map[i][j].isActive():
                        self.map[i][j].setSquare(state='disabled', text='F')
            return True
        return False
        
    def win(self):
        for i in range(self.max_x):
            for j in range(self.max_y):
                if not self.map[i][j].mine:
                    self.clearEmptySpace(i, j)


class square(tk.Button):
    def __init__(self, *args, **kwargs):
        self.mine = False
        self.img = tk.PhotoImage(height=1, width=1)
        super().__init__(master=None, 
            width=20, 
            height=20,
            compound='c', 
            image=self.img,
            text=' ',
            highlightthickness=0,
            padx=0,
            pady=0,
            relief='raised'
        )

        self.x = kwargs['x']
        self.y = kwargs['y']
        self.field = kwargs['field']

        self.bind('<Button-1>', self.leftClick)
        self.bind('<Button-3>', self.rightClick)
        self.bind('<Button-2>', self.rightClick)

    def leftClick(self, event):
        if self['state'] != 'disabled':
            if self.mine:
                self.field.showMines()
                return
            if self['text'] != 'F':
                self.field.clearEmptySpace(self.x, self.y)

    def rightClick(self, event):
        if self['state'] == 'disabled':
            if self['text'] == 'F':
                self['text'] = '?'
                self['state'] = 'active'
        else:
            if self['text'] == ' ':
                self['text'] = 'F'
                self['state'] = 'disabled'
            else:
                self['text'] = ' '
                self['state'] = 'active'
    
    def isActive(self):
        return self['state'] == 'active'
        
    def setSquare(self, **kwargs):
        for k,v in kwargs.items():
            self[k] = v

if __name__ == '__main__':
    m = mainWindow()
    m.run()
