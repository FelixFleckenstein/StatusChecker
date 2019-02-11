import wx
import cx_Oracle
import threading
import configparser


config = configparser.ConfigParser()
config.read('config.ini')

class App(wx.App):
	def OnInit(self):	
		frame=wx.Frame(None)
		self.SetTopWindow(frame)
		return True
		
class StatusChecker:
	def __init__(self):
		self.app = App(False)
		self.tasks = TaskChecker()
		
	def addWebCallTask(self, name, url):
		self.tasks.addWebCallTask(name, url)
		
	def addDBTask(self, name, sql):
		self.tasks.addDBTask(name, sql)

	def runMainLoop(self):
		#Oracle DB-Connection starten
		#con = cx_Oracle.connect(config['DB']['user'], config['DB']['pass'], cx_Oracle.makedsn(config['DB']['url'], config['DB']['port'], config['DB']['ssid']), cx_Oracle.SYSDBA)
		con = None
		
		tBar = TaskBarIcon(frame, con)
		
		th = threading.Thread(target=self.tasks.checkTasks, args=(tBar, con,))
		tBar.set_main_thread(th)
		th.start()
		
		self.app.MainLoop()