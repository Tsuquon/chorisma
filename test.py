from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score

from tqdm import tqdm
from scipy import sparse

import pandas as pd
import numpy as np

train_data = pd.read_pickle('TrainingData.pkl').reset_index(drop=True)
print(train_data.iloc[0:, 1:])

import librosa

