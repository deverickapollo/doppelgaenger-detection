import random
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
    i = 1
    for user_id in user_ids:
        train_x, test_x, train_y, test_y = get_train_test_split(matrix, user_id)
        print("Training classifier for user " + str(user_id) + " (" + str(i) + "/" + str(len(user_ids)) + ")")
        classifiers[user_id] = train_classifier_svc(train_x, train_y)
        i += 1
    return classifiers


# get the training and testing data to train a classifier for a specific user
# last column of the feature matrix has to be the user id
# input: feature matrix, user id
# output: tuple (train_X, test_X, train_y, test_y)
def get_train_test_split(matrix, user_id):
    train = np.array([list for list in matrix if list[-1] != user_id])
    test = np.array([list for list in matrix if list[-1] == user_id])
    train_x, train_y = train[:, :-4], train[:, -1]
    test_x, test_y = test[:, :-4], test[:, -1]
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
        p = predict_probabilities_svc(models[line[-1]], [line[:-4]])
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

# Doppelgaenger detection
# compares every pair of comments by different users
#
# Input feature matrix
# Output list with tuples(final decision, user id A, comment id A, user id B, comment id B, is artificial doppelgaenger pair)
def dopplegeanger_detection(matrix, mode):
    matrix = np.real(matrix)
    models = get_classifiers(matrix)
    threshold = get_threshold(matrix,mode, models)
    # i=0
    # for m in matrix:
    #     print(str(i) + ": " + str(m))
    #     i+=1
    # print()
    # print("")
    results = []
    pairs_comment_ids_compared = []
    for row in matrix:
        j = 0
        for r in matrix:
            s = set()
            s.add(r[-2])
            s.add(row[-2])
            if (row[-1] != r[-1]) and (s not in pairs_comment_ids_compared):
                prob = predict_pairwise_probability_svc(models,[r, row])
                pairs_comment_ids_compared.append(s)
                decision = final_decision(prob, threshold, mode)
                is_doppel = is_doppel_pair(r, row)
                results.append([decision, r[-1], r[-2], row[-1], row[-2], prob, is_doppel, is_true_false_positive_negative(decision, is_doppel)])
    return results


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
# Output: feature matrix with split user accounts
def split_user_accounts(matrix):
    matrices = np.split(matrix, np.where(np.diff(matrix[:, -1]))[0] + 1)
    for m in matrices:
        np.random.shuffle(m)
        A = set()
        B = set()
        i=0
        for row in m:
            if i%2 == 1:
                row[-1] = float("9000" + str(row[-1]))
            else:
                row[-1] = float("8000" + str(row[-1]))
            i += 1
            # if row[-3] in A:
            #     row[-1] = float("9000" + str(row[-1]))
            # elif row[-3] in B:
            #     row[-1] = float("8000" + str(row[-1]))
            # else:
            #     k = random.randint(0, 1)
            #     if k == 0:
            #         row[-1] = float("9000" + str(row[-1]))
            #         A.add(row[-3])
            #     else:
            #         row[-1] = float("8000" + str(row[-1]))
            #         B.add(row[-3])
    return matrix


# get threshold
def get_threshold(matrix_split, mode, classifiers):
    # matrix_split = split_user_accounts(matrix)
    # classifiers = get_classifiers(matrix_split)
    d = dict(prob_doppel_pairs = [],
             prob_non_doppel_pairs = [])
    i = 0
    for row in matrix_split:
        j = 0
        for r in matrix_split:
            if row[-1] != r[-1]:
                prob = predict_pairwise_probability_svc(classifiers,[r, row])
                if is_doppel_pair(row, r):
                    d["prob_doppel_pairs"].append(prob[mode])
                else:
                    d["prob_non_doppel_pairs"].append(prob[mode])
            j += 1
        i += 1
    # TODO: compute an appropriate threshold for every mode (average, multiplication, squaredaverage)
    print("==================")
    print("Average Probability Doppelgaenger Pairs: " + str(np.average(d["prob_doppel_pairs"])))
    print("Average Probability Non Doppelgaenger Pairs: " + str(np.average(d["prob_non_doppel_pairs"])))
    print("==================")
    threshold = np.average(d["prob_doppel_pairs"])
    return threshold


# determine wether two given feature vectors are a artificially created doppelgaenger pair
def is_doppel_pair(vector1, vector2):
    if ((str(vector1[-1])[:4] == "8000") and (str(vector2[-1])[:4] == "9000")) or ((str(vector2[-1])[:4] == "8000") or (str(vector1[-1])[:4] == "9000")):
        if str(vector1[-1])[4:] == str(vector2[-1])[4:]:
            return True
        else:
            return False
    else:
        return False


# Task 2: Known Number of Doppelgaengers

# extract feature matrix for a number of comments for a number of users with a specified minimum text length
def get_matrix_experiment_one(matrix, users=60, comments=20, text_length=250):
    experiment_matrix = []
    d = dict.fromkeys(matrix[:,-1],0)
    u = set()
    temp = []
    prior = [matrix[0][-1]]
    for row in matrix:
        if len(u) >= users:
            break
        if d[row[-1]] < comments:
            if (row[-4] >= text_length) and (row[-1] == prior):
                temp.append(row)
                d[row[-1]] += 1
        if (prior != row[-1]) and (len(temp) == comments):
            u.add(prior)
            for r in temp:
                experiment_matrix.append(r)
            temp = []
        elif (prior != row[-1]) and (len(temp) != comments):
            temp = []
        prior = row[-1]
    return np.array(experiment_matrix)


# extract feature matrices with three disjoint sets of features
def get_matrix_experiment_two(matrix):
    matrix = get_matrix_experiment_one(matrix)
    user_ids = matrix[:,-1][:,None]
    comment_ids = matrix[:,-2][:,None]
    article_ids = matrix[:,-3][:,None]
    text_lengths = matrix[:,-4][:,None]
    matrices = np.array_split(matrix[:,:-4],3, axis=1)
    list = []
    for m in matrices:
        m = np.append(m, text_lengths, axis=1)
        m = np.append(m, article_ids, axis=1)
        m = np.append(m, comment_ids,axis=1)
        m = np.append(m, user_ids,axis=1)
        list.append(m)
    return list


# Task 3: Comparison with Baseline

# compute the euclidean distance between to vectors
def get_euclid(vector1, vector2):
    return np.linalg.norm(np.array(vector1)-np.array(vector2))


def final_decision_euclid(dist, threshold):
    if dist < threshold:
        return True
    else:
        return False


# Doppelgaenger detection for euclid unsupervised
# compares every pair of comments by different users
#
# Input feature matrix
# Output list with tuples(final decision, user id A, comment id A, user id B, comment id B, is artificial doppelgaenger pair)
def dopplegaenger_detection_euclid(matrix, threshold):
    results = []
    pairs_comment_ids_compared = []
    for row in matrix:
        for r in matrix:
            s = set()
            s.add(r[-2])
            s.add(row[-2])
            if (row[-1] != r[-1]) and (s not in pairs_comment_ids_compared):
                dist = get_euclid(r[:-4], row[:-4])
                pairs_comment_ids_compared.append(s)
                decision = final_decision_euclid(dist, threshold)
                is_doppel = is_doppel_pair(r, row)
                results.append([decision, r[-1], r[-2], row[-1], row[-2], dist, is_doppel, is_true_false_positive_negative(decision, is_doppel)])
    return results

def is_true_false_positive_negative(final_decision, is_doppel_pair):
    if (final_decision == True) and (is_doppel_pair == True):
        return "true_positive"
    elif (final_decision == True) and (is_doppel_pair == False):
        return "false_positive"
    elif (final_decision == False) and (is_doppel_pair == False):
        return "true_negative"
    elif (final_decision == False) and (is_doppel_pair == True):
        return "false_negative"


