from StatusChecker.Task import *
from StatusChecker.ErrorObject import *
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

	def addWebCallTask(self, name, url, warningValue = None, errorValue = None, counter_measurement = None):	
		self.tasks.append(Task(name, TYPE_URL_TEST, url, '', warningValue, errorValue, counter_measurement))
	
	def addDBTask(self, name, sql, warningValue = None, errorValue = None, counter_measurement = None):
		self.tasks.append(Task(name, TYPE_SQL_TEST, '', sql, warningValue, errorValue, counter_measurement))
		
	def checkTasks(self, tBar, con):
		t = threading.currentThread()
		while getattr(t, "running", True):
			isError = False
			ret = True
		
			for task in self.tasks:			
				if task.type == TYPE_URL_TEST:
					ret = self.executeWebCallTask(task, task.url)
				elif task.type == TYPE_SQL_TEST:
					ret = self.executeSQLTask(task, task.sql, con)
		
				if not ret:
					task.countInRow += 1
					
					if task.countInRow >= task.errorValue:
						ts = time.time()
						st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
						print(st + ": Fehler: " + task.name)
						isError = True
					else:
						ts = time.time()
						st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
						print(st + ": Counting: " + task.name + " => " + str(task.countInRow))						
				
			if isError:
				tBar.set_icon(TRAY_ICON_RED)
			else:
				if ret:
					task.countInRow = 0
				tBar.set_icon(TRAY_ICON_GREEN)
		
			time.sleep(60);

	def executeWebCallTask(self, task, url):
		try:
			output = requests.get(url)
				
			if(output.status_code != 200):			
				return False
		except:
			print("Exception in executeWebCallTask !!!")
			return False
		
		return True

	def executeSQLTask(self, task, sql, con):
		try:
			isError = False
			
			for t in task.errorObjects:
				t.again = 0
			
			cur = con.cursor()
			cur.execute(sql)
			for result in cur:
				found = False
				for t in task.errorObjects:
					if t.value == result:
						t.again = 1
						found = True
				
				if not found:
					task.errorObjects.append(ErrorObject(result, 2)) #2 for not deleting in next Step, but not counting for "again" error
						
				print(result)
				
					
			for t in task.errorObjects:
				if t.again == 0:
					task.errorObjects.remove(t)
				
			for t in task.errorObjects:
				if t.again == 1:
					isError = True
				
			if isError:
				if task.counter_measurement != "":
					cur = con.cursor()
					cur.execute(task.counter_measurement)
				return False

			cur.close()	
		except Exception as e:
			print(e)
			print("Exception in executeSQLTask !!!")
			return False
			
		return True