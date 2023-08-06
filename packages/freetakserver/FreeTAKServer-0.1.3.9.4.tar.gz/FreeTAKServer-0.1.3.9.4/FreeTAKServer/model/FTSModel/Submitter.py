from FreeTAKServer.model.FTSModelVariables.SubmitterVariables import SubmitterVariables as vars

class Submitter:
    def __init__(self):
        self.INTAG = None

    @staticmethod
    def ExcheckUpdate(INTAG=vars.ExcheckUpdate().INTAG, ):
        submitter = Submitter()

        submitter.setINTAG(INTAG)

        return submitter

    def setINTAG(self, INTAG):
        self.INTAG = INTAG

    def getINTAG(self):
        return self.INTAG