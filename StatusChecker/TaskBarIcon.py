import wx.adv
import wx

TRAY_TOOLTIP = 'StatusChecker' 
TRAY_ICON_GREEN = 'iconGreen.png' 

def create_menu_item(menu, label, func):
		item = wx.MenuItem(menu, -1, label)
		menu.Bind(wx.EVT_MENU, func, id=item.GetId())
		menu.Append(item)
		return item

class TaskBarIcon(wx.adv.TaskBarIcon):
	def __init__(self, frame, con):
		self.frame = frame
		super(TaskBarIcon, self).__init__()
		self.set_icon(TRAY_ICON_GREEN)
		self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)
		self.con = con

	def CreatePopupMenu(self):
		menu = wx.Menu()
		create_menu_item(menu, 'Solved', self.on_solved)
		#create_menu_item(menu, 'Site 2', self.on_zwei)
		menu.AppendSeparator()
		create_menu_item(menu, 'Exit', self.on_exit)
		return menu

	def set_main_thread(self, th):
		self.th = th
		
	def set_icon(self, path):
		icon = wx.Icon(path)
		self.SetIcon(icon, TRAY_TOOLTIP)

	def on_left_down(self, event):	  
		print ('Tray icon was left-clicked.')

	def on_solved(self, event):
		self.set_icon(TRAY_ICON_GREEN)
		print ('Hello, world!')

	def on_zwei(self, event):
		#self.set_icon(TRAY_ICON_RED)
		print ('Zwei!')

	def on_exit(self, event):
		self.th.running = False
		self.th.join()
			
		self.con.close()
		wx.CallAfter(self.Destroy)
		self.frame.Close()