import mxdevtool as mx


class BlackConstantVol(mx.core_BlackConstantVol):
    def __init__(self, refDate, vol, calendar=None, dayCounter=mx.Actual365Fixed()):
        if isinstance(refDate, mx.Date):
            _refDate = refDate
        else:
            _refDate = mx.Date(refDate)

        _calendar = calendar

        if _calendar is None:
            _calendar = mx.default_calendar()
            
        mx.core_BlackConstantVol.__init__(self, _refDate, vol, _calendar, dayCounter)

class BlackVarianceCurve(mx.core_BlackVarianceCurve):
    def __init__(self, refDate, periods, volatilities, 
                   interpolationType=mx.Interpolator1D.Linear, 
                   calendar=None,
                   dayCounter=mx.Actual365Fixed(), 
                   businessDayConvention=mx.ModifiedFollowing):
        if isinstance(refDate, mx.Date):
            _refDate = refDate
        else:
            _refDate = mx.Date(refDate)

        _periods = periods
        _calendar = calendar

        if _calendar is None:
            _calendar = mx.default_calendar()

        mx.core_BlackVarianceCurve.__init__(self, _refDate, _periods, volatilities, interpolationType,
                                    _calendar, dayCounter, businessDayConvention)

class BlackVarianceSurface(mx.core_BlackVarianceSurface):
    def __init__(self, refDate, periods, strikes, blackVols,
                   calendar=None,
                   dayCounter=mx.Actual365Fixed(), 
                   businessDayConvention=mx.ModifiedFollowing):
        if isinstance(refDate, mx.Date):
            _refDate = refDate
        else:
            _refDate = mx.Date(refDate)

        _periods = periods
        _calendar = calendar

        if _calendar is None:
            _calendar = mx.default_calendar()

        _blackVols = mx.Matrix(blackVols)

        mx.core_BlackVarianceSurface.__init__(self, _refDate, _periods, strikes, blackVols,
                                    _calendar, dayCounter, businessDayConvention)

