import StatusChecker

checker = StatusChecker.StatusChecker.StatusChecker()
checker.addWebCallTask("test", "http://www.google.de")
checker.runMainLoop()