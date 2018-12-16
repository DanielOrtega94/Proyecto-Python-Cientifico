import numpy as np
import pandas as pd

archivo =  pd.read_csv("cmtcmt.csv",low_memory=False)
print(archivo.shape)
