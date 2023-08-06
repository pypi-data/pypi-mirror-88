from FreeTAKServer.model.FTSModelVariables.HashVariables import HashVariables as vars

class Hash:
    def __init__(self):
        self.INTAG = None

    @staticmethod
    def ExcheckUpdate(INTAG=vars.ExcheckUpdate().INTAG, ):
        hash = Hash()

        hash.setINTAG(INTAG)

        return hash

    def setINTAG(self, INTAG):
        self.INTAG = INTAG

    def getINTAG(self):
        return self.INTAG