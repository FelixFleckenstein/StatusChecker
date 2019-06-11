class Task:
	def __init__(self, name, type, url, sql, warningValue = None, errorValue = None, counter_measurement = None):
		self.name = name
		self.type = type
		self.url = url
		self.sql = sql
		
		self.countInRow = 0
		self.erg = 0
		
		self.errorObjects = []
		
		if warningValue is None:
			self.warningValue = 1
		else:
			self.warningValue = warningValue
			
		if errorValue is None:
			self.errorValue = 1
		else:
			self.errorValue = errorValue
			
		if counter_measurement is None:
			self.counter_measurement = ""
		else:
			self.counter_measurement = counter_measurement