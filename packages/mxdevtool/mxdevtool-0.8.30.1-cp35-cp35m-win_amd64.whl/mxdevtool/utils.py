import os
import mxdevtool as mx
import numpy as np
from datetime import datetime
import tempfile

def npzee_view(arg):
    if isinstance(arg, np.ndarray):
        tempfilename = os.path.join(tempfile.gettempdir(), 'temp_' + datetime.utcnow().strftime('%Y%m%d%H%M%S%f') + '.npz')
        np.savez(tempfilename, data=arg)
        os.startfile(tempfilename)
    elif isinstance(arg, str):
        if os.path.exists(arg):
            os.startfile(arg)
        else:
            raise Exception('file does not exist')
    elif isinstance(arg, mx.core_ScenarioResult):
        if os.path.exists(arg.filename):
            os.startfile(arg.filename)
        else:
            raise Exception('file does not exist')
    else:
        print('unknown')


def yield_curve_view(yieldcurve):
    pass

