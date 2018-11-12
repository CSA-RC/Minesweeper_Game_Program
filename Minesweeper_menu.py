"""Minesweeper version 0.2.2 made by Ryan Callahan"""

from tkinter import *
from tkinter import ttk
import random
import time

root = Tk()

class Minesweeper:

    def __init__ (self, root):
        root.title("Minesweeper")
        self.button_dict = dict()

        self.label = Label(text="MINESWEEPER\n-------------\nChoose A Difficulty\n-------------")
        self.label.grid(columnspan=3, column=1, row=1, sticky='w')
        self.easystart = Button(text="Easy", command=self.easy)
        self.easystart.grid(column=1, row=2)
        self.mediumstart = Button(text="Medium", command=self.medium)
        self.mediumstart.grid(column=2, row=2)
        self.hardstart = Button(text="Hard", command=self.hard)
        self.hardstart.grid(column=3, row=2)

        self.mine = 1
        self.size = 5
        self.mlist = []
        self.mines = []

    def easy(self):
        self.mine = 20
        self.size = 10
        self.label.destroy()
        self.easystart.destroy()
        self.mediumstart.destroy()
        self.hardstart.destroy()
        self.create()

    def medium(self):
        self.mine = 45
        self.size = 15
        self.label.destroy()
        self.easystart.destroy()
        self.mediumstart.destroy()
        self.hardstart.destroy()
        self.create()

    def hard(self):
        self.mine = 80
        self.size = 20
        self.label.destroy()
        self.easystart.destroy()
        self.mediumstart.destroy()
        self.hardstart.destroy()
        self.create()

    def create(self):
        self.minecount = self.mine
        self.flagcount = self.mine
        for x in range(0, self.size):
            for y in range(0, self.size):
                self.mlist.append([x, y])

        for x in range(0, self.size):
            for y in range(0, self.size):
                self.button_dict[f"{x}, {y}"] = Button(text="", height=1, width=2)
                self.button_dict[f"{x}, {y}"].bind("<ButtonPress-1>", self.minesweeperclick)
                self.button_dict[f"{x}, {y}"].bind("<ButtonRelease-3>", self.flag)
                self.button_dict[f"{x}, {y}"].grid(column=x, row=y)

        for x in range(0, self.mine):
            self.minegenerate()

        self.buttonlabel=Label(text=("Flags Remaining: %s" % self.flagcount))
        self.buttonlabel.grid(columnspan=10, column=1, row=999, sticky="ew")

    def minegenerate(self):
        x, y = random.choice(self.mlist)
        self.mines.append(self.button_dict[f"{x}, {y}"])
        self.button_dict[f"{x}, {y}"].unbind("<ButtonPress-1>")
        self.button_dict[f"{x}, {y}"].bind("<ButtonPress-1>", self.boom)
        self.mlist.remove([x, y])
        #self.button_dict[f"{x}, {y}"].config(text="m")

    def boom(self, event):
        for button in self.button_dict.values():
            button.update()
            root.update()
            button_geo, button_x, button_y = button.winfo_geometry().split("+")
            button_length, button_height = button_geo.split("x")
            root_x, root_y = root.winfo_rootx(), root.winfo_rooty()
            x = int(event.x_root) - int(root_x)
            y = int(event.y_root) - int(root_y)
            if x in range(int(button_x), (int(button_x) + int(button_length)))\
                    and y in range(int(button_y), (int(button_y) + int(button_height))):
                button.config(state="disabled", relief="sunken", text="*")
                root.update()
                self.losescreen()
                break

    def losescreen(self):
        lose = Toplevel()
        lose.geometry('50x50')
        lose.title("Minesweeper")
        msg = Message(lose, text="You Lose.")
        msg.pack()
        closebutton = Button(lose, text="Close", command = self.close)
        closebutton.pack()

    def flag(self, event):
        for button in self.button_dict.values():
            button.update()
            root.update()
            button_geo, button_x, button_y = button.winfo_geometry().split("+")
            button_length, button_height = button_geo.split("x")
            root_x, root_y = root.winfo_rootx(), root.winfo_rooty()
            x = int(event.x_root) - int(root_x)
            y = int(event.y_root) - int(root_y)
            if x in range(int(button_x), (int(button_x) + int(button_length)))\
                    and y in range(int(button_y), (int(button_y) + int(button_height))):
                if self.flagcount > 0:
                    button.config(relief="ridge", state="disabled", text="F")
                    self.flagcount -= 1
                    self.buttonlabel.config(text=("Flags Remaining: %s" % self.flagcount))
                if button in self.mines:
                    self.minecount -= 1
                    if self.minecount == 0:
                        self.winscreen()
                        break
                button.unbind("<ButtonPress-1>")
                button.unbind("<ButtonRelease-3>")
                button.bind("<ButtonRelease-3>", self.unflag)

    def winscreen(self):
        win = Toplevel()
        win.geometry('50x65')
        win.title("Minesweeper")
        msg = Message(win, text="You Win!")
        msg.pack()
        closebutton = Button(win, text="Close", command = self.close)
        closebutton.pack()

    def close(self):
        root.destroy()


    def unflag(self, event):
        for button in self.button_dict.values():
            button.update()
            root.update()
            button_geo, button_x, button_y = button.winfo_geometry().split("+")
            button_length, button_height = button_geo.split("x")
            root_x, root_y = root.winfo_rootx(), root.winfo_rooty()
            x = int(event.x_root) - int(root_x)
            y = int(event.y_root) - int(root_y)
            if x in range(int(button_x), (int(button_x) + int(button_length)))\
                    and y in range(int(button_y), (int(button_y) + int(button_height))):
                self.flagcount += 1
                self.buttonlabel.config(text=("Flags Remaining: %s" % self.flagcount))
                button.config(relief="raised", state="disabled", text="")
                button.unbind("<ButtonRelease-3>")
                button.bind("<ButtonPress-1>", self.minesweeperclick)
                button.bind("<ButtonRelease-3>", self.flag)


    def minesweeperclick(self, event):
        for button in self.button_dict.values():
            button.update()
            root.update()
            button_geo, button_x, button_y = button.winfo_geometry().split("+")
            button_length, button_height = button_geo.split("x")
            root_x, root_y = root.winfo_rootx(), root.winfo_rooty()
            x = int(event.x_root) - int(root_x)
            y = int(event.y_root) - int(root_y)
            if x in range(int(button_x), (int(button_x) + int(button_length)))\
                    and y in range(int(button_y), (int(button_y) + int(button_height))):
                button.config(state="disabled", relief="sunken")
                button.unbind("<ButtonRelease-3>")
                self.numbertest(button)

    def numbertest(self, button):
        adjacentmines = 0
        for list in self.button_dict.items():
            if button in list:
                x, y = list[0].split(", ")
                try:
                    if self.button_dict[f"{str(int(x)-1)}, {str(int(y)+1)}"] in self.mines:
                        adjacentmines += 1
                except KeyError:
                    pass
                try:
                    if self.button_dict[f"{str(int(x)-1)}, {y}"] in self.mines:
                        adjacentmines += 1
                except KeyError:
                    pass
                try:
                    if self.button_dict[f"{str(int(x)-1)}, {str(int(y)-1)}"] in self.mines:
                        adjacentmines += 1
                except KeyError:
                    pass
                try:
                    if self.button_dict[f"{x}, {str(int(y)-1)}"] in self.mines:
                        adjacentmines += 1
                except KeyError:
                    pass
                try:
                    if self.button_dict[f"{x}, {str(int(y)+1)}"] in self.mines:
                        adjacentmines += 1
                except KeyError:
                    pass
                try:
                    if self.button_dict[f"{str(int(x)+1)}, {str(int(y)+1)}"] in self.mines:
                        adjacentmines += 1
                except KeyError:
                    pass
                try:
                    if self.button_dict[f"{str(int(x)+1)}, {y}"] in self.mines:
                        adjacentmines += 1
                except KeyError:
                    pass
                try:
                    if self.button_dict[f"{str(int(x)+1)}, {str(int(y)-1)}"] in self.mines:
                        adjacentmines += 1
                except KeyError:
                    pass
                if adjacentmines == 0:
                    button.config(relief="sunken", text="", state="disabled")
                    self.blankspacecalculate(button)
                else:
                    button.config(relief="sunken", text=adjacentmines, state="disabled")

    def blankspacecalculate(self, button):
        for list in self.button_dict.items():
            if button in list:
                x, y = list[0].split(", ")
                try:
                    if self.button_dict[f"{int(x)-1}, {int(y)+1}"].cget("relief") == "raised":
                        self.numbertest(self.button_dict[f"{int(x)-1}, {int(y)+1}"])
                except KeyError:
                    pass
                try:
                    if self.button_dict[f"{int(x)-1}, {y}"].cget("relief") == "raised":
                        self.numbertest(self.button_dict[f"{int(x)-1}, {y}"])
                except KeyError:
                    pass
                try:
                    if self.button_dict[f"{int(x)-1}, {int(y)-1}"].cget("relief") == "raised":
                        self.numbertest(self.button_dict[f"{int(x)-1}, {int(y)-1}"])
                except KeyError:
                    pass
                try:
                    if self.button_dict[f"{x}, {str(int(y)+1)}"].cget("relief") == "raised":
                        self.numbertest(self.button_dict[f"{x}, {str(int(y)+1)}"])
                except KeyError:
                    pass
                try:
                    if self.button_dict[f"{x}, {str(int(y)-1)}"].cget("relief") == "raised":
                        self.numbertest(self.button_dict[f"{x}, {str(int(y)-1)}"])
                except KeyError:
                    pass
                try:
                    if self.button_dict[f"{str(int(x)+1)}, {str(int(y)+1)}"].cget("relief") == "raised":
                        self.numbertest(self.button_dict[f"{str(int(x)+1)}, {str(int(y)+1)}"])
                except KeyError:
                    pass
                try:
                    if self.button_dict[f"{str(int(x)+1)}, {y}"].cget("relief") == "raised":
                        self.numbertest(self.button_dict[f"{str(int(x)+1)}, {y}"])
                except KeyError:
                    pass
                try:
                    if self.button_dict[f"{str(int(x)+1)}, {str(int(y)-1)}"].cget("relief") == "raised":
                        self.numbertest(self.button_dict[f"{str(int(x)+1)}, {str(int(y)-1)}"])
                except KeyError:
                    pass


Minesweeper(root)
root.mainloop()
