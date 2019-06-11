import wx
import cx_Oracle
import threading
import configparser

from StatusChecker.TaskChecker import *
from StatusChecker.TaskBarIcon import *

config = configparser.ConfigParser()
config.read('config.ini')
config.read('config.dev.ini')  #Developer Configdatei, welche in .gitignore steht

class App(wx.App):
	def OnInit(self):	
		frame=wx.Frame(None)
		self.frame = frame
		self.SetTopWindow(frame)
		return True
		
class StatusChecker:
	def __init__(self):
		self.app = App(False)
		self.tasks = TaskChecker()
		
	def addWebCallTask(self, name, url, warningValue = None, errorValue = None, counter_measurement = None):
		self.tasks.addWebCallTask(name, url, warningValue, errorValue, counter_measurement)
		
	def addDBTask(self, name, sql, warningValue = None, errorValue = None, counter_measurement = None):
		self.tasks.addDBTask(name, sql, warningValue, errorValue, counter_measurement)

	def runMainLoop(self):
		#Oracle DB-Connection starten
		con = cx_Oracle.connect(config['DB']['user'], config['DB']['pass'], cx_Oracle.makedsn(config['DB']['url'], config['DB']['port'], config['DB']['ssid']), cx_Oracle.SYSDBA)
		
		tBar = TaskBarIcon(self.app.frame, con)
		
		th = threading.Thread(target=self.tasks.checkTasks, args=(tBar, con,))
		tBar.set_main_thread(th)
		th.start()
		
		self.app.MainLoop()