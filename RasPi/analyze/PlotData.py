import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('/home/kawashima/Data/SDCard/1MinSD.csv', index_col=0, skiprows=2, names=["millis", "temperature", "humidity", "pressure", "voltage"])

