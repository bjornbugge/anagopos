import wx
from wx import glcanvas
from glgrapharea import MyCubeCanvas
from glgrapharea import MyCanvasBase



class MainWindow(wx.Frame):

	def __init__(self, parent = None, id = -1, title = "Reduction Visualizer"):
		# Init
		wx.Frame.__init__(
				self, parent, id, title, size = (1366,768),
				style = wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE
		)
		
		graph = None
		drawing = MyCubeCanvas(self)
		# drawing = GraphArea(graph)
		drawing.ready = False
		drawing.shownewestedget = False

		# Buttons
		tf1 = wx.TextCtrl(self, 0, size=(200, 100), style = wx.TE_MULTILINE)
		bt1 = wx.Button(self, 0, "Draw Graph")
		bt2 = wx.Button(self, 0, "Generate Random Lambda term")
		bt3 = wx.Button(self, 0, "Forward")
		bt4 = wx.Button(self, 0, "Back")
		bt5 = wx.Button(self, 0, "Redraw Graph")
		bt6 = wx.Button(self, 0, "Optimize Graph")
		st1 = wx.StaticText(self, -1, 'Select Drawing Alg: ', (5, 5))
		cb1 = wx.ComboBox(self, -1, size=(120, -1))
		st2 = wx.CheckBox(self, -1, 'Start')
		st3 = wx.StaticText(self, -1, 'Clicked Term: ', (5, 5))
		tf2 = wx.TextCtrl(self, 0, size=(200, 100), style = wx.TE_MULTILINE|wx.TE_READONLY)
		st4 = wx.StaticText(self, -1, 'Output: ', (5, 5))
		tf3 = wx.TextCtrl(self, 0, size=(200, 100), style = wx.TE_MULTILINE|wx.TE_READONLY)
		
		# Button actions
		bt1.Bind(wx.EVT_BUTTON, self.DrawGraph)
		bt2.Bind(wx.EVT_BUTTON, self.Generate)
		bt3.Bind(wx.EVT_BUTTON, self.Forward)
		bt4.Bind(wx.EVT_BUTTON, self.Back)
		bt5.Bind(wx.EVT_BUTTON, self.Redraw)
		bt6.Bind(wx.EVT_BUTTON, self.Optimize)
		
		bts = wx.BoxSizer(wx.VERTICAL)
		bts.Add(tf1, 0, wx.ALIGN_CENTER|wx.ALL, 10)
		bts.Add(bt1, 0, wx.ALIGN_CENTER|wx.ALL, 3)
		bts.Add(bt2, 0, wx.ALIGN_CENTER|wx.ALL, 3)
		bts.Add(bt3, 0, wx.ALIGN_CENTER|wx.ALL, 3)
		bts.Add(bt4, 0, wx.ALIGN_CENTER|wx.ALL, 3)
		bts.Add(bt5, 0, wx.ALIGN_CENTER|wx.ALL, 3)
		bts.Add(bt6, 0, wx.ALIGN_CENTER|wx.ALL, 3)
		bts.Add(st1, 0, wx.ALIGN_CENTER|wx.ALL, 3)
		bts.Add(cb1, 0, wx.ALIGN_CENTER|wx.ALL, 3)
		bts.Add(st2, 0, wx.ALIGN_CENTER|wx.ALL, 3)
		bts.Add(st3, 0, wx.ALIGN_CENTER|wx.ALL, 3)
		bts.Add(tf2, 0, wx.ALIGN_CENTER|wx.ALL, 3)
		bts.Add(st4, 0, wx.ALIGN_CENTER|wx.ALL, 3)
		bts.Add(tf3, 0, wx.ALIGN_CENTER|wx.ALL, 3)
		
		box = wx.BoxSizer(wx.HORIZONTAL)
		box.Add(bts, 0, wx.ALIGN_TOP, 15)
		box.Add(drawing, 1, wx.EXPAND)
		
		self.SetAutoLayout(True)
		self.SetSizer(box)
		self.Layout()

		# StatusBar
		self.CreateStatusBar()

		# Filemenu
		filemenu = wx.Menu()

		# Filemenu - About
		menuitem = filemenu.Append(-1, "&About", "Reduction Visualizer")
		self.Bind(wx.EVT_MENU, self.OnAbout, menuitem) # here comes the event-handler
		# Filemenu - Separator
		filemenu.AppendSeparator()

		# Filemenu - Exit
		menuitem = filemenu.Append(-1, "E&xit", "Terminate the program")
		self.Bind(wx.EVT_MENU, self.OnExit, menuitem) # here comes the event-handler

		# Menubar
		menubar = wx.MenuBar()
		menubar.Append(filemenu,"&File")
		self.SetMenuBar(menubar)

		# Show
		self.Show(True)


	def OnAbout(self,event):
		message = "Reduction Visualizer\n\nURL:\nhttp://code.google.com/p/reduction-visualizer/\n\nBy:\n Niels Bjørn Bugge Grathwohl\n Jens Duelund Pallesen"
		caption = "Reduction Visualizer"
		wx.MessageBox(message, caption, wx.OK)
	
	def OnExit(self,event):
		self.Close(True)
	
	def DrawGraph(self,event):
		print "DrawGraph"
	
	def Generate(self,event):
		print "Generate"
	
	def Forward(self,event):
		print "Forward"
	
	def Back(self,event):
		print "Back"
	
	def Optimize(self,event):
		print "Optimize"
	
	def Redraw(self,event):
		print "Redraw"


app = wx.PySimpleApp()
frame = MainWindow()
app.MainLoop()

# destroying the objects, so that this script works more than once in IDLEdieses Beispiel
del frame
del app