import numpy as np
import pandas as pd

def numpy_to_python(obj):
    """Convierte tipos de NumPy a tipos nativos de Python para serialización JSON"""
    if isinstance(obj, (np.integer)):
        return int(obj)
    elif isinstance(obj, (np.floating)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, pd.Series):
        return obj.to_dict()
    else:
        return obj
