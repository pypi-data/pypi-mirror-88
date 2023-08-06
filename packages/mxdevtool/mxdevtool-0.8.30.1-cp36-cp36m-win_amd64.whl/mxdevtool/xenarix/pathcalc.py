import mxdevtool as mx
import numpy as np


class DeterministicParameter(mx.core_DeterministicParameter):
    def __init__(self, times, values):
        mx.core_DeterministicParameter.__init__(self, times, values)

# models ----------------------------

class GBMConst(mx.core_GBMConstModel):
    def __init__(self, name, x0, rf, div, vol):
        mx.core_GBMConstModel.__init__(self, name, x0, rf, div, vol)

class GBM(mx.core_GBMModel):
    def __init__(self, name, x0, rfCurve, divCurve, volTs):
        mx.core_GBMModel.__init__(self, name, x0, rfCurve, divCurve, volTs)

class Heston(mx.core_HestonModel):
    def __init__(self, name, x0, rfCurve, divCurve, v0, volRevertingSpeed, longTermVol, volOfVol, rho):
        mx.core_HestonModel.__init__(self, name, x0, rfCurve, divCurve, v0, volRevertingSpeed, longTermVol, volOfVol, rho)

class CIR1F(mx.core_CIR1FModel):
    def __init__(self, name, r0, alpha, longterm, sigma):
        mx.core_CIR1FModel.__init__(self, name, r0, alpha, longterm, sigma)

class Vasicek1F(mx.core_Vasicek1FModel):
    def __init__(self, name, r0, alpha, longterm, sigma):
        mx.core_Vasicek1FModel.__init__(self, name, r0, alpha, longterm, sigma)

class HullWhite1F(mx.core_HullWhite1FModel):
    def __init__(self, name, fittingCurve, alphaPara, sigmaPara):
        mx.core_HullWhite1FModel.__init__(self, name, fittingCurve, alphaPara, sigmaPara)
    
    # def calibrate(self, volMatrix, expiries, tenors, vols_using=None, familyname='default', tool='swaption'):
    #     mx.core_HullWhite1FModel.calibrate(self, volMatrix, expiries, tenors, vols_using, familyname)

class BK1F(mx.core_BK1FModel):
    def __init__(self, name, fittingCurve, alphaPara, sigmaPara):
        mx.core_BK1FModel.__init__(self, name, fittingCurve, alphaPara, sigmaPara)

class G2Ext(mx.core_GTwoExtModel):
    def __init__(self, name, fittingCurve, alpha1, sigma1, alpha2, sigma2, corr):
        mx.core_GTwoExtModel.__init__(self, name, fittingCurve, alpha1, sigma1, alpha2, sigma2, corr)


# calcs -----------------------------

class YieldCurve(mx.core_YieldCurveValueCalc):
    def __init__(self, name, yc, output_type='spot', compound=mx.Compounded):
        mx.core_YieldCurveValueCalc.__init__(self, name, yc, output_type, compound)


class FixedRateBond(mx.core_FixedRateCMBondPositionCalc):
    def __init__(self, name, ir_pc, 
                 notional=10000, 
                 fixedrate=0.0, 
                 coupon_tenor=mx.Period(3, mx.Months), 
                 maturity_tenor=mx.Period(3, mx.Years), 
                 discount=None):
        if discount is None:
            raise Exception('discount curve is required')

        mx.core_FixedRateCMBondPositionCalc.__init__(self, name, ir_pc, notional, fixedrate, coupon_tenor, maturity_tenor, discount)

    def returns(self, typeStr):
        return mx.core_ReturnWrapperCalc(self.name + '_' + typeStr, self, typeStr)

class Returns(mx.core_ReturnWrapperCalc):
    def __init__(self, name, pc, return_type='returns'):
        mx.core_ReturnWrapperCalc.__init__(self, name, pc, return_type)

class Shift(mx.core_ShiftWrapperCalc):
    def __init__(self, name, pc, shift, fill_value=0.0):
        mx.core_ShiftWrapperCalc.__init__(self, name, pc, shift, fill_value)

class ConstantValue(mx.core_ConstantValueCalc):
    def __init__(self, name, v):
        mx.core_ConstantValueCalc.__init__(self, name, v)
        
class ConstantArray(mx.core_ConstantArrayCalc):
    def __init__(self, name, arr):
        mx.core_ConstantArrayCalc.__init__(self, name, arr)
        
class LinearOper(mx.core_LinearOperWrapperCalc):
    def __init__(self, name, pc, multiple=1.0, spread=0.0):
        mx.core_LinearOperWrapperCalc.__init__(self, name, pc, multiple, spread)

class UnaryFunction(mx.core_UnaryFunctionWrapperCalc):
    def __init__(self, name, pc, func_type):
        mx.core_UnaryFunctionWrapperCalc.__init__(self, name, pc, func_type)

class BinaryFunction(mx.core_BinaryFunctionWrapperCalc):
    def __init__(self, name, pc1, pc2, func_type):
        mx.core_BinaryFunctionWrapperCalc.__init__(self, name, pc1, pc2, func_type)

class MultaryFunction(mx.core_MultaryFunctionWrapperCalc):
    def __init__(self, name, pc_list, func_type):
        mx.core_MultaryFunctionWrapperCalc.__init__(self, name, pc_list, func_type)

class Fund(mx.core_FundWrapperCalc):
    def __init__(self, name, weights, pc_list):
        mx.core_FundWrapperCalc.__init__(self, name, weights, pc_list)


# math functions ---------------------

def min(models, name=None):
    if name is None:
        name = '_'.join([m.name() for m in models]) + 'min'
    return mx.core_MultaryFunctionWrapperCalc(name, models, 'min')


def max(models, name=None):
    if name is None:
        name = '_'.join([m.name() for m in models]) + 'max'
    return mx.core_MultaryFunctionWrapperCalc(name, models, 'max')


