from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score

from tqdm import tqdm
from scipy import sparse

import pandas as pd
import numpy as np

# clf = DecisionTreeClassifier(random_state=0)
clf = RandomForestClassifier(
    random_state=44
)

# Loading our training data
test_data = pd.read_csv('TestData.csv', names=["Chord", "Chromagram"]).reset_index(drop=True)
train_data = pd.read_pickle('TrainingData.pkl').reset_index(drop=True)

Y = train_data.iloc[0:, 0]
X = train_data.iloc[0:, 1:]
print(X)
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
# train_x, train_y = [train_data["Chromagram"][:1], train_data["Chord"][:1]]

# test_x, test_y = [test_data["Chromagram"], test_data["Chord"]]
# x = np.array(train_x, dtype=object)
# print(train_data)
# tqdm(clf.fit(list(np.array(train_x, dtype=object)), list(np.array(train_y, dtype=object))))

# train_data = pd.read_pickle('test.obj')
# print(train_data[0])
# train_y = []
# train_x = []
# for row in train_data[1]:
#     train_y.append(row[0])
#     train_x.append(row[1])

print("Printing train y")
print(y_train)

print("Printing train x")
print(X_train)
clf.fit(X_train, y_train)
score = clf.score(X_test, y_test)
print(score)

import librosa

def get_chromagram(raw_audio_path):
    raw_audio_ts, sr = librosa.load(raw_audio_path)
    chromagram = np.array(librosa.feature.chroma_stft(y=raw_audio_ts, sr=sr, center=True), dtype=object)
    chromagram = np.mean(chromagram, axis=1)
    print(chromagram.shape)
    return chromagram

dillon_g_chord = get_chromagram('/Users/dillon/projects/chord-recognizer/Data/Experimental/Random_Bb_Chord.wav')
for pitch in dillon_g_chord:
    print(pitch)

chord_pitches = [pitch for pitch in dillon_g_chord]
print(dillon_g_chord)
# LINE BELOW DOES PREDICTION
pred = clf.predict(dillon_g_chord.reshape(1, -1))
print(f"PREDICTED CHORD: {pred}")
