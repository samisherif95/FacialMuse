import librosa
import os
import numpy as np
import pandas as pd
from os import listdir
from os.path import isfile, join

cwd = os.getcwd()
files = os.listdir(cwd)  # Get all the files in that directory
print("Files in '%s': %s" % (cwd, files))

linenum = 1
feature_set = pd.DataFrame()

songname_vector = pd.Series()
tempo_vector = pd.Series()
total_beats = pd.Series()
chroma_stft_std = pd.Series()
chroma_cq_std = pd.Series()
chroma_cens_std = pd.Series()
mel_std = pd.Series()
mfcc_std = pd.Series()
mfcc_delta_std = pd.Series()
rmse_std = pd.Series()
cent_std = pd.Series()
spec_bw_std = pd.Series()
contrast_std = pd.Series()
rolloff_std = pd.Series()
poly_std = pd.Series()
tonnetz_std = pd.Series()
zcr_std = pd.Series()
harm_std = pd.Series()
perc_std = pd.Series()
frame_std = pd.Series()
path = 'SadTrain/'

file_data = [f for f in listdir(path) if isfile(join(path, f))]
for line in file_data:
    songname = path + line

    y, sr = librosa.load(songname, duration=90)
    S = np.abs(librosa.stft(y))
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
    chroma_cq = librosa.feature.chroma_cqt(y=y, sr=sr)
    chroma_cens = librosa.feature.chroma_cens(y=y, sr=sr)
    melspectrogram = librosa.feature.melspectrogram(y=y, sr=sr)
    rmse = librosa.feature.rmse(y=y)
    cent = librosa.feature.spectral_centroid(y=y, sr=sr)
    spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
    contrast = librosa.feature.spectral_contrast(S=S, sr=sr)
    rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
    poly_features = librosa.feature.poly_features(S=S, sr=sr)
    tonnetz = librosa.feature.tonnetz(y=y, sr=sr)
    zcr = librosa.feature.zero_crossing_rate(y)
    harmonic = librosa.effects.harmonic(y)
    percussive = librosa.effects.percussive(y)

    mfcc = librosa.feature.mfcc(y=y, sr=sr)
    mfcc_delta = librosa.feature.delta(mfcc)

    onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
    frames_to_time = librosa.frames_to_time(onset_frames[:20], sr=sr)

    songname_vector.at[linenum] = line
    tempo_vector.at[linenum] = tempo
    total_beats.at[linenum] = sum(beats)
    chroma_stft_std.at[linenum] = np.std(chroma_stft)
    chroma_cq_std.at[linenum] = np.std(chroma_cq)
    chroma_cens_std.at[linenum] = np.std(chroma_cens)
    mel_std.at[linenum] = np.std(melspectrogram)
    mfcc_std.at[linenum] = np.std(mfcc)
    mfcc_delta_std.at[linenum] = np.std(mfcc_delta)
    rmse_std.at[linenum] = np.std(rmse)
    cent_std.at[linenum] = np.std(cent)
    spec_bw_std.at[linenum] = np.std(spec_bw)
    contrast_std.at[linenum] = np.std(contrast)
    rolloff_std.at[linenum] = np.std(rolloff)
    poly_std.at[linenum] = np.std(poly_features)
    tonnetz_std.at[linenum] = np.std(tonnetz)
    zcr_std.at[linenum] = np.std(zcr)
    harm_std.at[linenum] = np.std(harmonic)
    perc_std.at[linenum] = np.std(percussive)
    frame_std.at[linenum] = np.std(frames_to_time)

    print(songname)
    linenum = linenum + 1

feature_set['song_name'] = songname_vector  # song name
feature_set['tempo'] = tempo_vector  # tempo
feature_set['total_beats'] = total_beats  # beats
feature_set['chroma_stft_std'] = chroma_stft_std
feature_set['chroma_cq_std'] = chroma_cq_std
feature_set['chroma_cens_std'] = chroma_cens_std
feature_set['melspectrogram_std'] = mel_std
feature_set['mfcc_std'] = mfcc_std
feature_set['mfcc_delta_std'] = mfcc_delta_std
feature_set['rmse_std'] = rmse_std
feature_set['cent_std'] = cent_std
feature_set['spec_bw_std'] = spec_bw_std
feature_set['contrast_std'] = contrast_std
feature_set['rolloff_std'] = rolloff_std
feature_set['poly_std'] = poly_std
feature_set['tonnetz_std'] = tonnetz_std
feature_set['zcr_std'] = zcr_std
feature_set['harm_std'] = harm_std
feature_set['perc_std'] = perc_std
feature_set['frame_std'] = frame_std

feature_set.to_csv('Sad_Music_Features.csv')

