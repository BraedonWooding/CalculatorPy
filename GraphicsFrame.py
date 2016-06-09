import wx.lib.plot as plot
import wx.adv
import wx
import UIConstants
import subprocess

selfV = None
#Not sure if used but it could be somewhere.  Shouldn't be used though since doesn't update
#Probably left over from archaic
latestGraphSelf = None
allGraphs = []

colours = [
"FIREBRICK","MEDIUM FOREST GREEN","RED",
"BLACK","FOREST GREEN","MEDIUM GOLDENROD","SALMON",
"BLUE","GOLD","MEDIUM ORCHID", "SEA GREEN",
"BLUE VIOLET","GOLDENROD", "MEDIUM SEA GREEN", "SIENNA",
"BROWN", "GREY", "MEDIUM SLATE BLUE", "SKY BLUE",
"CADET BLUE", "GREEN", "MEDIUM SPRING GREEN", "SLATE BLUE",
"CORAL","GREEN YELLOW",	"MEDIUM TURQUOISE", "SPRING GREEN",
"CORNFLOWER BLUE",	"INDIAN RED", "MEDIUM VIOLET RED", "STEEL BLUE",
"CYAN", "KHAKI", "MIDNIGHT BLUE", "TAN",
"DARK GREY",	"LIGHT BLUE",	"NAVY",	"THISTLE",
"DARK GREEN",	"LIGHT GREY",	"ORANGE",	"TURQUOISE",
"DARK OLIVE GREEN",	"LIGHT STEEL BLUE",	"ORANGE RED", "VIOLET",
"DARK ORCHID",	"LIME GREEN", 	"ORCHID",	"VIOLET RED",
"DARK SLATE BLUE",	"MAGENTA",	"PALE GREEN",	"WHEAT",
"DARK SLATE GREY",	"MAROON",	"PINK",	"WHITE",
"DARK TURQUOISE",	"MEDIUM AQUAMARINE",	"PLUM",	"YELLOW",
"DIM GREY",	"MEDIUM BLUE",	"PURPLE",	"YELLOW GREEN"
]

#A choice dialog for choosing a colour
def chooseColour() -> str:
    colourPicker = wx.SingleChoiceDialog(None, "Choose Colour", "", colours,
                                         wx.CHOICEDLG_STYLE | wx.OK | wx.CANCEL | wx.CENTRE)
    try:
        if colourPicker.ShowModal() == wx.ID_OK and 0 < colourPicker.GetSelection() < len(colours):
            return colours[colourPicker.GetSelection()]
    finally:
        colourPicker.Destroy()

#A choice dialog for all the hidden lines (returns an index)
def chooseHidden(graph) -> int:
    if graph is not None:
        if len(graph[0].hiddenLines) > 1:
            strings = graph[0].hiddenLegends
            #Removes left most space
            strings = [x.lstrip(' ') for x in strings]
            if len(strings) >= 1:
                dlg = wx.SingleChoiceDialog(None, "Choose Line", "Choose one of the line/s", strings, wx.CHOICEDLG_STYLE | wx.OK | wx.CANCEL | wx.CENTRE)
                try:
                    if dlg.ShowModal() == wx.ID_OK:
                        if dlg.GetSelection() is not None and dlg.GetSelection() >= 0:
                            return dlg.GetSelection()
                finally:
                    dlg.Destroy()
        elif len(graph[0].hiddenLines) == 1:
            return 0
        else:
            return None
    else:
        return None

#A choice dialog that returns a line index
def chooseLine(graph) -> int:
    if graph is not None:
        if len(graph[0].data) > 1:
            strings = graph[0].legends
            #Removes left most space
            strings = [x.lstrip(' ') for x in strings]
            if len(strings) >= 1:
                dlg = wx.SingleChoiceDialog(None, "Choose Line", "Choose one of the line/s", strings, wx.CHOICEDLG_STYLE | wx.OK | wx.CANCEL | wx.CENTRE)
                try:
                    if dlg.ShowModal() == wx.ID_OK:
                        if dlg.GetSelection() is not None and dlg.GetSelection() >= 0:
                            return dlg.GetSelection()
                finally:
                    dlg.Destroy()
        elif len(graph[0].data) == 1:
            return 0
        else:
            return None
    else:
        return None

#A choice dialog that returns a graph index
def chooseGraph() -> int:
    # Select a graph
    for x in allGraphs:
        if x[0].canvas is None:
            allGraphs.remove(x)

    if allGraphs is not None and len(allGraphs) > 0:
        if len(allGraphs) == 1:
            return 0
        dlg = wx.SingleChoiceDialog(None, "Choose Graph", "Choose one of the graph/s", tuple(x[1] for x in allGraphs),
                                    wx.CHOICEDLG_STYLE | wx.OK | wx.CANCEL | wx.CENTRE)
        try:
            if dlg.ShowModal() == wx.ID_OK:
                if dlg.GetSelection() is not None and dlg.GetSelection() >= 0:
                    return dlg.GetSelection()
        finally:
            dlg.Destroy()
    return 0

#Setups the graphics frame (or the graph)
class GraphicsFrame(wx.Frame):
    def __init__(self, parent, data, x, y, expression, start_colour='FIREBRICK', xaxis='X axis', yaxis='Y axis', width=1.5, start_colours=None, legends=None):
        wx.Frame.__init__(self, parent, -1, "Graph " + str(len(allGraphs)), size=(940, 720))
        #Data is in format of [ [ [(24,1)], [(1,6)] ], [ [(2,9)] ] ]
        self.data = data
        self.xaxis = xaxis
        self.yaxis = yaxis
        self.title = expression
        self.canvas = None
        self.lines = []
        self.frame_size = None
        self.name = ""
        self.hiddenLines = []
        self.hiddenLegends = []
        self.colour = []
        #Base Colours
        self.bgColour = 'WHITE'
        self.fgColour = 'BLACK'
        self.legends = legends
        self.x = x
        self.y = y
        self.width = width
        index = colours.index(start_colour.upper())
        if start_colours is not None:
            for colour in start_colours:
                index = colours.index(colour.upper())
                self.colour.append(colours[index])
        for _ in range(len(data)):
            if index >= len(colours):
                index = 0
            self.colour.append(colours[index])
            index += 1
        allGraphs.append((self, expression))
        self.graph = (self, expression)
        self.Center()
        self.Bind(wx.EVT_CLOSE, self.onExit)
        #Draws graph
        self.draw()

    #Draws the graph
    def draw(self):
        # plot.
        global latestGraphSelf
        self.canvas = plot.PlotCanvas(self, pos=(0,0), size=(940,720))
        self.canvas.EnableZoom = True
        self.canvas.SetBackgroundColour(self.bgColour)
        self.canvas.FontSizeLegend = 10
        self.canvas.SetForegroundColour(self.fgColour)
        self.lines = []
        self.title = self.name if self.name is not "" else "& ".join([x.lstrip(' ') for x in self.legends])
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                line = plot.PolyLine(self.data[i][j], colour=self.colour[i].lower(), width=self.width, legend=(self.legends[i] if j == 0 and len(self.legends) > i else "^"))
                self.lines.append(line)
        # get client usable size of frame
        # needed for SaveFile() later
        self.frame_size = self.GetClientSize()
        self.canvas.SetInitialSize(size=self.frame_size)
        gc = plot.PlotGraphics(self.lines, self.title, self.xaxis, self.yaxis)
        self.canvas.Draw(gc, xAxis=self.x, yAxis=self.y)
        self.canvas.EnableZoom = False
        self.canvas.EnableAntiAliasing = True
        self.canvas.EnableHiRes = UIConstants.gHiRes
        if len(self.data) > 0:
            self.canvas.EnableLegend = UIConstants.gLegend
        self.canvas.EnableGrid = UIConstants.gGrid
        latestGraphSelf = self

    #On exit of graph, remove the graph
    def onExit(self, event):
        allGraphs.remove(self.graph)
        self.Destroy()
        event.Skip()

outlineGraph = True
#Setups calculator menu from panel
class CalculatorMenu:
    def __init__(self, panel):
        self.menu_bar = wx.MenuBar()

        # Options menu
        self.edit_menu = wx.Menu()
        self.edit_menu.Append(wx.ID_EDIT, "&Command Line\tCtrl+L")
        self.edit_menu.Append(wx.ID_FILE2, "&Degrees\tCtrl+D", "Degrees/Radians")
        self.edit_menu.Append(wx.ID_FILE9, "&Decimals\tCtrl+F", "Decimals/Fractions")
        self.edit_menu.Append(wx.ID_FILE3, "&Recursion Stopper\tCtrl+R", "Enable recursion blocker", wx.ITEM_CHECK)
        self.edit_menu.Append(wx.ID_FILE4, "&Time Logger\tCtrl+T", "Enable time logger", wx.ITEM_CHECK)
        self.menu_bar.Append(self.edit_menu, "&Options")

        #Graphing Options menu
        self.graphing_menu = wx.Menu()
        self.graphing_menu.Append(wx.ID_FILE6, "&Grid Outline\tCtrl+I", "Enable grid", wx.ITEM_CHECK)
        self.graphing_menu.Append(wx.ID_FILE7, "&Hi-Res\tCtrl+H", "Enable Hi-Res Mode", wx.ITEM_CHECK)
        self.graphing_menu.Append(wx.ID_FILE8, "&Legend\tCtrl+J", "Enable Legend", wx.ITEM_CHECK)
        self.menu_bar.Append(self.graphing_menu, "&Graphing")

        #Options menu checks
        self.edit_menu.Check(wx.ID_FILE3, UIConstants.gRecursionStopper)
        self.edit_menu.Check(wx.ID_FILE4, UIConstants.gTime)

        #Graphing menu checks
        self.graphing_menu.Check(wx.ID_FILE6, True)
        self.graphing_menu.Check(wx.ID_FILE7, False)
        self.graphing_menu.Check(wx.ID_FILE8, True)

        #Save Menu
        self.save_menu = wx.Menu()
        self.save_menu.Append(wx.ID_SAVE, "&Save Graph\tCtrl+S")
        self.save_menu.Append(wx.ID_PRINT, "&Print Graph\tCtrl+P")
        self.menu_bar.Append(self.save_menu, "&Save")

        #Help Menu
        self.help_menu = wx.Menu()
        self.help_menu.Append(wx.ID_ABOUT, "&About Complex Calculator")
        self.help_menu.Append(wx.ID_FILE, "&About Calculator Mode")
        self.help_menu.Append(wx.ID_FILE1, "&About Graph Mode")
        self.help_menu.Append(wx.ID_HELP, "&Help File")
        self.menu_bar.Append(self.help_menu, "&Help")

        #Binds the panels and their actions
        panel.SetMenuBar(self.menu_bar)
        panel.Bind(wx.EVT_MENU, self.onAboutMain, id=wx.ID_ABOUT)
        panel.Bind(wx.EVT_MENU, self.onAboutCalc, id=wx.ID_FILE)
        panel.Bind(wx.EVT_MENU, self.onAboutGraph, id=wx.ID_FILE1)
        panel.Bind(wx.EVT_MENU, self.printGraph, id=wx.ID_PRINT)
        panel.Bind(wx.EVT_MENU, self.saveGraph, id=wx.ID_SAVE)
        panel.Bind(wx.EVT_MENU, self.commandLine, id=wx.ID_EDIT)
        panel.Bind(wx.EVT_MENU, self.toggleDegrees, id=wx.ID_FILE2)
        panel.Bind(wx.EVT_MENU, self.toggleRecursion, id=wx.ID_FILE3)
        panel.Bind(wx.EVT_MENU, self.toggleTime, id=wx.ID_FILE4)
        panel.Bind(wx.EVT_MENU, self.toggleGrid, id=wx.ID_FILE6)
        panel.Bind(wx.EVT_MENU, self.toggleHiRes, id=wx.ID_FILE7)
        panel.Bind(wx.EVT_MENU, self.toggleLegend, id=wx.ID_FILE8)
        panel.Bind(wx.EVT_MENU, self.toggleFractions, id=wx.ID_FILE9)

        panel.Bind(wx.EVT_MENU, self.openHelp, id=wx.ID_HELP)

    @classmethod
    def openHelp(cls, event):
        subprocess.Popen("open Help.pdf", shell=True)

    #Toggles degrees and radians; is reversed since I called variable gRadians instead of gDegrees
    def toggleDegrees(self, event):
        UIConstants.gRadians = not UIConstants.gRadians
        self.edit_menu.SetLabel(wx.ID_FILE2, "Radians\tCtrl+D" if UIConstants.gRadians else "Degrees\tCtrl+D")

    # Toggles recursion
    def toggleRecursion(self, event):
        UIConstants.gRecursionStopper = self.edit_menu.IsChecked(wx.ID_FILE3)
        self.edit_menu.Check(wx.ID_FILE3, self.edit_menu.IsChecked(wx.ID_FILE3))

    # Toggles time logging
    def toggleTime(self, event):
        UIConstants.gTime = self.edit_menu.IsChecked(wx.ID_FILE4)
        self.edit_menu.Check(wx.ID_FILE4, self.edit_menu.IsChecked(wx.ID_FILE4))

    #Toggles grid
    def toggleGrid(self, event):
        global outlineGraph
        UIConstants.gGrid = self.graphing_menu.IsChecked(wx.ID_FILE6)
        outlineGraph = UIConstants.gGrid
        self.graphing_menu.Check(wx.ID_FILE6, self.graphing_menu.IsChecked(wx.ID_FILE6))
        for graph in allGraphs:
            graph[0].draw()

    #Toggles high resolution
    def toggleHiRes(self, event):
        UIConstants.gHiRes = self.graphing_menu.IsChecked(wx.ID_FILE7)
        self.graphing_menu.Check(wx.ID_FILE7, self.graphing_menu.IsChecked(wx.ID_FILE7))
        if UIConstants.gHiRes:
            UIConstants.gGrid = False
            self.graphing_menu.Check(wx.ID_FILE6, False)
        else:
            UIConstants.gGrid = outlineGraph
            self.graphing_menu.Check(wx.ID_FILE6, outlineGraph)
        for graph in allGraphs:
            graph[0].draw()

    #Toggles legends for graphs
    def toggleLegend(self, event):
        UIConstants.gLegend = self.graphing_menu.IsChecked(wx.ID_FILE8)
        self.graphing_menu.Check(wx.ID_FILE8, self.graphing_menu.IsChecked(wx.ID_FILE8))
        for graph in allGraphs:
            graph[0].draw()

    # Toggles recursion
    def toggleFractions(self, event):
        UIConstants.gFraction = not UIConstants.gFraction
        self.edit_menu.SetLabel(wx.ID_FILE9, "Fraction\tCtrl+F" if UIConstants.gFraction else "Decimal\tCtrl+F")
        if "y" not in _latest.lower() and "x" not in _latest.lower() and _latest is not "" and _latest is not " ":
            _main(_latest)

    #An about information of main mode
    @classmethod
    def onAboutMain(cls, event):
        aboutInfo = wx.adv.AboutDialogInfo()
        aboutInfo.SetName("Graphics Calculator")
        aboutInfo.SetVersion("1.01a")
        aboutInfo.SetDescription("A graphics calculator")
        aboutInfo.SetCopyright("(C) 2016-")
        aboutInfo.AddDeveloper("Braedon Wooding")
        wx.adv.AboutBox(aboutInfo)

    #An about information of calculator mode
    @classmethod
    def onAboutCalc(cls, event):
        dlg = wx.MessageDialog(None, "Calculator Mode\n"
                                     "This mode allows you to perform complex sets of equations, chaining multiple together.\n"
                                     "All commands and further explanation is in the documentation\n",
                               "About Calculator Mode", wx.OK | wx.ICON_INFORMATION)

        dlg.ShowModal()

    #An about information of graph mode
    @classmethod
    def onAboutGraph(cls, event):
        dlg = wx.MessageDialog(None, "Graph Mode\n"
                                     "This mode allows you to graph any set of x and y values as long as its in the format of x|y = [x|y].*.\n"
                                     "This is explained further in the documentation\n",
                               "About Graphing Mode", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()

    #Prints the graph
    @classmethod
    def printGraph(cls, event):
        chosenGraph = chooseGraph()
        if chosenGraph < len(allGraphs):
            allGraphs[chosenGraph][0].canvas.PrintPreview()

    #Saves the graph
    @classmethod
    def saveGraph(cls, event):
        chosenGraph = chooseGraph()
        if chosenGraph < len(allGraphs):
            if not cls.saveGraphDialog(graphInt=chosenGraph, fileName=allGraphs[chosenGraph][1]):
                dlg = wx.MessageDialog(None, "Saving failed", 'File Saving Error',
                                        wx.OK | wx.ICON_ERROR)
                try:
                    dlg.ShowModal()
                finally:
                    dlg.Destroy()

    #For some reason the wxpython save dialog wasn't working so I just decided to copy and paste the function into here and fix it.
    #So some documentation may be a bit off but should be mostly good.
    @classmethod
    def saveGraphDialog(cls, fileName = '', graphInt = 0):
        #The plotcanvas savefile is broken currently and since I can't end the code this is just a copy and paste with the fixes
        """
        Saves the file to the type specified in the extension. If no file
        name is specified a dialog box is provided.  Returns True if sucessful,
        otherwise False.
        .bmp  Save a Windows bitmap file.
        .png  Save a Portable Network Graphics file.
        .jpg  Save a Joint Photographic Experts Group file.
        """
        extensions = {
            "bmp": wx.BITMAP_TYPE_BMP,  # Save a Windows bitmap file.
            "jpg": wx.BITMAP_TYPE_JPEG,  # Save a JPG file.
            "png": wx.BITMAP_TYPE_PNG,  # Save a PNG file.
        }

        fType = fileName[-3:].lower()
        dlg1 = None
        while fType not in extensions:

            msg_txt = ('File name extension\n'  # implicit str concat
                       'must be one of\nbmp, png, or jpg')

            if dlg1:  # FileDialog exists: Check for extension
                dlg2 = wx.MessageDialog(None, msg_txt, 'File Name Error',
                                        wx.OK | wx.ICON_ERROR)
                try:
                    dlg2.ShowModal()
                finally:
                    dlg2.Destroy()
            # FileDialog doesn't exist: just check one
            else:
                msg_txt = ("Choose a file with extension bmp, "
                           "gif, tif, gif, png, or jpg")
                wildcard_str = ("BMP files (*.bmp)|*.bmp|"
                                "PNG files (*.png)|*.png|"
                                "JPG files (*.jpg)|*.jpg")
                dlg1 = wx.FileDialog(allGraphs[graphInt][0],
                                     msg_txt,
                                     ".",
                                     "",
                                     wildcard_str,
                                     wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
                                     )

            if dlg1.ShowModal() == wx.ID_OK:
                fileName = dlg1.GetPath()
                fType = fileName[-3:].lower()
            else:  # exit without saving
                dlg1.Destroy()
                return True
        if dlg1:
            dlg1.Destroy()

        # Save Bitmap
        res = allGraphs[graphInt][0].canvas._Buffer.SaveFile(fileName, extensions[fType])
        return res

    @classmethod
    #Command Line that changes the graph based of input
    def commandLine(cls, event):
        #Select a graph
        chosenGraph = chooseGraph()
        if chosenGraph < len(allGraphs):
            graphOfChoice = allGraphs[chosenGraph]
        else:
            graphOfChoice = None
        #Type command
        textEntryDialog = wx.TextEntryDialog(None, "Type your command in.\nCommands in documentation", "Command Line")
        if textEntryDialog.ShowModal() == wx.ID_OK:
            value = textEntryDialog.GetValue()
            #Closes the graph
            if "close" in value.lower() and graphOfChoice is not None:
                graphOfChoice[0].Close()
            #Changes the colour of the graph
            if "colour" in value.lower() and graphOfChoice is not None:
                line = chooseLine(graphOfChoice)
                colour = chooseColour()
                if colour is not None and line is not None:
                    graphOfChoice[0].colour[line] = colour
                    graphOfChoice[0].draw()
            #Clears the graph
            if "clear" in value.lower() and graphOfChoice is not None:
                graphOfChoice[0].canvas.Clear()
            #Redraws the graph
            if "redraw" in value.lower() or "reset" in value.lower() and graphOfChoice is not None:
                graphOfChoice[0].canvas.Clear()
                graphOfChoice[0].draw()
            #Changes the min and max size x of graph
            if "sizex" in value.lower() and graphOfChoice is not None:
                textEntryDialogXS = wx.TextEntryDialog(None, "Type x small size", "From...")
                textEntryDialogXL = wx.TextEntryDialog(None, "Type x large size", "From...")
                if textEntryDialogXS.ShowModal() == wx.ID_OK and textEntryDialogXL.ShowModal() == wx.ID_OK:
                    try:
                        graphOfChoice[0].x = (float(textEntryDialogXS.GetValue()), float(textEntryDialogXL.GetValue()))
                    except (ArithmeticError, ValueError, TypeError, NameError, AssertionError):
                        msgDialog = wx.MessageDialog(None, "Size X Error", "You entered values wrong")
                        msgDialog.ShowModal()
                    finally:
                        graphOfChoice[0].draw()

            #Changes the min and max size y of graph
            if "sizey" in value.lower() and graphOfChoice is not None:
                textEntryDialogYS = wx.TextEntryDialog(None, "Type y small size", "From...")
                textEntryDialogYL = wx.TextEntryDialog(None, "Type y large size", "From...")
                if textEntryDialogYS.ShowModal() == wx.ID_OK and textEntryDialogYL.ShowModal() == wx.ID_OK:
                    try:
                        graphOfChoice[0].y = (float(textEntryDialogYS.GetValue()), float(textEntryDialogYL.GetValue()))
                    except (ArithmeticError, ValueError, TypeError, NameError, AssertionError):
                        msgDialog = wx.MessageDialog(None, "Size Y Error", "You entered values wrong")
                        msgDialog.ShowModal()
                    finally:
                        graphOfChoice[0].draw()

            #Changes the title of the graph
            if "name" in value.lower() and graphOfChoice is not None:
                textEntryDialogN = wx.TextEntryDialog(None, "Type new graph name", "For title of graph")
                if textEntryDialogN.ShowModal() == wx.ID_OK:
                    graphOfChoice[0].name = textEntryDialogN.GetValue()
                    graphOfChoice[0].draw()

            #Changes the width of line
            if "width" in value.lower() and graphOfChoice is not None:
                textEntryDialogWidth = wx.TextEntryDialog(None, "Type new width", "Line Width")
                textEntryDialogWidth.SetValue(str(graphOfChoice[0].width))
                if textEntryDialogWidth.ShowModal() == wx.ID_OK:
                    try:
                        graphOfChoice[0].width = float(textEntryDialogWidth.GetValue())
                        graphOfChoice[0].draw()
                    except (ValueError, NameError, TypeError):
                        pass

            # Changes the label x-axis text
            if "labelx" in value.lower() and graphOfChoice is not None:
                textEntryDialogXAxis = wx.TextEntryDialog(None, "Type horizontal axis name",
                                                          "Normally \'X Axis\'")
                if textEntryDialogXAxis.ShowModal() == wx.ID_OK:
                    graphOfChoice[0].xAxis = textEntryDialogXAxis.GetValue()
                    graphOfChoice[0].draw()

            #Changes the label y-axis text
            if "labely" in value.lower() and graphOfChoice is not None:
                textEntryDialogYAxis = wx.TextEntryDialog(None, "Type vertical axis name", "Normally \'Y Axis\'")
                if textEntryDialogYAxis.ShowModal() == wx.ID_OK:
                    graphOfChoice[0].yAxis = textEntryDialogYAxis.GetValue()
                    graphOfChoice[0].draw()

            #Sets background of graph
            if "background" in value.lower():
                colourChosen = chooseColour()
                if colourChosen is not None and graphOfChoice is not None:
                    graphOfChoice[0].bgColour = colourChosen
                    graphOfChoice[0].draw()

            #Sets the text colour or 'foreground'
            if "foreground" in value.lower():
                colourChosen = chooseColour()
                if colourChosen is not None and graphOfChoice is not None:
                    graphOfChoice[0].fgColour = colourChosen
                    graphOfChoice[0].draw()

            #Unhides all linse
            if "unhide all" in value.lower():
                if graphOfChoice[0] is not None:
                    graphOfChoice[0].data.extend(graphOfChoice[0].hiddenLines)
                    graphOfChoice[0].hiddenLines = []
                    graphOfChoice[0].legends.extend(graphOfChoice[0].hiddenLegends)
                    graphOfChoice[0].hiddenLegends = []
                    graphOfChoice[0].draw()

            #Unhides x line
            elif "unhide" in value.lower():
                if graphOfChoice is not None:
                    line = chooseHidden(graphOfChoice)
                    if line is not None:
                        graphOfChoice[0].data.append(graphOfChoice[0].hiddenLines[line])
                        graphOfChoice[0].hiddenLines.remove(graphOfChoice[0].hiddenLines[line])
                        graphOfChoice[0].legends.append(graphOfChoice[0].hiddenLegends[line])
                        graphOfChoice[0].hiddenLegends.remove(graphOfChoice[0].hiddenLegends[line])
                        graphOfChoice[0].draw()

            #Hides all lines
            elif "hide all" in value.lower():
                if graphOfChoice is not None:
                    graphOfChoice[0].hiddenLines = graphOfChoice[0].data
                    graphOfChoice[0].data = []
                    graphOfChoice[0].hiddenLegends = graphOfChoice[0].legends
                    graphOfChoice[0].legends = []
                    graphOfChoice[0].draw()

            #Hides x line
            elif "hide" in value.lower():
                if graphOfChoice is not None:
                    line = chooseLine(graphOfChoice)
                    if line is not None:
                        graphOfChoice[0].hiddenLines.append(graphOfChoice[0].data[line])
                        graphOfChoice[0].data.remove(graphOfChoice[0].data[line])
                        graphOfChoice[0].hiddenLegends.append(graphOfChoice[0].legends[line])
                        graphOfChoice[0].legends.remove(graphOfChoice[0].legends[line])
                        graphOfChoice[0].draw()
_main = None
_latest = ""

#Setup the program frame with the main text input and output panels
class ProgramFrame(wx.Frame):
    def __init__(self, parent, main):
        global selfV, _main
        _main = main
        self.parent = parent
        wx.Frame.__init__(self, parent, -1, "Programmatic Calculator", size=(1000, 600))
        self.panel = wx.Panel(self, size=(1000, 600))
        wx.StaticText(self.panel, -1, "Enter Expression:", (0, 500), (1000, 100))
        self.textEntry = wx.TextCtrl(self.panel, -1, "", (0, 525), (1000,100), style=wx.TE_PROCESS_ENTER)
        self.textEntry.Bind(wx.EVT_TEXT_ENTER, self.setText)
        self.Bind(wx.EVT_CLOSE, self.onExit)
        self.output = wx.TextCtrl(self.panel, -1, "", (0, 0), (1000,500), style=wx.TE_MULTILINE|wx.TE_READONLY)
        selfV = self
        self.Center()

    #Removes graph from all graphs
    def onExit(self, event):
        for graphFrame in allGraphs:
            graphFrame[0].Close()
        self.Destroy()
        if event is not None:
            event.Skip()

#If enter is pressed then it checks for simple clear or voids.  Else do main or process the text equation.
    def setText(self, event):
        global _latest
        if "clear" in self.textEntry.GetLineText(lineNo=0).lower():
            self.output.Clear()
        elif "void" in self.textEntry.GetLineText(lineNo=0).lower():
            #This is just a cool little graph that I wanted to put in.  Just for fun.  Its been acknowledged that its a junk line but still its kinda cool.
            graphics = GraphicsFrame(None, data=[[[(0.0, -10.0), (2.222048604328897, -9.75), (3.122498999199199, -9.5), (3.799671038392666, -9.25), (4.358898943540674, -9.0), (4.841229182759271, -8.75), (5.267826876426369, -8.5), (5.651327277728657, -8.25), (6.0, -8.0), (6.319612329882269, -7.75), (6.614378277661476, -7.5), (6.887488656977955, -7.25), (7.14142842854285, -7.0), (7.378177281686853, -6.75), (7.599342076785332, -6.5), (7.806247497997997, -6.25), (8.0, -6.0), (8.181534085976786, -5.75), (8.351646544245034, -5.5), (8.511022265274601, -5.25), (8.660254037844387, -5.0), (8.799857953399021, -4.75), (8.930285549745875, -4.5), (9.051933495115836, -4.25), (9.16515138991168, -4.0), (9.270248108869579, -3.75), (9.367496997597597, -3.5), (9.45714015968887, -3.25), (9.539392014169456, -3.0), (9.614442261514705, -2.75), (9.682458365518542, -2.5), (9.743587634952538, -2.25), (9.797958971132712, -2.0), (9.845684333757609, -1.75), (9.886859966642595, -1.5), (9.921567416492215, -1.25), (9.9498743710662, -1.0), (9.971835337589566, -0.75), (9.987492177719089, -0.5), (9.996874511566103, -0.25), (10.0, 0.0), (9.996874511566103, 0.25), (9.987492177719089, 0.5), (9.971835337589566, 0.75), (9.9498743710662, 1.0), (9.921567416492215, 1.25), (9.886859966642595, 1.5), (9.845684333757609, 1.75), (9.797958971132712, 2.0), (9.743587634952538, 2.25), (9.682458365518542, 2.5), (9.614442261514705, 2.75), (9.539392014169456, 3.0), (9.45714015968887, 3.25), (9.367496997597597, 3.5), (9.270248108869579, 3.75), (9.16515138991168, 4.0), (9.051933495115836, 4.25), (8.930285549745875, 4.5), (8.799857953399021, 4.75), (8.660254037844387, 5.0), (8.511022265274601, 5.25), (8.351646544245034, 5.5), (8.181534085976786, 5.75), (8.0, 6.0), (7.806247497997997, 6.25), (7.599342076785332, 6.5), (7.378177281686853, 6.75), (7.14142842854285, 7.0), (6.887488656977955, 7.25), (6.614378277661476, 7.5), (6.319612329882269, 7.75), (6.0, 8.0), (5.651327277728657, 8.25), (5.267826876426369, 8.5), (4.841229182759271, 8.75), (4.358898943540674, 9.0), (3.799671038392666, 9.25), (3.122498999199199, 9.5), (2.222048604328897, 9.75), (0.0, 10.0)]], [[(0.0, -10.0), (-2.222048604328897, -9.75), (-3.122498999199199, -9.5), (-3.799671038392666, -9.25), (-4.358898943540674, -9.0), (-4.841229182759271, -8.75), (-5.267826876426369, -8.5), (-5.651327277728657, -8.25), (-6.0, -8.0), (-6.319612329882269, -7.75), (-6.614378277661476, -7.5), (-6.887488656977955, -7.25), (-7.14142842854285, -7.0), (-7.378177281686853, -6.75), (-7.599342076785332, -6.5), (-7.806247497997997, -6.25), (-8.0, -6.0), (-8.181534085976786, -5.75), (-8.351646544245034, -5.5), (-8.511022265274601, -5.25), (-8.660254037844387, -5.0), (-8.799857953399021, -4.75), (-8.930285549745875, -4.5), (-9.051933495115836, -4.25), (-9.16515138991168, -4.0), (-9.270248108869579, -3.75), (-9.367496997597597, -3.5), (-9.45714015968887, -3.25), (-9.539392014169456, -3.0), (-9.614442261514705, -2.75), (-9.682458365518542, -2.5), (-9.743587634952538, -2.25), (-9.797958971132712, -2.0), (-9.845684333757609, -1.75), (-9.886859966642595, -1.5), (-9.921567416492215, -1.25), (-9.9498743710662, -1.0), (-9.971835337589566, -0.75), (-9.987492177719089, -0.5), (-9.996874511566103, -0.25), (-10.0, 0.0), (-9.996874511566103, 0.25), (-9.987492177719089, 0.5), (-9.971835337589566, 0.75), (-9.9498743710662, 1.0), (-9.921567416492215, 1.25), (-9.886859966642595, 1.5), (-9.845684333757609, 1.75), (-9.797958971132712, 2.0), (-9.743587634952538, 2.25), (-9.682458365518542, 2.5), (-9.614442261514705, 2.75), (-9.539392014169456, 3.0), (-9.45714015968887, 3.25), (-9.367496997597597, 3.5), (-9.270248108869579, 3.75), (-9.16515138991168, 4.0), (-9.051933495115836, 4.25), (-8.930285549745875, 4.5), (-8.799857953399021, 4.75), (-8.660254037844387, 5.0), (-8.511022265274601, 5.25), (-8.351646544245034, 5.5), (-8.181534085976786, 5.75), (-8.0, 6.0), (-7.806247497997997, 6.25), (-7.599342076785332, 6.5), (-7.378177281686853, 6.75), (-7.14142842854285, 7.0), (-6.887488656977955, 7.25), (-6.614378277661476, 7.5), (-6.319612329882269, 7.75), (-6.0, 8.0), (-5.651327277728657, 8.25), (-5.267826876426369, 8.5), (-4.841229182759271, 8.75), (-4.358898943540674, 9.0), (-3.799671038392666, 9.25), (-3.122498999199199, 9.5), (-2.222048604328897, 9.75), (0.0, 10.0)]], [[(2.1065374432940898, -9.25), (3.0, -9.0), (3.665719574653795, -8.75), (4.2130748865881795, -8.5), (4.683748498798798, -8.25), (5.0990195135927845, -8.0), (5.4715171570598224, -7.75), (5.809475019311125, -7.5), (6.118619125260208, -7.25), (6.4031242374328485, -7.0), (6.6661458129866915, -6.75), (6.910137480542627, -6.5), (7.137051211810099, -6.25), (7.3484692283495345, -6.0), (7.545694136393285, -5.75), (7.729812416870153, -5.5), (7.901740314639554, -5.25), (8.06225774829855, -5.0), (8.212033852828421, -4.75), (8.351646544245034, -4.5), (8.481597726843686, -4.25), (8.602325267042627, -4.0), (8.714212528966687, -3.75), (8.817596044274199, -3.5), (8.912771734987944, -3.25), (9.0, -3.0), (9.079509898667439, -2.75), (9.151502608861563, -2.5), (9.216154295583381, -2.25), (9.273618495495704, -2.0), (9.324028099485759, -1.75), (9.367496997597597, -1.5), (9.404121436902013, -1.25), (9.433981132056603, -1.0), (9.45714015968887, -0.75), (9.473647660748208, -0.5), (9.48353836919533, -0.25), (9.486832980505138, 0.0), (9.48353836919533, 0.25), (9.473647660748208, 0.5), (9.45714015968887, 0.75), (9.433981132056603, 1.0), (9.404121436902013, 1.25), (9.367496997597597, 1.5), (9.324028099485759, 1.75), (9.273618495495704, 2.0), (9.216154295583381, 2.25), (9.151502608861563, 2.5), (9.079509898667439, 2.75), (9.0, 3.0), (8.912771734987944, 3.25), (8.817596044274199, 3.5), (8.714212528966687, 3.75), (8.602325267042627, 4.0), (8.481597726843686, 4.25), (8.351646544245034, 4.5), (8.212033852828421, 4.75), (8.06225774829855, 5.0), (7.901740314639554, 5.25), (7.729812416870153, 5.5), (7.545694136393285, 5.75), (7.3484692283495345, 6.0), (7.137051211810099, 6.25), (6.910137480542627, 6.5), (6.6661458129866915, 6.75), (6.4031242374328485, 7.0), (6.118619125260208, 7.25), (5.809475019311125, 7.5), (5.4715171570598224, 7.75), (5.0990195135927845, 8.0), (4.683748498798798, 8.25), (4.2130748865881795, 8.5), (3.665719574653795, 8.75), (3.0, 9.0), (2.1065374432940898, 9.25)]], [[(-2.1065374432940898, -9.25), (-3.0, -9.0), (-3.665719574653795, -8.75), (-4.2130748865881795, -8.5), (-4.683748498798798, -8.25), (-5.0990195135927845, -8.0), (-5.4715171570598224, -7.75), (-5.809475019311125, -7.5), (-6.118619125260208, -7.25), (-6.4031242374328485, -7.0), (-6.6661458129866915, -6.75), (-6.910137480542627, -6.5), (-7.137051211810099, -6.25), (-7.3484692283495345, -6.0), (-7.545694136393285, -5.75), (-7.729812416870153, -5.5), (-7.901740314639554, -5.25), (-8.06225774829855, -5.0), (-8.212033852828421, -4.75), (-8.351646544245034, -4.5), (-8.481597726843686, -4.25), (-8.602325267042627, -4.0), (-8.714212528966687, -3.75), (-8.817596044274199, -3.5), (-8.912771734987944, -3.25), (-9.0, -3.0), (-9.079509898667439, -2.75), (-9.151502608861563, -2.5), (-9.216154295583381, -2.25), (-9.273618495495704, -2.0), (-9.324028099485759, -1.75), (-9.367496997597597, -1.5), (-9.404121436902013, -1.25), (-9.433981132056603, -1.0), (-9.45714015968887, -0.75), (-9.473647660748208, -0.5), (-9.48353836919533, -0.25), (-9.486832980505138, 0.0), (-9.48353836919533, 0.25), (-9.473647660748208, 0.5), (-9.45714015968887, 0.75), (-9.433981132056603, 1.0), (-9.404121436902013, 1.25), (-9.367496997597597, 1.5), (-9.324028099485759, 1.75), (-9.273618495495704, 2.0), (-9.216154295583381, 2.25), (-9.151502608861563, 2.5), (-9.079509898667439, 2.75), (-9.0, 3.0), (-8.912771734987944, 3.25), (-8.817596044274199, 3.5), (-8.714212528966687, 3.75), (-8.602325267042627, 4.0), (-8.481597726843686, 4.25), (-8.351646544245034, 4.5), (-8.212033852828421, 4.75), (-8.06225774829855, 5.0), (-7.901740314639554, 5.25), (-7.729812416870153, 5.5), (-7.545694136393285, 5.75), (-7.3484692283495345, 6.0), (-7.137051211810099, 6.25), (-6.910137480542627, 6.5), (-6.6661458129866915, 6.75), (-6.4031242374328485, 7.0), (-6.118619125260208, 7.25), (-5.809475019311125, 7.5), (-5.4715171570598224, 7.75), (-5.0990195135927845, 8.0), (-4.683748498798798, 8.25), (-4.2130748865881795, 8.5), (-3.665719574653795, 8.75), (-3.0, 9.0), (-2.1065374432940898, 9.25)]], [[(1.8540496217739157, -8.75), (2.7838821814150108, -8.5), (3.4550687402713134, -8.25), (4.0, -8.0), (4.4651427748729375, -7.75), (4.873397172404482, -7.5), (5.238081709939241, -7.25), (5.5677643628300215, -7.0), (5.868347297152751, -6.75), (6.144102863722254, -6.5), (6.398241946034863, -6.25), (6.6332495807108, -6.0), (6.85109480302236, -5.75), (7.053367989832942, -5.5), (7.241374178980119, -5.25), (7.416198487095663, -5.0), (7.578753195612059, -4.75), (7.729812416870153, -4.5), (7.870038119348597, -4.25), (8.0, -4.0), (8.120190884455857, -3.75), (8.231038816577165, -3.5), (8.332916656249479, -3.25), (8.426149773176359, -3.0), (8.511022265274601, -2.75), (8.587782018658833, -2.5), (8.656644846590392, -2.25), (8.717797887081348, -2.0), (8.771402396424417, -1.75), (8.817596044274199, -1.5), (8.856494791959175, -1.25), (8.888194417315589, -1.0), (8.912771734987944, -0.75), (8.930285549745875, -0.5), (8.940777371123833, -0.25), (8.94427190999916, 0.0), (8.940777371123833, 0.25), (8.930285549745875, 0.5), (8.912771734987944, 0.75), (8.888194417315589, 1.0), (8.856494791959175, 1.25), (8.817596044274199, 1.5), (8.771402396424417, 1.75), (8.717797887081348, 2.0), (8.656644846590392, 2.25), (8.587782018658833, 2.5), (8.511022265274601, 2.75), (8.426149773176359, 3.0), (8.332916656249479, 3.25), (8.231038816577165, 3.5), (8.120190884455857, 3.75), (8.0, 4.0), (7.870038119348597, 4.25), (7.729812416870153, 4.5), (7.578753195612059, 4.75), (7.416198487095663, 5.0), (7.241374178980119, 5.25), (7.053367989832942, 5.5), (6.85109480302236, 5.75), (6.6332495807108, 6.0), (6.398241946034863, 6.25), (6.144102863722254, 6.5), (5.868347297152751, 6.75), (5.5677643628300215, 7.0), (5.238081709939241, 7.25), (4.873397172404482, 7.5), (4.4651427748729375, 7.75), (4.0, 8.0), (3.4550687402713134, 8.25), (2.7838821814150108, 8.5), (1.8540496217739157, 8.75)]], [[(-1.8540496217739157, -8.75), (-2.7838821814150108, -8.5), (-3.4550687402713134, -8.25), (-4.0, -8.0), (-4.4651427748729375, -7.75), (-4.873397172404482, -7.5), (-5.238081709939241, -7.25), (-5.5677643628300215, -7.0), (-5.868347297152751, -6.75), (-6.144102863722254, -6.5), (-6.398241946034863, -6.25), (-6.6332495807108, -6.0), (-6.85109480302236, -5.75), (-7.053367989832942, -5.5), (-7.241374178980119, -5.25), (-7.416198487095663, -5.0), (-7.578753195612059, -4.75), (-7.729812416870153, -4.5), (-7.870038119348597, -4.25), (-8.0, -4.0), (-8.120190884455857, -3.75), (-8.231038816577165, -3.5), (-8.332916656249479, -3.25), (-8.426149773176359, -3.0), (-8.511022265274601, -2.75), (-8.587782018658833, -2.5), (-8.656644846590392, -2.25), (-8.717797887081348, -2.0), (-8.771402396424417, -1.75), (-8.817596044274199, -1.5), (-8.856494791959175, -1.25), (-8.888194417315589, -1.0), (-8.912771734987944, -0.75), (-8.930285549745875, -0.5), (-8.940777371123833, -0.25), (-8.94427190999916, 0.0), (-8.940777371123833, 0.25), (-8.930285549745875, 0.5), (-8.912771734987944, 0.75), (-8.888194417315589, 1.0), (-8.856494791959175, 1.25), (-8.817596044274199, 1.5), (-8.771402396424417, 1.75), (-8.717797887081348, 2.0), (-8.656644846590392, 2.25), (-8.587782018658833, 2.5), (-8.511022265274601, 2.75), (-8.426149773176359, 3.0), (-8.332916656249479, 3.25), (-8.231038816577165, 3.5), (-8.120190884455857, 3.75), (-8.0, 4.0), (-7.870038119348597, 4.25), (-7.729812416870153, 4.5), (-7.578753195612059, 4.75), (-7.416198487095663, 5.0), (-7.241374178980119, 5.25), (-7.053367989832942, 5.5), (-6.85109480302236, 5.75), (-6.6332495807108, 6.0), (-6.398241946034863, 6.25), (-6.144102863722254, 6.5), (-5.868347297152751, 6.75), (-5.5677643628300215, 7.0), (-5.238081709939241, 7.25), (-4.873397172404482, 7.5), (-4.4651427748729375, 7.75), (-4.0, 8.0), (-3.4550687402713134, 8.25), (-2.7838821814150108, 8.5), (-1.8540496217739157, 8.75)]], [[(1.0, -7.0), (2.1065374432940898, -6.75), (2.7838821814150108, -6.5), (3.307189138830738, -6.25), (3.7416573867739413, -6.0), (4.115519408288582, -5.75), (4.444097208657794, -5.5), (4.736823830374104, -5.25), (5.0, -5.0), (5.238081709939241, -4.75), (5.454356057317857, -4.5), (5.651327277728657, -4.25), (5.830951894845301, -4.0), (5.994789404140899, -3.75), (6.144102863722254, -3.5), (6.279928343540235, -3.25), (6.4031242374328485, -3.0), (6.514407110397691, -2.75), (6.614378277661476, -2.5), (6.703543838895961, -2.25), (6.782329983125268, -2.0), (6.85109480302236, -1.75), (6.910137480542627, -1.5), (6.959705453537527, -1.25), (7.0, -1.0), (7.031180555212616, -0.75), (7.053367989832942, -0.5), (7.066647012551285, -0.25), (7.0710678118654755, 0.0), (7.066647012551285, 0.25), (7.053367989832942, 0.5), (7.031180555212616, 0.75), (7.0, 1.0), (6.959705453537527, 1.25), (6.910137480542627, 1.5), (6.85109480302236, 1.75), (6.782329983125268, 2.0), (6.703543838895961, 2.25), (6.614378277661476, 2.5), (6.514407110397691, 2.75), (6.4031242374328485, 3.0), (6.279928343540235, 3.25), (6.144102863722254, 3.5), (5.994789404140899, 3.75), (5.830951894845301, 4.0), (5.651327277728657, 4.25), (5.454356057317857, 4.5), (5.238081709939241, 4.75), (5.0, 5.0), (4.736823830374104, 5.25), (4.444097208657794, 5.5), (4.115519408288582, 5.75), (3.7416573867739413, 6.0), (3.307189138830738, 6.25), (2.7838821814150108, 6.5), (2.1065374432940898, 6.75), (1.0, 7.0)]], [[(-1.0, -7.0), (-2.1065374432940898, -6.75), (-2.7838821814150108, -6.5), (-3.307189138830738, -6.25), (-3.7416573867739413, -6.0), (-4.115519408288582, -5.75), (-4.444097208657794, -5.5), (-4.736823830374104, -5.25), (-5.0, -5.0), (-5.238081709939241, -4.75), (-5.454356057317857, -4.5), (-5.651327277728657, -4.25), (-5.830951894845301, -4.0), (-5.994789404140899, -3.75), (-6.144102863722254, -3.5), (-6.279928343540235, -3.25), (-6.4031242374328485, -3.0), (-6.514407110397691, -2.75), (-6.614378277661476, -2.5), (-6.703543838895961, -2.25), (-6.782329983125268, -2.0), (-6.85109480302236, -1.75), (-6.910137480542627, -1.5), (-6.959705453537527, -1.25), (-7.0, -1.0), (-7.031180555212616, -0.75), (-7.053367989832942, -0.5), (-7.066647012551285, -0.25), (-7.0710678118654755, 0.0), (-7.066647012551285, 0.25), (-7.053367989832942, 0.5), (-7.031180555212616, 0.75), (-7.0, 1.0), (-6.959705453537527, 1.25), (-6.910137480542627, 1.5), (-6.85109480302236, 1.75), (-6.782329983125268, 2.0), (-6.703543838895961, 2.25), (-6.614378277661476, 2.5), (-6.514407110397691, 2.75), (-6.4031242374328485, 3.0), (-6.279928343540235, 3.25), (-6.144102863722254, 3.5), (-5.994789404140899, 3.75), (-5.830951894845301, 4.0), (-5.651327277728657, 4.25), (-5.454356057317857, 4.5), (-5.238081709939241, 4.75), (-5.0, 5.0), (-4.736823830374104, 5.25), (-4.444097208657794, 5.5), (-4.115519408288582, 5.75), (-3.7416573867739413, 6.0), (-3.307189138830738, 6.25), (-2.7838821814150108, 6.5), (-2.1065374432940898, 6.75), (-1.0, 7.0)]], [[(0.0, -5.0), (1.5612494995995996, -4.75), (2.179449471770337, -4.5), (2.6339134382131846, -4.25), (3.0, -4.0), (3.307189138830738, -3.75), (3.570714214271425, -3.5), (3.799671038392666, -3.25), (4.0, -3.0), (4.175823272122517, -2.75), (4.330127018922194, -2.5), (4.4651427748729375, -2.25), (4.58257569495584, -2.0), (4.683748498798798, -1.75), (4.769696007084728, -1.5), (4.841229182759271, -1.25), (4.898979485566356, -1.0), (4.943429983321297, -0.75), (4.9749371855331, -0.5), (4.993746088859544, -0.25), (5.0, 0.0), (4.993746088859544, 0.25), (4.9749371855331, 0.5), (4.943429983321297, 0.75), (4.898979485566356, 1.0), (4.841229182759271, 1.25), (4.769696007084728, 1.5), (4.683748498798798, 1.75), (4.58257569495584, 2.0), (4.4651427748729375, 2.25), (4.330127018922194, 2.5), (4.175823272122517, 2.75), (4.0, 3.0), (3.799671038392666, 3.25), (3.570714214271425, 3.5), (3.307189138830738, 3.75), (3.0, 4.0), (2.6339134382131846, 4.25), (2.179449471770337, 4.5), (1.5612494995995996, 4.75), (0.0, 5.0)]], [[(0.0, -5.0), (-1.5612494995995996, -4.75), (-2.179449471770337, -4.5), (-2.6339134382131846, -4.25), (-3.0, -4.0), (-3.307189138830738, -3.75), (-3.570714214271425, -3.5), (-3.799671038392666, -3.25), (-4.0, -3.0), (-4.175823272122517, -2.75), (-4.330127018922194, -2.5), (-4.4651427748729375, -2.25), (-4.58257569495584, -2.0), (-4.683748498798798, -1.75), (-4.769696007084728, -1.5), (-4.841229182759271, -1.25), (-4.898979485566356, -1.0), (-4.943429983321297, -0.75), (-4.9749371855331, -0.5), (-4.993746088859544, -0.25), (-5.0, 0.0), (-4.993746088859544, 0.25), (-4.9749371855331, 0.5), (-4.943429983321297, 0.75), (-4.898979485566356, 1.0), (-4.841229182759271, 1.25), (-4.769696007084728, 1.5), (-4.683748498798798, 1.75), (-4.58257569495584, 2.0), (-4.4651427748729375, 2.25), (-4.330127018922194, 2.5), (-4.175823272122517, 2.75), (-4.0, 3.0), (-3.799671038392666, 3.25), (-3.570714214271425, 3.5), (-3.307189138830738, 3.75), (-3.0, 4.0), (-2.6339134382131846, 4.25), (-2.179449471770337, 4.5), (-1.5612494995995996, 4.75), (0.0, 5.0)]], [[(0.5, -3.5), (1.3919410907075054, -3.25), (1.8708286933869707, -3.0), (2.222048604328897, -2.75), (2.5, -2.5), (2.7271780286589284, -2.25), (2.9154759474226504, -2.0), (3.072051431861127, -1.75), (3.2015621187164243, -1.5), (3.307189138830738, -1.25), (3.391164991562634, -1.0), (3.4550687402713134, -0.75), (3.5, -0.5), (3.526683994916471, -0.25), (3.5355339059327378, 0.0), (3.526683994916471, 0.25), (3.5, 0.5), (3.4550687402713134, 0.75), (3.391164991562634, 1.0), (3.307189138830738, 1.25), (3.2015621187164243, 1.5), (3.072051431861127, 1.75), (2.9154759474226504, 2.0), (2.7271780286589284, 2.25), (2.5, 2.5), (2.222048604328897, 2.75), (1.8708286933869707, 3.0), (1.3919410907075054, 3.25), (0.5, 3.5)]], [[(-0.5, -3.5), (-1.3919410907075054, -3.25), (-1.8708286933869707, -3.0), (-2.222048604328897, -2.75), (-2.5, -2.5), (-2.7271780286589284, -2.25), (-2.9154759474226504, -2.0), (-3.072051431861127, -1.75), (-3.2015621187164243, -1.5), (-3.307189138830738, -1.25), (-3.391164991562634, -1.0), (-3.4550687402713134, -0.75), (-3.5, -0.5), (-3.526683994916471, -0.25), (-3.5355339059327378, 0.0), (-3.526683994916471, 0.25), (-3.5, 0.5), (-3.4550687402713134, 0.75), (-3.391164991562634, 1.0), (-3.307189138830738, 1.25), (-3.2015621187164243, 1.5), (-3.072051431861127, 1.75), (-2.9154759474226504, 2.0), (-2.7271780286589284, 2.25), (-2.5, 2.5), (-2.222048604328897, 2.75), (-1.8708286933869707, 3.0), (-1.3919410907075054, 3.25), (-0.5, 3.5)]], [[(1.0, -2.0), (1.3919410907075054, -1.75), (1.6583123951777, -1.5), (1.8540496217739157, -1.25), (2.0, -1.0), (2.1065374432940898, -0.75), (2.179449471770337, -0.5), (2.222048604328897, -0.25), (2.23606797749979, 0.0), (2.222048604328897, 0.25), (2.179449471770337, 0.5), (2.1065374432940898, 0.75), (2.0, 1.0), (1.8540496217739157, 1.25), (1.6583123951777, 1.5), (1.3919410907075054, 1.75), (1.0, 2.0)]], [[(-1.0, -2.0), (-1.3919410907075054, -1.75), (-1.6583123951777, -1.5), (-1.8540496217739157, -1.25), (-2.0, -1.0), (-2.1065374432940898, -0.75), (-2.179449471770337, -0.5), (-2.222048604328897, -0.25), (-2.23606797749979, 0.0), (-2.222048604328897, 0.25), (-2.179449471770337, 0.5), (-2.1065374432940898, 0.75), (-2.0, 1.0), (-1.8540496217739157, 1.25), (-1.6583123951777, 1.5), (-1.3919410907075054, 1.75), (-1.0, 2.0)]]], x=(-10, 10), y=(-10, 10), expression="Void")
            graphics.Show()
        else:
            _latest = self.textEntry.GetLineText(lineNo=0)
            #Getting in-editor error saying _main is not callable.  No actual error just the in-editor not recognising that the global is fine.  Importing a global when its not needed wastes resources so this is faster and has no negative effect.
            _main(_latest)
        self.textEntry.Clear()

#Logs the text to the text control
#This is essentially the print function
    def logText(self, text):
        self.output.AppendText(text + "\n")