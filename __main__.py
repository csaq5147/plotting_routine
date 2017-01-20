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
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self, -1, self.figure)

        # Header of the Menu
        titleSizer = wx.BoxSizer(wx.HORIZONTAL)
        title = wx.StaticText(self, wx.ID_ANY, 'Menu Bar')
        titleSizer.Add(title, 0, wx.TOP | wx.BOTTOM, 20)

        # Creating the rows of button
        self.btn_row1 = wx.BoxSizer(wx.HORIZONTAL) 
        self.btn_row2 = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_row3 = wx.BoxSizer(wx.HORIZONTAL)

        # Button to create a function
        self.btn_plt = wx.Button(self, -1, "Plot a function")
        self.btn_row1.Add(self.btn_plt, -1, wx.EXPAND)
        self.Bind(wx.EVT_BUTTON, self.GetFunc, self.btn_plt)

        # Button for Intervall input
        self. btn_int = wx.Button(self, -1, "Intervall")
        self.btn_row1.Add(self.btn_int, -1, wx.EXPAND)
        self.Bind(wx.EVT_BUTTON, self.GetxInt, self.btn_int)

        # Button
        self.btn_xLabel = wx.Button(self, -1, "xLabel")
        self.btn_row2.Add(self.btn_xLabel, 1, wx.EXPAND)
        self.Bind(wx.EVT_BUTTON, self.GetxLabel, self.btn_xLabel)

        # Button
        self.btn_yLabel = wx.Button(self, -1, "yLabel")
        self.btn_row2.Add(self.btn_yLabel, 1, wx.EXPAND)
        self.Bind(wx.EVT_BUTTON, self.GetyLabel, self.btn_yLabel)

        # Button - Clear Plot
        self.btn_clear = wx.Button(self, -1, "Clear")
        self.btn_row3.Add(self.btn_clear, 1, wx.EXPAND)
        self.Bind(wx.EVT_BUTTON, self.on_button_clear, self.btn_clear)

        # Output field
        self.output= wx.TextCtrl(self, style=wx.TE_READONLY)
        self.output.SetValue(' ')

        # Radio Box
        self.radioList = ['blue', 'green', 'red', 'cyan', 'magenta',
                     'yellow', 'black']
        rb = wx.RadioBox(self, label="Colors", choices=self.radioList, majorDimension=2, style=wx.RA_SPECIFY_COLS)
        self.Bind(wx.EVT_RADIOBOX, self.ChangeColor, rb)

        # Menu 
        self.menu = wx.BoxSizer(wx.VERTICAL) 
        self.menu.Add(titleSizer, 0, wx.ALIGN_CENTER)
        self.menu.Add(wx.StaticLine(self), 0, wx.EXPAND, 0)   
        self.menu.Add(self.btn_plt, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 15)
        self.menu.Add(self.btn_int, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 15)
        self.menu.Add(wx.StaticLine(self), 0, wx.EXPAND, 0)   
        self.menu.Add(self.btn_row2, 0, wx.EXPAND | wx.ALL, 15)
        self.menu.Add(wx.StaticLine(self), 0, wx.EXPAND, 0) 
        self.menu.Add(rb, 0, wx.ALL, 15)
        self.menu.Add(wx.StaticLine(self), 0, wx.EXPAND, 0)   
        self.menu.Add(self.btn_row3, 0, wx.EXPAND | wx.ALL, 15)
        self.menu.Add(wx.StaticLine(self), 0, wx.EXPAND, 0)   
        self.menu.Add(self.output, 0, wx.EXPAND | wx.ALL, 15)

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
          self.myfunc = str(dlg.GetValue())
          self.variable = parse_expr(self.myfunc, transformations=transformations)
          self.Fx = sym.lambdify(x, self.variable)

          self.output.SetValue('f(x) = '+ self.myfunc)

          self.ax.cla()
          self.y = np.arange(0, 10, 0.01)
          self.ax.plot(self.y, np.array([self.Fx(i) for i in y]), 'b-')
          self.canvas.draw()

        except:
          self.output.SetValue('<- try again ->')

        dlg.Destroy()


    def GetxInt(self, event):
        dlg = wx.TextEntryDialog(None, 'x Intervall x1, x2',"Intervall","x1, x2", style=wx.OK)
        dlg.ShowModal()

        try:
          values = str(dlg.GetValue())
          self.xint = np.array(values.split(','), dtype='|S4')
          self.xint = self.xint.astype(np.float)
          
          self.output.SetValue('x in ['+str(self.xint[0])+','+str(self.xint[1])+']')

          self.ax.cla()
          y = np.arange(np.min(self.xint), np.max(self.xint), 0.01)
          self.ax.plot(y, np.array([self.Fx(i) for i in y]), 'k-')
          self.canvas.draw()
        except:
          self.output.SetValue('<- Error ->')

        dlg.Destroy()


    def GetxLabel(self, event):
        dlg = wx.TextEntryDialog(None, 'label of the x-axis',"Labels","xlabel", style=wx.OK)
        dlg.ShowModal()

        self.ax.set_xlabel( str(dlg.GetValue()) )
        self.canvas.draw()

        dlg.Destroy()

    def GetyLabel(self, event):
        dlg = wx.TextEntryDialog(None, 'label of the y-axis',"Labels","ylabel", style=wx.OK)
        dlg.ShowModal()

        self.ax.set_ylabel( str(dlg.GetValue()) )
        self.canvas.draw()

        dlg.Destroy()

    def ChangeColor(self, event):
        # try:
        #     self.ax.cla()
        #     try:
        #         y = np.arange(np.min(self.xint), np.max(self.xint), 0.01)
        #     except:
        #         y = np.arange(0, 10, 0.01)

        #     self.ax.plot(y, np.array([self.Fx(i) for i in y]), color=self.radioList[event.GetInt()] )

        #     self.canvas.draw()
        #     self.output.SetValue('<- Changed color ->')

        # except:
        #   self.output.SetValue('<- no function ->')

        # y = np.arange(np.min(self.xint), np.max(self.xint), 0.01)
        lines = self.ax.plot(self.y, np.array([self.Fx(i) for i in self.y]) )
        line = lines[0]
        line.set_color(self.radioList[event.GetInt()])

        self.canvas.draw()

        # self.ax.set_color(self.radioList[event.GetInt()])

    def on_button_clear(self, event):
        self.ax.cla()
        self.canvas.draw()
        self.Fx=0
        self.output.SetValue('clear')

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