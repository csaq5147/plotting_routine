import wx
import numpy as np
from matplotlib import collections, colors, transforms
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas, NavigationToolbar2WxAgg as NavigationToolbar
from matplotlib.figure import Figure
import sympy as sym
from sympy.abc import x
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

# let sympy read i.e. 2x as 2*x 
transformations = (standard_transformations + (implicit_multiplication_application,))


class CanvasFrame(wx.Frame):
    'Derive a new Class of Frame'
    def __init__(self):
        'runs when we create an instance of Canvas Frame'
        wx.Frame.__init__(self, None, -1,'Quick Plot')

        # Create a figure frame - here will be the plotted function 
        self.figure = Figure()
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self, -1, self.figure)

        # Header of the controll-menu
        titleSizer = wx.BoxSizer(wx.HORIZONTAL)
        title = wx.StaticText(self, wx.ID_ANY, 'Menu Bar')
        titleSizer.Add(title, 0, wx.TOP | wx.BOTTOM, 20)

        # Button to create a function
        self.btn_plt = wx.Button(self, -1, "Plot a function") # create a button
        self.Bind(wx.EVT_BUTTON, self.GetFunc, self.btn_plt) # create an action on the button

        # Button for Intervall input
        self. btn_int = wx.Button(self, -1, "Intervall")
        self.Bind(wx.EVT_BUTTON, self.GetxInt, self.btn_int)

        # Creating row of button to put to buttons next to each other
        self.btn_row = wx.BoxSizer(wx.HORIZONTAL)

        # Button - xlabel
        self.btn_xLabel = wx.Button(self, -1, "x-Label")
        self.btn_row.Add(self.btn_xLabel, -1, wx.EXPAND) # Add the button to the row
        self.Bind(wx.EVT_BUTTON, self.GetxLabel, self.btn_xLabel)

        # Button - ylable
        self.btn_yLabel = wx.Button(self, -1, "y-Label")
        self.btn_row.Add(self.btn_yLabel, -1, wx.EXPAND)
        self.Bind(wx.EVT_BUTTON, self.GetyLabel, self.btn_yLabel)

        # Button - Title
        self.btn_title = wx.Button(self, -1 , "Title")
        self.Bind(wx.EVT_BUTTON, self.GetTitle, self.btn_title)

        # Radio Box - choose from a list the color for the plot
        self.colorList = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black']
        self.rb = wx.RadioBox(self, label="Colors", choices=self.colorList, majorDimension=2, style=wx.RA_SPECIFY_COLS)
        self.Bind(wx.EVT_RADIOBOX, self.ChangeColor, self.rb)

        # Button - change linewidth
        self.btn_width = wx.Button(self, -1, "Linewidth")
        self.Bind(wx.EVT_BUTTON, self.ChangeWidth, self.btn_width)

        # button - output field (sth like a console)
        self.output= wx.TextCtrl(self, style=wx.TE_READONLY) 
        self.output.SetValue(' ')

        # Button - Clear figure 
        self.btn_clear = wx.Button(self, -1, "Clear")
        self.Bind(wx.EVT_BUTTON, self.on_button_clear, self.btn_clear)
       

        # Menu 
        self.menu = wx.BoxSizer(wx.VERTICAL) # the menu itself

        self.menu.Add(titleSizer, 0, wx.ALIGN_CENTER) # Adding Header of Menu

        self.menu.Add(wx.StaticLine(self), 0, wx.EXPAND, 0)  # Add a Static line for spacing

        self.menu.Add(self.btn_plt, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 15) # Add button to plot the function
        self.menu.Add(self.btn_int, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 15) # Add button for intervall

        self.menu.Add(wx.StaticLine(self), 0, wx.EXPAND, 0)  

        self.menu.Add(self.btn_row, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 15) # Add button for xlabel and ylabel
        self.menu.Add(self.btn_title, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 15) # Add button for title

        self.menu.Add(wx.StaticLine(self), 0, wx.EXPAND, 0) 

        self.menu.Add(self.rb, 0, wx.ALL, 15) # Add the radiobox for picking colors

        self.menu.Add(wx.StaticLine(self), 0, wx.EXPAND, 0) 

        self.menu.Add(self.btn_width, 0, wx.EXPAND | wx.ALL, 15) # A button for linewidth

        self.menu.Add(wx.StaticLine(self), 0, wx.EXPAND, 0) 

        self.menu.Add(self.btn_clear, 0, wx.EXPAND | wx.ALL, 15)  # Add clear button

        self.menu.Add(wx.StaticLine(self), 0, wx.EXPAND, 0)

        self.menu.Add(self.output, 0, wx.EXPAND | wx.ALL, 15) # Add console 

        # Add Toolbar to figure
        self.fframe = wx.BoxSizer(wx.VERTICAL)
        self.fframe.Add(self.canvas, 1, wx.EXPAND, 5)
        self.add_toolbar()

        # Main Frame - put menu and figure together
        self.main = wx.BoxSizer(wx.HORIZONTAL)
        self.main.Add(self.menu, 0, 0, 0)
        self.main.Add(self.fframe, 1, wx.EXPAND, 5)
        
        self.SetSizer(self.main)
        self.Fit()
         

    def GetFunc(self, event):
        'opens a dialog to insert a symbolic function'
        dlg = wx.TextEntryDialog(None, 'Please type in your function (argument is x)',"Which function do you wanna plot?","", style=wx.OK)
        dlg.ShowModal()

        try:
          myfunc = str(dlg.GetValue())
          variable = parse_expr(myfunc, transformations=transformations) # transforms the input value (string) to a sympy function
          self.Fx = sym.lambdify(x, variable) # transforms a the sympy to a readable function of 'x'

          self.output.SetValue('f(x) = '+ myfunc)
          self.ax.cla() 

          try: 
            self.xrange = np.arange(np.min(self.xint), np.max(self.xint), 0.01)
          except:
            self.xrange = np.arange(0, 10, 0.01) #default range of the plot

          self.myplot = self.ax.plot(self.xrange, np.array([self.Fx(i) for i in self.xrange]) )

          self.myplot
          self.canvas.draw()

        except:
          self.output.SetValue('<- try again ->')

        dlg.Destroy()


    def GetxInt(self, event):
        'opens a dialog to get range of the function'
        dlg = wx.TextEntryDialog(None, 'x Intervall x1, x2',"Intervall","x1, x2", style=wx.OK)
        dlg.ShowModal()

        try:
          values = str(dlg.GetValue())
          self.xint = np.array(values.split(','), dtype='|S4') 
          self.xint = self.xint.astype(np.float) #converts str to float
          
          self.ax.cla()

          self.xrange = np.arange(np.min(self.xint), np.max(self.xint), 0.01)
          self.myplot = self.ax.plot(self.xrange, np.array([self.Fx(i) for i in self.xrange]) )

          self.canvas.draw()

          self.output.SetValue('x in ['+str(self.xint[0])+','+str(self.xint[1])+']')

        except:
          self.output.SetValue('<- Error ->')

        dlg.Destroy()


    def GetxLabel(self, event):
        'opens a dialog to insert xlabel'
        dlg = wx.TextEntryDialog(None, 'insert x-label',"label of x-axis","xlabel", style=wx.OK)
        dlg.ShowModal()

        self.ax.set_xlabel( str(dlg.GetValue()) )
        self.canvas.draw()

        dlg.Destroy()

    def GetyLabel(self, event):
        'opens a dialog to insert ylabel'
        dlg = wx.TextEntryDialog(None, 'insert y-label',"label of y-axis","ylabel", style=wx.OK)
        dlg.ShowModal()

        self.ax.set_ylabel( str(dlg.GetValue()) )
        self.canvas.draw()

        dlg.Destroy()

    def GetTitle(self, event):
        'opens a dialog to insert title'
        dlg = wx.TextEntryDialog(None, 'Insert title',"title of plot","title", style=wx.OK)
        dlg.ShowModal()

        self.ax.set_title( str(dlg.GetValue()) )
        self.canvas.draw()

        dlg.Destroy()

    def ChangeColor(self, event):
        'event to select the color for the plot'
        try:
            self.line = self.myplot[0]
            self.line.set_color( self.colorList[event.GetInt()] )
            self.canvas.draw()

            self.output.SetValue('<- Changed color ->')

        except:
          self.output.SetValue('<- no function ->')

    def ChangeWidth(self, event):
        'opens a dialog to customize linewidth of the plotted function'
        dlg = wx.TextEntryDialog(None, 'Insert linewidth',"Linewidth","1.0", style=wx.OK)
        dlg.ShowModal()

        try:
            self.line = self.myplot[0]
            self.line.set_linewidth( float(dlg.GetValue()) )
            self.canvas.draw()

            self.output.SetValue('<- Changed width ->')

        except:
          self.output.SetValue('<- error with width ->')

    def on_button_clear(self, event):
        'clears the figure'
        self.ax.cla()
        self.canvas.draw()
        self.rb.SetSelection(0)
        self.output.SetValue('clear')


    def add_toolbar(self):
        'Add a toolbar under the figure'
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