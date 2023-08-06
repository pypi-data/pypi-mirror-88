import mxdevtool as mx


class FlatForward(mx.core_FlatForward):
    def __init__(self, refDate, forward, 
                   dayCounter=mx.Actual365Fixed(), 
                   compounding=mx.Compounded,
                   frequency = mx.Annual):
        if isinstance(refDate, mx.Date):
            _refDate = refDate
        else:
            _refDate = mx.Date(refDate)

        mx.core_FlatForward.__init__(self, _refDate, forward, dayCounter, compounding, frequency)


class ZeroYieldCurve(mx.core_ZeroYieldCurveExt):
    def __init__(self, refDate, periods, zeroRates, 
                   interpolationType=mx.Interpolator1D.Linear, 
                   extrapolationType=mx.Extrapolator1D.FlatForward, 
                   calendar=None,
                   dayCounter=mx.Actual365Fixed(), 
                   businessDayConvention=mx.ModifiedFollowing,
                   compounding=mx.Compounded):
        if isinstance(refDate, mx.Date):
            _refDate = refDate
        else:
            _refDate = mx.Date(refDate)

        _periods = periods
        _calendar = calendar

        if _calendar is None:
            _calendar = mx.default_calendar()

        mx.core_ZeroYieldCurveExt.__init__(self, _refDate, _periods, zeroRates, interpolationType, extrapolationType,
                                    _calendar, dayCounter, businessDayConvention, compounding)



# familyname : irskrw_krccp only now
class BootstapSwapCurveCCP(mx.core_BootstapSwapCurveCCP):
    def __init__(self, refDate, tenors_str, rateTypes, quotes, 
                interpolationType=mx.Interpolator1D.Linear, 
                extrapolationType=mx.Extrapolator1D.FlatForward, 
                familyname='irskrw_krccp',
                forSettlement=True):

        if isinstance(refDate, mx.Date):
            _refDate = refDate
        else:
            _refDate = mx.Date(refDate)

        if extrapolationType == mx.Extrapolator1D.SmithWilson:
            extrapolation = mx.SmithWilsonExtrapolation(0.1, 0.042)
        elif extrapolationType == mx.Extrapolator1D.FlatSpot:
            extrapolation = mx.FlatExtrapolation('spot')
        else:
            extrapolation = mx.FlatExtrapolation('forward')

        mx.core_BootstapSwapCurveCCP.__init__(self, _refDate, tenors_str, rateTypes, quotes, 
                                            interpolationType, extrapolation,
                                            familyname, forSettlement)


class ZeroSpreadedCurve(mx.core_ZeroSpreadedTermStructure):
    def __init__(self, curve, spread, compounding=mx.Continuous, frequency=mx.Annual):
        mx.core_ZeroSpreadedTermStructure.__init__(self, curve, spread, compounding, frequency)


class ForwardSpreadedCurve(mx.core_ForwardSpreadedTermStructure):
    def __init__(self, curve, spread):
        mx.core_ForwardSpreadedTermStructure.__init__(self, curve, spread)
