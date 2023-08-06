from FreeTAKServer.model.FTSModelVariables.CreatorCallsignVariables import CreatorCallsignVariables as vars

class CreatorCallsign:
    @staticmethod
    def Checklist(INTAG = vars.Checklist().INTAG):
        creatorCallsign = CreatorCallsign()
        creatorCallsign.setINTAG(INTAG)
        return creatorCallsign

    def setINTAG(self, INTAG):
        self.INTAG = INTAG

    def getINTAG(self):
        return self.INTAG