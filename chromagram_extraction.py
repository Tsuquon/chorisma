from tqdm import tqdm

import pandas as pd
import librosa
import numpy as np

import os
import pickle

TRAINING_PATH = "/Users/dillon/projects/chord-recognizer/Data/Training"
TEST_PATH = "/Users/dillon/projects/chord-recognizer/Data/Test"

# Getting chromagram
def get_chromagram(raw_audio_path):
    raw_audio_ts, sr = librosa.load(raw_audio_path)
    chromagram = np.array(librosa.feature.chroma_stft(y=raw_audio_ts, sr=sr, center=True), dtype=object)
    chromagram = np.mean(chromagram, axis=1)
    print(chromagram.shape)
    return chromagram

# Returns a 2-element list with the label and chromagram
def extract_feature(chord_type, raw_audio_path):
    pass

def get_chord_from_subdir(subdir):
    subdir_components = subdir.split("/")

    return subdir_components[-1]

if __name__ == '__main__':
    print("--- FEATURE EXTRACTION INITIAL TRAINING DATA ---")

    # chromagram_to_chord_data = []

    # # Loop through chord directories
    # for subdir, dirs, files in tqdm(os.walk(TEST_PATH)):
    #     chord_name = get_chord_from_subdir(subdir)
    #     for file in files:
    #         raw_audio_path = os.path.join(subdir, file)
    #         chromagram = get_chromagram(raw_audio_path)
    #         feature_data = [chord_name, chromagram] 
    #         chromagram_to_chord_data.append(feature_data)

    # chromagram_to_chord_df = pd.DataFrame(data=chromagram_to_chord_data, columns=['Chord', 'Chromagram'])
    # chromagram_to_chord_df.to_csv('TestData.csv')
    # chromagram_to_chord_df.to_pickle('TestData.pkl')

    chromagram_to_chord_data = []

    # Loop through chord directories
    for subdir, dirs, files in tqdm(os.walk(TRAINING_PATH)):
        chord_name = get_chord_from_subdir(subdir)
        for file in files:
            raw_audio_path = os.path.join(subdir, file)
            chromagram = get_chromagram(raw_audio_path)
            # chromagram_reshaped = np.reshape(-1, len(chromagram))
            # print(chromagram_reshaped)
            feature_data = [chord_name] 
            for pitch in chromagram:
                feature_data.append(pitch)
            chromagram_to_chord_data.append(feature_data)

    chromagram_to_chord_df = pd.DataFrame(data=chromagram_to_chord_data)
    print(chromagram_to_chord_df.head(n=6))
    chromagram_to_chord_df.to_csv('TrainingData.csv')
    chromagram_to_chord_df.to_pickle('TrainingData.pkl')
    filehandler = open(b"test.obj","wb")
    pickle.dump(chromagram_to_chord_data, filehandler)