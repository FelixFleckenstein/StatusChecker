from StatusChecker.Task import *
import threading
import datetime
import time
import requests
import cx_Oracle

TRAY_ICON_GREEN = 'iconGreen.png' 
TRAY_ICON_BLUE = 'iconBlue.png'
TRAY_ICON_RED = 'iconRed.png'

TYPE_URL_TEST = 1
TYPE_SQL_TEST = 2

class TaskChecker:
	def __init__(self):
		self.tasks = []

	def addWebCallTask(self, name, url):	
		self.tasks.append(Task(name, TYPE_URL_TEST, url, ''))
	
	def addDBTask(self, name, sql):
		self.tasks.append(Task(name, TYPE_SQL_TEST, '', sql))
		
	def checkTasks(self, tBar, con):
		t = threading.currentThread()
		while getattr(t, "running", True):
			isError = False
			ret = True
		
			for task in self.tasks:		
				if task.type == TYPE_URL_TEST:
					ret = self.executeWebCallTask(task.url)
				elif task.type == TYPE_SQL_TEST:
					ret = self.executeSQLTask(task.sql, con)
		
				if not ret:
					ts = time.time()
					st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
					print(st + ": Fehler: " + task.name)
					isError = True
				
			if isError:
				tBar.set_icon(TRAY_ICON_RED)
			else:
				tBar.set_icon(TRAY_ICON_GREEN)
		
			time.sleep(60);

	def executeWebCallTask(self, url):
		try:
			output = requests.get(url)
				
			if(output.status_code != 200):			
				return False
		except:
			return False
		
		return True

	def executeSQLTask(self, sql, con):
		try:
			cur = con.cursor()
			cur.execute(sql)
			for result in cur:
				return False

			cur.close()	
		except:
			return False
			
		return True