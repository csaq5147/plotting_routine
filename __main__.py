import wx
import numpy as np
from matplotlib import collections, colors, transforms
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas, NavigationToolbar2WxAgg as NavigationToolbar
from matplotlib.figure import Figure
import sympy as sym
from sympy.abc import x
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
transformations = (standard_transformations + (implicit_multiplication_application,))


class CanvasFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1,'Quick Plot')

        # Figure Frame - here will be the plotted function
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.axes.plot()
        self.canvas = FigureCanvas(self, -1, self.figure)

        # Header of the Menu
        titleSizer = wx.BoxSizer(wx.HORIZONTAL)
        title = wx.StaticText(self, wx.ID_ANY, 'Menu Bar')
        titleSizer.Add(title, 0, wx.TOP | wx.BOTTOM, 20)

        # Creating the rows of button
        self.btn = [] 
        self.btn_row1 = wx.BoxSizer(wx.HORIZONTAL) 
        self.btn_row2 = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_row3 = wx.BoxSizer(wx.HORIZONTAL)

        # Button for Intervall input
        self.btn.append(wx.Button(self, -1, "Intervall"))
        self.btn_row1.Add(self.btn[0], 1, wx.EXPAND)
        self.Bind(wx.EVT_BUTTON, self.GetxInt, self.btn[0])

        # Button - change color 
        self.btn.append(wx.Button(self, -1, "Red"))
        self.btn_row2.Add(self.btn[1], 1, wx.EXPAND)
        self.Bind(wx.EVT_BUTTON, self.ChangeColor, self.btn[1])

        # Button -
        self.btn.append(wx.Button(self, -1, "Thick"))
        self.btn_row2.Add(self.btn[2], 1, wx.EXPAND)
        self.Bind(wx.EVT_BUTTON, self.GetyInt, self.btn[2])

        # Button - Clear Plot
        self.btn.append(wx.Button(self, -1, "Clear"))
        self.btn_row3.Add(self.btn[3], 1, wx.EXPAND)
        self.Bind(wx.EVT_BUTTON, self.on_button_clear, self.btn[3])

        # Button to create a function
        self.btn_plt = wx.Button(self, -1, "Plot a function")
        self.Bind(wx.EVT_BUTTON, self.GetFunc, self.btn_plt)

        # Output field
        self.output= wx.TextCtrl(self, style=wx.TE_READONLY)
        self.output.SetValue(' ')

        # Empty Row
        empty_r = wx.BoxSizer(wx.HORIZONTAL)
        empty_r.Add(wx.StaticText(self, wx.ID_ANY, ' '), 0, wx.CENTER, 5)

        # Menu 
        self.menu = wx.BoxSizer(wx.VERTICAL) 
        self.menu.Add(titleSizer, 0, wx.ALIGN_CENTER)
        self.menu.Add(wx.StaticLine(self), 0, wx.EXPAND, 0)   
        self.menu.Add(self.btn_plt, 0, wx.EXPAND | wx.ALL, 15)
        self.menu.Add(wx.StaticLine(self), 0, wx.EXPAND, 0)   
        self.menu.Add(self.btn_row1, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 15)
        self.menu.Add(self.btn_row2, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 15)
        self.menu.Add(self.btn_row3, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 15)
        self.menu.Add(wx.StaticLine(self), 0, wx.EXPAND, 0)   
        self.menu.Add(self.output, 0, wx.EXPAND | wx.ALL, 15)
        self.menu.Add(empty_r, 0, 0, 0)

        # Adding Toolbar to Plot
        self.fframe = wx.BoxSizer(wx.VERTICAL)
        self.fframe.Add(self.canvas, 1, wx.EXPAND, 5)
        self.add_toolbar()

        # Main Frame
        self.main = wx.BoxSizer(wx.HORIZONTAL)
        self.main.Add(self.menu, 0, 0, 0)
        self.main.Add(self.fframe, 1, wx.EXPAND, 5)
        
        self.SetSizer(self.main)
        self.Fit()
         

    def GetFunc(self, event):
        dlg = wx.TextEntryDialog(None, 'Please type in your function (argument is x)',"Which function do you wanna plot?","", style=wx.OK)
        dlg.ShowModal()

        try:
          myfunc = str(dlg.GetValue())
          self.variable = parse_expr(myfunc, transformations=transformations)
          self.Fx = sym.lambdify(x, self.variable)
          ax = self.figure.add_subplot(111)

          self.output.SetValue('f(x) = '+ myfunc)

          ax.cla()
          y = np.arange(0, 10, 0.01)
          ax.plot(y, np.array([self.Fx(i) for i in y]), 'k-')
          self.canvas.draw()
        except:
          self.output.SetValue('<--- NEW ENTRY --->')

        dlg.Destroy()


    def GetxInt(self, event):
        dlg = wx.TextEntryDialog(None, 'x Intervall x1, x2',"Intervall","x1, x2", style=wx.OK)
        dlg.ShowModal()

        try:
          values = str(dlg.GetValue())
          self.xint = np.array(values.split(','), dtype='|S4')
          self.xint = self.xint.astype(np.float)
          
          self.output.SetValue('x in ['+str(self.xint[0])+','+str(self.xint[1])+']')

          ax = self.figure.add_subplot(111)
          ax.cla()
          y = np.arange(np.min(self.xint), np.max(self.xint), 0.01)
          ax.plot(y, np.array([self.Fx(i) for i in y]), 'k-')
          self.canvas.draw()
        except:
          self.output.SetValue('<--- Error --->')

        dlg.Destroy()


    def GetyInt(self, event): # doesn't work
        dlg = wx.TextEntryDialog(None, 'y Intervall y1, y2',"Intervall","y1, y2", style=wx.OK)
        dlg.ShowModal()

        try:
          values = str(dlg.GetValue())
          self.yint = np.array(values.split(','), dtype='|S4')
          self.yint = self.yint.astype(np.float)
          
          self.output.SetValue('y in ['+str(self.yint[0])+','+str(self.myint[1])+']')

          ax = self.figure.add_subplot(111)
          ax.cla()
          # ax.axes.set_ylim(np.min(self.yint), np.max(self.yint))
          y = np.arange(np.min(self.xint), np.max(self.xint), 0.01)
          ax.plot(y, np.array([self.Fx(i) for i in y]), 'k-')
          self.canvas.draw()
        except:
          self.output.SetValue('<--- Error --->')

        dlg.Destroy()



    def ChangeColor(self, event):
        try:
            ax = self.figure.add_subplot(111)
            ax.cla()
            try:
                y = np.arange(np.min(self.myint), np.max(self.myint), 0.01)
            except:
                y = np.arange(0, 10, 0.01)

            ax.plot(y, np.array([self.Fx(i) for i in y]), 'r')
            self.canvas.draw()

        except:
          self.output.SetValue('<--- Try Again --->')

    def on_button_clear(self, event):
        ax = self.figure.add_subplot(111)
        ax.cla()
        self.canvas.draw()
        self.Fx=0

    def add_toolbar(self):
        self.toolbar = NavigationToolbar(self.canvas)
        self.toolbar.Realize()
        self.fframe.Add(self.toolbar, 0, wx.EXPAND | wx.ALIGN_CENTER)
        self.toolbar.update()

class App(wx.App):
    def OnInit(self):
        'Create the main window and insert the custom frame'
        frame = CanvasFrame()
        frame.Show(True)
        return True

app = App(0)
app.MainLoop()