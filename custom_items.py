from tkinter import *

class CustomAverage():

    def __init__(self, master, name_1, name_2):
        self.master = master
        self.name_1 = name_1
        self.name_2 = name_2

    def render(self, target_1, target_2, _row = 0, _column = 0):
        self.master.grid_columnconfigure(0, weight=1)
        l1 = Label(self.master, text = self.name_1, background = "white")
        l1.grid(row = 0, column = 1)
        l2 = Label(self.master,
            textvariable = target_1,
            background = "white",
            width = 8)
        l2.grid(row = 0, column = 2)
        b1 = Frame(self.master, bg = "black", height = 20, width = 1)
        b1.grid(row = 0, column = 3, padx = 10)
        l3 = Label(self.master, text = self.name_2, background = "white")
        l3.grid(row = 0, column = 4)
        l4 = Label(self.master,
            textvariable = target_2,
            background = "white",
            width = 8)
        l4.grid(row = 0, column = 5)

class CustomCrawler():

    def __init__(self, master, name, point, validate_command, action_command):
        self.master           = master
        self.name             = name
        self.validate_command = validate_command
        self.action_command   = action_command
        self.point            = point

    def run(self, target):
        self.validate_command(target)
        self.action_command()


    def add(self, target, value):
        target.set(target.get() + value)
        self.run(target)


    def render(self, target, _row = 0, _column = 0, editable = True):
        self.master.grid_columnconfigure(0, weight=1)
        self.lpe_label = Label(self.master, text = self.name, bg = "white")
        self.lpe_label.grid(row = _row, column = _column + 1)
        self.lpe_dw_ten = Button(self.master,
            text = "-10",
            command = lambda: self.add(self.point, - 10),
            highlightbackground = "white",
            activebackground = '#64b6ac')
        self.lpe_dw_ten.grid(row = _row, column = _column + 2)
        self.lpe_dw = Button(self.master,
            text = "-1",
            command = lambda: self.add(self.point, - 1),
            highlightbackground = "white",
            activebackground = '#64b6ac')
        self.lpe_dw.grid(row = _row, column = _column + 3)
        if editable:
            self.lpe = Entry(self.master,
            textvariable = target,
            width = 8,
            highlightbackground = "white")
        else:
            self.lpe = Label(self.master,
                textvariable = target,
                width = 8,
                background = "white")
        self.lpe.bind("<FocusOut>", lambda e: self.run(self.point))
        self.lpe.bind("<Return>", lambda e: self.run(self.point))
        self.lpe.grid(row = _row, column = _column + 4)
        self.lpe_up = Button(self.master,
            text = "+1",
            command = lambda: self.add(self.point, 1),
            highlightbackground = "white",
            activebackground = '#64b6ac')
        self.lpe_up.grid(row = _row, column = _column + 5)
        self.lpe_up_ten = Button(self.master,
            text = "+10",
            command = lambda: self.add(self.point, 10),
            highlightbackground = "white",
            activebackground = '#64b6ac')
        self.lpe_up_ten.grid(row = _row, column = _column + 6)
        

class CustomRange():
    
    def __init__(self, master, max_size, action_command):
        self.max_size = max_size
        self.lp = IntVar()
        self.hp = IntVar()
        self.lp.set(1)
        self.hp.set(max_size)
        self.action_command = action_command

        self.lpe_crawler = CustomCrawler(master, "Low point:", self.lp,
            self.validate, self.action_command)
        self.hpe_crawler = CustomCrawler(master, "High point:", self.hp,
            self.validate, self.action_command)
    

    def validate(self, target):
        if self.lp.get() >= self.hp.get() and target == self.lp:
            self.lp.set(self.hp.get() - 1)
        if self.lp.get() <= 0:
            self.lp.set(1)
        if self.hp.get() <= self.lp.get() and target == self.hp:
            self.hp.set(self.lp.get() + 1)
        if self.hp.get() > self.max_size:
            self.hp.set(self.max_size)


    def render(self, _row = 0, _column = 0):
        self.lpe_crawler.render(self.lp, _row + 1, _column)
        self.hpe_crawler.render(self.hp, _row + 2, _column)


class CustomRangeTime(CustomRange):

    def __init__(self, master, max_size, action_command, times, name):
        self.max_size = max_size
        self.lp = IntVar()
        self.hp = IntVar()
        self.lp_label = StringVar()
        self.hp_label = StringVar()
        self.lp.set(0)
        self.hp.set(max_size)
        self.lp_label.set(times[self.lp.get()])
        self.hp_label.set(times[self.hp.get()])
        self.action_command = action_command

        self.lpe_crawler = CustomCrawler(master, "Start: " + name, self.lp,
            self.validate, self.action_command)
        self.hpe_crawler = CustomCrawler(master, "End: " + name, self.hp,
            self.validate, self.action_command)
    

    def validate(self, target):
        if self.lp.get() >= self.hp.get() and target == self.lp:
            self.lp.set(self.hp.get() - 1)
        if self.lp.get() < 0:
            self.lp.set(0)
        if self.hp.get() <= self.lp.get() and target == self.hp:
            self.hp.set(self.lp.get() + 1)
        if self.hp.get() > self.max_size:
            self.hp.set(self.max_size)


    def render(self, _row = 0, _column = 0):
        self.lpe_crawler.render(self.lp_label, _row + 1, editable = False)
        self.hpe_crawler.render(self.hp_label, _row + 2, editable = False)