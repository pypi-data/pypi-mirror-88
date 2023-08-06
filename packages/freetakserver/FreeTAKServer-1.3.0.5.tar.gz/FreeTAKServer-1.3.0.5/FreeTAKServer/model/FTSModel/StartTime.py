from FreeTAKServer.model.FTSModelVariables.StartTimeVariables import StartTimeVariables as vars

class StartTime:
    @staticmethod
    def Checklist(INTAG = vars.Checklist().INTAG):
        starttime = StartTime()
        starttime.setINTAG(INTAG)
        return starttime

    def setINTAG(self, INTAG):
        self.INTAG = INTAG

    def getINTAG(self):
        return self.INTAG