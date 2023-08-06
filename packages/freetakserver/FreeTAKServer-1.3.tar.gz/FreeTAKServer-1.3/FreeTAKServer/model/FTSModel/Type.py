from FreeTAKServer.model.FTSModelVariables.TypeVariables import TypeVariables as vars

class Type:
    def __init__(self):
        self.INTAG = None

    @staticmethod
    def ExcheckUpdate(INTAG=vars.ExcheckUpdate().INTAG, ):
        type = Type()

        type.setINTAG(INTAG)

        return type

    def setINTAG(self, INTAG):
        self.INTAG = INTAG

    def getINTAG(self):
        return self.INTAG
