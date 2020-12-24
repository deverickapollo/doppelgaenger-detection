import numpy as np
from sklearn.calibration import CalibratedClassifierCV
from sklearn.svm import SVC
import pickle
import pandas as pd


# get the classifiers for every user present in the feature matrix
# last column of the feature matrix has to be the user id
# input: feature matrix
# output: dict(userid : classifier)
def get_classifiers(matrix):
    user_ids = set()
    classifiers = dict()
    for list in matrix:
        user_ids.add(list[-1])
    for user_id in user_ids:
        train_x, test_x, train_y, test_y = get_train_test_split(matrix, user_id)
        classifiers[user_id] = train_classifier_svc(train_x, train_y)
    return classifiers


# get the training and testing data to train a classifier for a specific user
# last column of the feature matrix has to be the user id
# input: feature matrix, user id
# output: tuple (train_X, test_X, train_y, test_y)
def get_train_test_split(matrix, user_id):
    train = np.array([list for list in matrix if list[-1] != user_id])
    test = np.array([list for list in matrix if list[-1] == user_id])
    train_x, train_y = train[:, :-1], train[:, -1]
    test_x, test_y = test[:, :-1], test[:, -1]
    return (train_x, test_x, train_y, test_y)


# train and calibrate a support vector classifier (svc)
def train_classifier_svc(train_x, train_y):
    model = SVC()
    calibrated_model = CalibratedClassifierCV(model, method='sigmoid', cv=5)
    calibrated_model.fit(train_x, train_y)
    return calibrated_model


# predict probabilities for a feature vector
# input: classifier model, feature matrix
# output: probabilities for each class
def predict_probabilities_svc(model, feature_matrix):
    predict_y = pd.DataFrame(model.predict_proba(feature_matrix), columns=model.classes_)
    return predict_y


# predict the pairwise probability for two feature vectors in a matrix
# input: classifier models, feature matrix with two feature vectors
# output: pairwise probability dict(average, multiplication, squared_average)
def predict_pairwise_probability_svc(models, feature_matrix):
    predictions = []
    i=1
    for line in feature_matrix:
        p = predict_probabilities_svc(models[line[-1]], [line[:-1]])
        predictions.append(p.get(feature_matrix[i%2][-1])[0])
        i += 1
    print(predictions)
    pairwise_prob = dict(average = np.average(predictions),
                         multiplication = np.prod(predictions),
                         squared_average = np.average(np.square(predictions)))
    return pairwise_prob


# model serialization
# innput: model
# output: serialized model
def save_model(model):
    return pickle.dumps(model)


# model deserialization
# input: serialized model
# output: model
def load_model(s):
    return pickle.loads(s)