import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

music_data = pd.read_csv('Music_Features.csv')
music_data.drop(['song_name'], inplace=True, axis=1)
music_data['Mood'].replace(['Happy', 'Sad', 'Calm'], [0, 1, 2], inplace=True)
# print('-------------------------------------------------------------------------')
normalized_data = music_data.apply(lambda x: (x - np.min(x)) / (np.max(x) - np.min(x)))

X = normalized_data[
    ['tempo', 'total_beats', 'chroma_stft_std', 'chroma_cq_std', 'chroma_cens_std', 'melspectrogram_std',
     'mfcc_std', 'mfcc_delta_std', 'rmse_std', 'cent_std', 'spec_bw_std', 'contrast_std', 'rolloff_std',
     'poly_std', 'tonnetz_std', 'zcr_std', 'harm_std', 'perc_std', 'frame_std']].values
y = music_data['Mood'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# Logistic Reg
modelLOG = LogisticRegression(solver='lbfgs', multi_class='multinomial')
modelLOG.fit(X_train, y_train.ravel())

# KNN
modelKNN = KNeighborsClassifier(n_neighbors=7)
modelKNN.fit(X_train, y_train)

# SVC
modelSVM = SVC(kernel='linear', C=1)
modelSVM.fit(X_train, y_train)

# Logistic Reg
y_predLOG = modelLOG.predict(X_test)
cmLOG = confusion_matrix(y_test, y_predLOG)
#print("cm of LOG")
#print(cmLOG)
#print("Accuracy LOGISTIC", (cmLOG[0][0] + cmLOG[1][1]) / cmLOG.sum() * 100)
#print('-------------------------------------------------------------------------')

# KNN
accuracyKNN = modelKNN.score(X_test, y_test)
knn_predictions = modelKNN.predict(X_test)
cmKNN = confusion_matrix(y_test, knn_predictions)
#print("cm of KNN")
#print(cmKNN)
#print("Accuracy of KNN", accuracyKNN * 100)
#print('-------------------------------------------------------------------------')

# svm
svm_predictions = modelSVM.predict(X_test)
accuracySVM = modelSVM.score(X_test, y_test)
cmSVM = confusion_matrix(y_test, svm_predictions)
#print("cm of svm")
#print(cmSVM)
#print("Accuracy SVM", accuracySVM * 100)
