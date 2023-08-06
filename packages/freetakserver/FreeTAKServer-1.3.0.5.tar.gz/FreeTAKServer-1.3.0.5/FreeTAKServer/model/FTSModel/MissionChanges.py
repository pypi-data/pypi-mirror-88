from FreeTAKServer.model.FTSModel.MissionChange import MissionChange

class MissionChanges:
    def __init__(self):
        pass

    @staticmethod
    def ExcheckUpdate():
        missionchanges = MissionChanges()
        missionchanges.MissionChange = MissionChange.ExcheckUpdate()
        return missionchanges

