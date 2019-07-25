import sys
sys.path.append("E:/")

import pandas as pd
import numpy as np
import os
import common_utils as utils
from sklearn import preprocessing, neighbors, svm, linear_model, ensemble, pipeline, model_selection
import classification_utils as cutils
import kernel_utils as kutils
from sklearn.externals import joblib

dir = 'E:/'
titanic_train = pd.read_csv(os.path.join(dir, 'train.csv'))

print(titanic_train.shape)
print(titanic_train.info())

titanic_train1 = utils.drop_features(titanic_train, ['PassengerId', 'Name', 'Survived', 'Ticket', 'Cabin'])

#type casting
utils.cast_to_cat(titanic_train1, ['Sex', 'Pclass', 'Embarked'])

cat_features = utils.get_categorical_features(titanic_train1)
print(cat_features)
cont_features = utils.get_continuous_features(titanic_train1)
print(cont_features)

#handle missing data(imputation)
cat_imputers = utils.get_categorical_imputers(titanic_train1, cat_features)
titanic_train1[cat_features] = cat_imputers.transform(titanic_train1[cat_features])
cont_imputers = utils.get_continuous_imputers(titanic_train1, cont_features)
titanic_train1[cont_features] = cont_imputers.transform(titanic_train1[cont_features])

#one hot encoding
titanic_train2 = utils.ohe(titanic_train1, cat_features)
scaler = preprocessing.StandardScaler()
X_train = scaler.fit_transform(titanic_train2)
y_train = titanic_train['Survived']

kernel_svm_estimator = svm.SVC(kernel='rbf')
kernel_svm_grid = {'gamma':[0.001, 0.01, 0.1, 1], 'C':[0.001, 0.01, 1, 10, 100] }
svm_final_estimator = cutils.grid_search_best_model(kernel_svm_estimator, kernel_svm_grid, X_train, y_train)

objects_to_dump = {
        'cat_imputers': cat_imputers,
        'cont_imputers': cont_imputers,
        'scaler': scaler,
        'estimator': svm_final_estimator
        }
joblib.dump(objects_to_dump, os.path.join(dir, 'titanic_model_1.pkl'))