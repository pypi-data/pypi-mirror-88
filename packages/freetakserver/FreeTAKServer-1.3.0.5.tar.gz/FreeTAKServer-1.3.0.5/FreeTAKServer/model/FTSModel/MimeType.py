from FreeTAKServer.model.FTSModelVariables.MimeTypeVariables import MimeTypeVariables as vars
class MimeType:
    def __init__(self):
        self.INTAG = None

    @staticmethod
    def ExcheckUpdate(INTAG = vars.ExcheckUpdate().INTAG):
        mimetype = MimeType()
        mimetype.setINTAG(INTAG)
        return mimetype

    def setINTAG(self, INTAG):
        self.INTAG = INTAG

    def getINTAG(self):
        return self.INTAG