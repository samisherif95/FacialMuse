import librosa
import os
import shutil
import numpy as np
import pandas as pd
from os import listdir
from os.path import isfile, join
from Classification import modelSVM

SongName_Array = []

# path going to this function should be the path of the users playlist
def getUserSongFeatures(path):
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

    file_data = [f for f in listdir(path) if isfile(join(path, f))]
    for line in file_data:
        songname = path + line
        SongName_Array.append(
            line)  # saving all song names in an array to be able to identify the predicition of each song
        y, sr = librosa.load(songname, duration=5)
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
    feature_set['chroma_stft_mean'] = chroma_stft_std
    feature_set['chroma_cq_mean'] = chroma_cq_std
    feature_set['chroma_cens_mean'] = chroma_cens_std
    feature_set['melspectrogram_mean'] = mel_std
    feature_set['mfcc_mean'] = mfcc_std
    feature_set['mfcc_delta_mean'] = mfcc_delta_std
    feature_set['rmse_mean'] = rmse_std
    feature_set['cent_mean'] = cent_std
    feature_set['spec_bw_mean'] = spec_bw_std
    feature_set['contrast_mean'] = contrast_std
    feature_set['rolloff_mean'] = rolloff_std
    feature_set['poly_mean'] = poly_std
    feature_set['tonnetz_mean'] = tonnetz_std
    feature_set['zcr_mean'] = zcr_std
    feature_set['harm_mean'] = harm_std
    feature_set['perc_mean'] = perc_std
    feature_set['frame_mean'] = frame_std

    feature_set.to_csv('User_Music_Features.csv')



# checks mood files if available, if not then should create files for each mood
def Createfiles():
    if not os.path.exists('Happy'):
        os.makedirs('Happy')
    if not os.path.exists('Sad'):
        os.makedirs('Sad')
    if not os.path.exists('Calm'):
        os.makedirs('Calm')
    if not os.path.exists('Angry'):
        os.makedirs('Angry')
# gets the CSV file for user and normalizes data and predicts the mood and then uses mood to move songs to correct
# folders, Next step should be to get mood from user and play music depending on mood detected
def PredictMood_MoveSongs(path):
    music_data = pd.read_csv('User_Music_Features.csv')
    first_column = music_data.columns[0]
    music_data.drop([first_column], inplace=True, axis=1)
    music_data.drop(['song_name'], inplace=True, axis=1)
    # music_data['Mood'].replace(['Happy', 'Sad', 'Calm', 'Angry'], [0, 1, 2, 3], inplace=True)
    #print('-------------------------------------------------------------------------')
    normalized_data = music_data.apply(lambda x: (x - np.min(x)) / (np.max(x) - np.min(x)))
    #print(music_data.head(5))
    #print(normalized_data.head(5))
    X = normalized_data[
        ['tempo', 'total_beats', 'chroma_stft_mean', 'chroma_cq_mean', 'chroma_cens_mean', 'melspectrogram_mean',
         'mfcc_mean', 'mfcc_delta_mean', 'rmse_mean', 'cent_mean', 'spec_bw_mean', 'contrast_mean', 'rolloff_mean',
         'poly_mean', 'tonnetz_mean', 'zcr_mean', 'harm_mean', 'perc_mean', 'frame_mean']].values
    # y = music_data['Mood'].values
    Predictions = modelSVM.predict(normalized_data)
    #print('-------------------------------------------------------------------------')
    #print(Predictions)
    iterator = 0
    # for loop that loops over song names in array and finds the songs path and moves them to the correct folder
    for song in SongName_Array:

        SRCpath = path + song

        if Predictions[iterator] == 0:
            newDest = 'Happy/' + song
            newSRC = SRCpath.replace(path, newDest)
            shutil.move(SRCpath, newSRC)
        if Predictions[iterator] == 1:
            newDest = 'Sad/' + song
            newSRC = SRCpath.replace(path, newDest)
            shutil.move(SRCpath, newSRC)
        if Predictions[iterator] == 2:
            newDest = 'Calm/' + song
            newSRC = SRCpath.replace(path, newDest)
            shutil.move(SRCpath, newSRC)
        if Predictions[iterator] == 3:
            newDest = 'Angry/' + song
            newSRC = SRCpath.replace(path, newDest)
            shutil.move(SRCpath, newSRC)
        iterator += 1
