import StatusChecker

checker = StatusChecker.StatusChecker.StatusChecker()

#Website Task
checker.addWebCallTask("Google", "http://www.google.com")

#DB-Task
checker.addDBTask("DB-Locks", "select * from v$locked_object", 1, 5)

checker.runMainLoop()
