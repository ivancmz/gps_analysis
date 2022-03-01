%matplotlib inline

import numpy
import pandas
import geopandas
import pysal
import seaborn
import contextily
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN

def longSign(s):
    if s=='S':
        return -1
    else:
        return 1

def latSign(s):
    if s=='W':
        return -1 
    else:
        return 1

db = pandas.read_csv('./tramas_export_1644257289215.csv')

db["long"] = (longSign(db["ns"])*db["longitude"])
db["lat"] =  (latSign(db["ew"])*db["latitude"])

db.info()

# Generate scatter plot
seaborn.jointplot(x='long', y='lat', data=db, s=0.5);

