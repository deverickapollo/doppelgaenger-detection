import numpy as np
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import brier_score_loss
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
def predict_probabilities_svc(model, feature_vector):
    predict_y = pd.DataFrame(model.predict_proba(feature_vector), columns=model.classes_)
    return predict_y


# predict the pairwise probability for two feature vectors in a matrix
# CAUTION: user_ids need to be different
# input: classifier models, feature matrix with two feature vectors
# output: pairwise probability dict(average, multiplication, squared_average)
def predict_pairwise_probability_svc(models, feature_vectors):
    predictions = []
    i=1
    for line in feature_vectors:
        p = predict_probabilities_svc(models[line[-1]], [line[:-1]])
        predictions.append(p.get(float(feature_vectors[i%2][-1]))[0])
        i += 1
    pairwise_prob = dict(average = np.average(predictions),
                         multiplication = np.prod(predictions),
                         squaredaverage = np.average(np.square(predictions)))
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


def final_decision(prob, threshold, mode):
    if prob[mode] > threshold:
        return True
    else:
        return False


def dopplegeanger_detection(matrix, threshold, mode):
    matrix = np.real(matrix)
    models = get_classifiers(matrix)
    print("The following rows are present in the feature matrix, each representing one comment. The last value of each row is the user id which identifies the author of the comment: ")
    print("Final decision based on threshold: " + str(threshold) + " and mode: " + mode +"\n")
    # i=0
    # for m in matrix:
    #     print(str(i) + ": " + str(m))
    #     i+=1
    # print()
    # print("")
    i=0
    for row in matrix:
        j = 0
        for r in matrix:
            if row[-1] != r[-1]:
                prob = predict_pairwise_probability_svc(models,[r, row])
                if final_decision(prob, float(threshold), mode) is True:
                    print("Pairwise probability for row " + str(i) + " [user id: " + str(row[-1]) + "] and row " + str(j) + " [user id: " + str(r[-1]) + "]")
                    print(prob)
                    print("--------------------------------------------------------\n")
            j +=1
        i += 1


# Part IV: Evaluation: Known number of Doppelgaengers
# Task 1: Automated Threshold Metric and Statistical Measures

# Brier Score:
#
# The Brier score measures the mean squared difference between the predicted probability and the actual outcome.
# The Brier score always takes on a value between zero and one, since this is the largest possible difference between
# a predicted probability (which must be between zero and one) and the actual outcome (which can take on values of
# only 0 and 1). It can be decomposed is the sum of refinement loss and calibration loss.
#
# Formula: (1/N) * sum_{t=1}^N((ft-ot)^2)
# N = the number of items you’re calculating a Brier score for.
# ft is the forecast probability (i.e. 25% chance),
# ot is the outcome (1 if it happened, 0 if it didn’t)
#
# Input: true targets (list), probabilities (list)
# Output: brier score
def brier_score(true_targets, probabilities):
    return brier_score_loss(true_targets, probabilities)


# Split user accounts artificially. Pads 9000 and 8000 before the original user ids.
#
# Input: feature matrix
# Output: dict with two chunked splits for every user present in the feature matrix
def split_user_accounts(matrix):
    d = dict()
    for row in matrix:
        if row[-1] in d:
            d[row[-1]].append(row)
        else:
            d[row[-1]] = [row]
    for key in d:
        d[key] = np.array_split(d[key], 2)
        for row in d[key][1]:
            row[-1] = float("9000" + str(row[-1]))
        for row in d[key][0]:
            row[-1] = float("8000" + str(row[-1]))
    return d
