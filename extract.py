# -*- coding: utf-8 -*-
import os
import xlsxwriter
import numpy as np
from tkinter import *
from ttk import Style
from custom_items import *
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
import matplotlib.transforms as mtransforms
from matplotlib.backend_bases import key_press_handler
from tkfilebrowser import askopendirnames, asksaveasfilename
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

class Application(Frame):
    def __init__(self, master = None):
        self.master       = master
        self.system_size  = 100
        self.directories  = None
        self.reset_data()

        self.f1 = Frame(self.master, bg = "white", width = 500, height = 500)
        self.f2 = Frame(self.f1,     bg = "white", width = 500, height = 500)
        self.f3 = Frame(self.f1,     bg = "white", width = 500, height = 500)
        self.f4 = Frame(self.f1,     bg = "white", width = 500, height = 500)
        self.f5 = Frame(self.f1,     bg = "white", width = 500, height = 500)
        self.f6 = Frame(self.f1,     bg = "white", width = 500, height = 500)
        self.f7 = Frame(self.f1,     bg = "white", width = 500, height = 500)
        self.f8 = Frame(self.f1,     bg = "white", width = 500, height = 500)
        self.f9 = Frame(self.master, bg = "white", width = 500, height = 500)

        
        self.no_range     = CustomRange(self.f3, self.system_size, self.filter_data)
        self.time_range_a = CustomRangeTime(self.f4, 0, self.filter_time, self.times, "A")
        self.average_a    = CustomAverage(self.f5, "Average A:", "Average A (Mult):")
        self.time_range_b = CustomRangeTime(self.f6, 0, self.filter_time, self.times, "B")
        self.average_b    = CustomAverage(self.f7, "Average B:", "Average B (Mult):")
        self.difference   = CustomAverage(self.f8, "Difference:", "Difference (Mult):")
        self.mult         = DoubleVar()
        self.avg_a        = StringVar()
        self.avg_a_mult   = StringVar()
        self.avg_b        = StringVar()
        self.avg_b_mult   = StringVar()
        self.diff         = StringVar()
        self.diff_mult    = StringVar()
        self.mult.set(5.267)
        self.avg_a.set(" 000.000")
        self.avg_a_mult.set(" 000.000")
        self.avg_b.set(" 000.000")
        self.avg_b_mult.set(" 000.000")
        self.diff.set(" 000.000")
        self.diff_mult.set(" 000.000")
        self.error_bar_text = StringVar()

        self.plot_area = plt.figure(figsize=(4, 3))
        self.canvas    = FigureCanvasTkAgg(self.plot_area, master = self.f9)
        self.plot_axis = self.plot_area.add_subplot(111)
        self.plot_area.tight_layout()

        Frame.__init__(self, self.master)
        self.render_gui()

        #REMOVE THIS:
        self.directories = ('/home/jpereira/Downloads/Mariana/26',)
        self.no_range.lp.set(17)
        self.load_data()


    def reset_data(self):
        self.data         = np.zeros(self.system_size) # Initial array of zeros
        self.times        = ["None"]
        self.results      = None


    def load_data(self):
        self.reset_data()
        found_one = False
        for directory in sorted(self.directories):
            for filename in sorted(os.listdir(directory)):
                if '-pic.txt' in filename:
                    self.parse_file(os.path.join(directory, filename))
                    self.times.append(filename[:5])
                    found_one = True
        if found_one == False:
            self.error_bar_text.set("Selected folder does not have any information.")
        else:
            self.error_bar_text.set("")
        self.data = np.delete(self.data, 0, 0) # Remove initial array of zeros
        self.times.pop(0)
        self.time_range_a.max_size = len(self.times) - 1
        self.time_range_b.max_size = len(self.times) - 1
        self.time_range_a.hp.set(int(round((len(self.times) - 1) / 2)))
        self.time_range_b.lp.set(int(round((len(self.times) - 1) / 2)) + 1)
        self.time_range_b.hp.set(len(self.times) - 1)
        self.filter_data()
        self.filter_time()


    def parse_file(self, filename):
        v      = np.zeros(self.system_size)
        c      = 0
        header = True
        with open(filename, "r") as file_in:
            for line in file_in:
                elem = line.split()
                if len(elem) == 14:
                    if header:
                        header = False
                    else:
                        v[c] = float(elem[9])
                        c += 1
        self.data = np.vstack((self.data, v))


    def select_folders(self):
        self.directories = askopendirnames(
            parent = root,
            title = 'Select folder(s)',
            initialdir = '/home/jpereira/Downloads/Mariana') # Change to current working directory
        self.load_data()
    
    
    def export_to(self):
        target_path = asksaveasfilename(
            parent = root,
            title = 'Select destination',
            defaultextension=".xlsx",
            filetypes=(("Excel", "*.xlsx"),("All Files", "*.*")),
            initialdir = '/home/jpereira/Downloads/Mariana') # Change to current working directory
        workbook = xlsxwriter.Workbook(target_path)
        worksheet = workbook.add_worksheet()
        worksheet.write(0, 0, "Time")
        worksheet.write(0, 1, "Value (ugr/l)")
        worksheet.write(0, 2, "Value Mult (ugr/l)")
        row = 1
        for (time, value, valuemult) in zip(self.times, self.results, [x * self.mult.get() for x in self.results]):
            worksheet.write(row, 0, time)
            worksheet.write(row, 1, value)
            worksheet.write(row, 2, valuemult)
            row += 1
        workbook.close()


    def update_plot(self):
        self.plot_axis.clear()
        self.plot_axis.plot(self.times, self.results)
        self.plot_axis.set_xticks(self.plot_axis.get_xticks()[::20])
        self.plot_axis.axvspan(self.time_range_a.lp.get(), self.time_range_a.hp.get(),
            alpha = 0.2, color = "#e9b44c")
        self.plot_axis.axvspan(self.time_range_b.lp.get(), self.time_range_b.hp.get(),
            alpha = 0.2, color = "#06d6a0")
        self.plot_axis.set_xlabel('Experience Time (h)', fontsize = 7)
        self.plot_axis.set_ylabel('Value (ugr/l)', fontsize = 7)
        self.canvas.draw()


    def calculate_avgs(self, event = None):
        avg_a = sum(self.results[self.time_range_a.lp.get():self.time_range_a.hp.get()]) / (self.time_range_a.hp.get() - self.time_range_a.lp.get())
        self.avg_a.set("%4.3f" % (avg_a))
        avg_b = sum(self.results[self.time_range_b.lp.get():self.time_range_b.hp.get()]) / (self.time_range_b.hp.get() - self.time_range_b.lp.get())
        self.avg_b.set("%4.3f" % (avg_b))
        diff = max(avg_b, avg_a) - min(avg_a, avg_b)
        self.diff.set("%4.3f" % (diff))

        self.avg_a_mult.set("%4.3f" % (avg_a * self.mult.get()))
        self.avg_b_mult.set("%4.3f" % (avg_b * self.mult.get()))
        self.diff_mult.set("%4.3f" % (diff * self.mult.get()))


    def filter_data(self):
        if len(self.data.shape) > 1:
            filtered_data = self.data[:, (self.no_range.lp.get() - 1):(self.no_range.hp.get() - 1)]
            self.results  = filtered_data.max(axis = 1)
        else:
            filtered_data = self.data[(self.no_range.lp.get() - 1):(self.no_range.hp.get() - 1)]
            self.results  = filtered_data.max()
        self.calculate_avgs()
        self.update_plot()


    def filter_time(self):
        self.time_range_a.lp_label.set(self.times[self.time_range_a.lp.get()])
        self.time_range_a.hp_label.set(self.times[self.time_range_a.hp.get()])
        self.time_range_b.lp_label.set(self.times[self.time_range_b.lp.get()])
        self.time_range_b.hp_label.set(self.times[self.time_range_b.hp.get()])

        self.calculate_avgs()
        self.update_plot()


    def render_gui(self):
        self.f1.pack(side = LEFT, expand = 1)                # Frame LEFT
        self.f2.pack(expand = 1, pady = (50, 10), padx = 50) # Select folder
        self.f3.pack(expand = 1, pady = (0, 25), padx = 50, fill = "x")       # Low/High Point
        self.f4.pack(expand = 1, pady = (10, 5), padx = 50, fill = "x")  # Time Range A
        self.f5.pack(expand = 1, pady = (0, 25), padx = 50, fill = "x")  # Average A
        self.f6.pack(expand = 1, pady = (10, 5), padx = 50, fill = "x")  # Time Range B
        self.f7.pack(expand = 1, pady = (0, 25), padx = 50, fill = "x")  # Average B
        self.f8.pack(expand = 1, pady = (10, 50), padx = 50, fill = "x") # Average total
        self.f9.pack(side = LEFT, expand = 1)                # Frame RIGHT

        sf = Button(self.f2, text="Select folder(s)",
            command=self.select_folders,
            highlightbackground = "white",
            activebackground = '#64b6ac',
            relief = "flat")
        sf.grid(row = 0, column = 0)
        mcl = Label(self.f2,
            text = "Multiplication constant:",
            bg = "white", 
            width = 25,
            anchor = "e")
        mcl.grid(row = 0, column = 1)
        self.mce = Entry(self.f2,
            textvariable        = self.mult,
            width               = 10,
            highlightbackground = "white")
        self.mce.grid(row = 0, column = 2)
        self.mce.bind("<FocusOut>", self.calculate_avgs)
        self.mce.bind("<Return>", self.calculate_avgs)
        tel = Label(self.f2,
            textvariable = self.error_bar_text,
            fg           = '#64b6ac',
            font         = ('Helvetica', 12),
            background   = "white")
        tel.grid(row = 1, column = 0, columnspan = 3)

        self.no_range.render()
        self.time_range_a.render()
        self.average_a.render(self.avg_a, self.avg_a_mult)
        self.time_range_b.render()
        self.average_b.render(self.avg_b, self.avg_b_mult)
        self.difference.render(self.diff, self.diff_mult)
        
        self.canvas.get_tk_widget().grid(row = 0, column = 0, padx = 10, pady = 10)
        self.canvas.draw()

        eb = Button(self.f9,
            text="Export",
            command=self.export_to,
            width = 35,
            highlightbackground = "white",
            activebackground = '#64b6ac',
            relief = "flat")
        eb.grid(row = 1, column = 0)
        bt = Label(self.f9,
            text = "José Pereira @ UA, 2019 (v1.0) : jose.manuel.pereira@ua.pt",
            anchor = "se",
            background = "white",
            fg = '#64b6ac')
        bt.grid(row = 2, column = 0, pady = (50, 0))


if __name__ == '__main__':
    root = Tk()
    root.title("Photocatalytic Degradation Companion Tool")
    root.style = Style()
    root.style.theme_use("alt")
    root.configure(background='white')
    app  = Application(master = root)
    app.mainloop()


# ~~~~~~~~~~~~~~~~~~~~ TODO ~~~~~~~~~~~~~~~~~~~~
# - Test with multiple folders
# - "Compile" in an executable folder