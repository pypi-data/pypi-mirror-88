import mxdevtool as mx
import numpy as np

class Rsg(mx.core_Rsg):
    def __init__(self, sampleNum, dimension=365, seed=0, skip=0, isMomentMatching=False, randomType='pseudo', subType='mersennetwister', randomTransformType='boxmullernormal'):
        self.randomType = randomType
        self.subType = subType
        self.randomTransformType = randomTransformType

        mx.core_Rsg.__init__(self, sampleNum, dimension, seed, skip, isMomentMatching, randomType, subType, randomTransformType)
        

class ScenarioGenerator(mx.core_ScenarioGenerator2):
    def __init__(self, models, calcs, corr, timegrid, rsg, filename, isMomentMatching = False):
        _corr = mx.Matrix(corr)

        _dimension = (len(timegrid) - 1) * len(models)
        _rsg = Rsg(rsg.sampleNum, _dimension, rsg.seed, rsg.skip, rsg.isMomentMatching, rsg.randomType, rsg.subType, rsg.randomTransformType)

        mx.core_ScenarioGenerator2.__init__(self, models, calcs, _corr, timegrid, _rsg, filename, isMomentMatching)
    
    
class ScenarioResults(mx.core_ScenarioResult):
    def __init__(self, filename):
        mx.core_ScenarioResult.__init__(self, filename)
        self.shape = (self.simulNum, self.assetNum, self.timegridNum) 

    def toNumpyArr(self):
        npz = np.load(self.filename)
        arr = npz['data']
        arr.reshape(self.shape)

        return arr

    # def assetPath(self, asset):
    #     """
    #     name or num
    #     docstring
    #     """
    #     pass

    def __getitem__(self, scenCount):
        return self._multiPath(scenCount)

    def tPosSlice(self, t_pos, scenCount=None):
        if scenCount is None:
            return self._multiPathAllTPos(t_pos)
        else:
            return self._multiPathTPos(scenCount, t_pos)

    def timeSlice(self, time, scenCount=None):
        if scenCount is None:
            return self._multiPathAllTPosInterpolateTime(time)
        else:
            return self._multiPathTPosInterpolateTime(scenCount, time)

    def dateSlice(self, date, scenCount=None):
        if scenCount is None:
            return self._multiPathAllTPosInterpolateDate(date)
        else:
            return self._multiPathTPosInterpolateDate(scenCount, date)


def generate1d(model, calcs, timegrid, rsg, filename, isMomentMatching = False):
    _calcs = calcs

    if calcs is None:
        _calcs = []

    corr = mx.IdentityMatrix(1)

    generator = ScenarioGenerator([model], _calcs, corr, timegrid, rsg, filename, isMomentMatching)
    generator.generate()

    return ScenarioResults(filename)

def generate(models, calcs, corr, timegrid, rsg, filename, isMomentMatching = False):
    if calcs is None:
        calcs = []

    generator = ScenarioGenerator(models, calcs, corr, timegrid, rsg, filename, isMomentMatching)
    generator.generate()

    return ScenarioResults(filename)