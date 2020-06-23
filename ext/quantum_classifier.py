import os
import numpy as np
from sklearn.cluster import KMeans
import pandas as pd

__PATH__ = os.path.realpath("")


def buildUp(args):
	end = ""
	for i in range(len(args)):
		if (args[i] == args[-1]):
			end += str(args[i])
		else:
			end += str(args[i]) + ","
	return end

def all_numeric_cluster(req, data):
    if (data.shape[0] == 0):
        return []
    # elif (data.shape[0] < 3):
    #     mod = KMeans( n_clusters = data.shape[0] )
    # else:
    #     mod = KMeans( n_clusters = 3 )
    keys = data.pop("uid")
    if ('Volume' in req):
        req.pop("Volume")
    print( data )
    print("\n\n\n", req)
    heads = ['Open', 'High', 'Low', 'Close', 'Dividends', 'Splits']
    return data[ data[heads] >= req[heads] ]
    # mod.fit( data )
    # preds = mod.predict(data)
    # real = mod.predict(req)
    # return np.array([keys[i] for i in range(len(preds)) if preds[i] in real[-1:]])
