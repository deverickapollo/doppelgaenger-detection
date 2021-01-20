import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import brier_score_loss
from sklearn.datasets import make_classification
from sklearn.model_selection import StratifiedKFold
from sklearn.svm import SVC
import seaborn as sns
import pickle
import pandas as pd

# create a PdfPages object
pdf = PdfPages('heatmaps.pdf')

############################
#### SVM Classification ####
############################

# Doppelgaenger detection
# compares every pair of comments by different users
#
# Input: feature matrix, mode
# Output: list with tuples(final decision, user id A, comment id A, user id B, comment id B, is artificial doppelgaenger pair, classification true/false positive/negative)
def dopplegeanger_detection(matrix, mode):
    models = get_classifiers(matrix[0])
    threshold = get_threshold(matrix[0],mode, models)
    results = []
    pairs_comment_ids_compared = []
    for row in matrix[1]:
        j = 0
        for r in matrix[1]:
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

# Determine threshold for doppelgaenger detection automatically
#
# Input: feature matrix, mode, classifiers
# Output: threshold
def get_threshold(matrix_split, mode, classifiers):
    d = dict(prob_doppel_pairs = [],
             prob_non_doppel_pairs = [])
    pairs_comment_ids_compared = []
    for row in matrix_split:
        for r in matrix_split:
            s = set()
            s.add(r[-2])
            s.add(row[-2])
            if (row[-1] != r[-1]) and (s not in pairs_comment_ids_compared):
                prob = predict_pairwise_probability_svc(classifiers,[r, row])
                pairs_comment_ids_compared.append(s)
                if is_doppel_pair(row, r):
                    d["prob_doppel_pairs"].append(prob[mode])
                else:
                    d["prob_non_doppel_pairs"].append(prob[mode])
    print("==================")
    print("Average Probability Doppelgaenger Pairs: " + str(np.average(d["prob_doppel_pairs"])))
    print("Average Probability Non Doppelgaenger Pairs: " + str(np.average(d["prob_non_doppel_pairs"])))
    print("==================")
    threshold = (np.average(d["prob_doppel_pairs"]) + np.average(d["prob_non_doppel_pairs"])) / 2
    return threshold

# predict probabilities for a feature vector
#
# input: classifier model, feature matrix
# output: probabilities for each class
def predict_probabilities_svc(model, feature_vector):
    predict_y = pd.DataFrame(model.predict_proba(feature_vector), columns=model.classes_)
    return predict_y


# predict the pairwise probability for two feature vectors in a matrix
# CAUTION: user_ids need to be different
#
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

def final_decision(prob, threshold, mode):
    if prob[mode] > threshold:
        return True
    else:
        return False


# model serialization
# input: false positive rate, true positive rate, color, and label
def plot_roc_curve(fpr, tpr, color, label):
    fig = plt.figure()
    plt.plot(fpr, tpr, color=color, label=label)
    plt.plot([0, 1], [0, 1], color='darkblue', linestyle='--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.legend()
    plt.savefig('ROC.png')

# Plot confusion matrix to a heatmap and save to file
# input: confusion matrix object and title 
def plot_heatmap(cm, title):
    #Plot the matrix
    # sns.heatmap(cm, annot=True, fmt = ".2%", cmap="Spectral")
    fig = plt.figure()
    ax = sns.heatmap(cm/np.sum(cm), annot=True, fmt = ".2%", cmap="Spectral")
    ax.set(title=title,
      xlabel="Actual",
      ylabel="Predicted",)
    ax.xaxis.set_ticklabels(['True', 'False'])
    ax.yaxis.set_ticklabels(['True', 'False']) 
    pdf.savefig(fig)


############################
###### SVM Training ########
############################

# close open file and figure
def closepdf():
    plt.close()
    pdf.close()

# get the classifiers for every user present in the feature matrix
# last column of the feature matrix has to be the user id
#
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
#
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

# model serialization

# input: model
# output: serialized model
def save_model(model):
    return pickle.dumps(model)

# model deserialization
#
# input: serialized model
# output: model
def load_model(s):
    return pickle.loads(s)



############################
######### EUCLID ###########
############################

# Doppelgaenger detection for euclid
# compares every pair of comments by different users
#
# Input: feature matrix, threshold
# Output: list with tuples(final decision, user id A, comment id A, user id B, comment id B, is artificial doppelgaenger pair, classification true/false positive/negative)
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

# compute optimal distance euclid
#
# Input: feature matrix
# Output: distance
def get_optimal_distance_euclid(matrix_split):
    d = dict(dist_doppel_pairs = [],
             dist_non_doppel_pairs = [])
    pairs_comment_ids_compared = []
    for row in matrix_split:
        for r in matrix_split:
            s = set()
            s.add(r[-2])
            s.add(row[-2])
            if (row[-1] != r[-1]) and (s not in pairs_comment_ids_compared):
                dist = get_euclid(r[:-4], row[:-4])
                pairs_comment_ids_compared.append(s)
                if is_doppel_pair(row, r):
                    d["dist_doppel_pairs"].append(dist)
                else:
                    d["dist_non_doppel_pairs"].append(dist)
    print("==================")
    print("Average Distance Doppelgaenger Pairs: " + str(np.average(d["dist_doppel_pairs"])))
    print("Average Distance Non Doppelgaenger Pairs: " + str(np.average(d["dist_non_doppel_pairs"])))
    print("==================")
    threshold = (np.average(d["dist_doppel_pairs"]) + np.average(d["dist_non_doppel_pairs"])) / 2
    return threshold

# Compute the euclidean distance between to vectors
#
# Input: vector1, vector2
# Output: euclidean distance
def get_euclid(vector1, vector2):
    return np.linalg.norm(np.array(vector1)-np.array(vector2))

# make final decision for euclid based on threshold
#
# Input: dist, threshold
# Output: final decision
def final_decision_euclid(dist, threshold):
    if dist < threshold:
        return True
    else:
        return False



############################
######### HELPERS ##########
############################

# classify final decision as true/false positive/negative
#
# Input: final decision, is doppel pair
# Output: true/false positive/negative
def is_true_false_positive_negative(final_decision, is_doppel_pair):
    if (final_decision == True) and (is_doppel_pair == True):
        return "true_positive"
    elif (final_decision == True) and (is_doppel_pair == False):
        return "false_positive"
    elif (final_decision == False) and (is_doppel_pair == False):
        return "true_negative"
    elif (final_decision == False) and (is_doppel_pair == True):
        return "false_negative"

# Get numbers and rates of true/false positive/negatives for one experiment
#
# Input: experiment results
# Output: numbers + rates true/false positives/negatives
def get_number_true_false_positive_negative(results):
    d = dict.fromkeys(["true_positive", "false_positive", "true_negative", "false_negative"], 0)
    for row in results:
        d[row[-1]] += 1
    d["true_positive_rate"] = d["true_positive"] / (d["true_positive"] + d["false_negative"])
    d["false_positive_rate"] = d["false_positive"] / (d["false_positive"] + d["true_negative"])
    d["true_negative_rate"] = d["true_negative"] / (d["true_negative"] + d["false_negative"])
    d["false_negative_rate"] = d["false_negative"] / (d["false_negative"] + d["true_positive"])
    return d

# Apply k fold cross validation and return k train / test matrices
#
# Input: feauture matrix, k
# Output: k train / test matrices
def k_fold_cross_validation(matrix, k):
    kfold = StratifiedKFold(n_splits=k, shuffle=True, random_state=1)
    r = []
    for train_ix, test_ix in kfold.split(matrix, matrix[:,-1]):
        train, test = matrix[train_ix], matrix[test_ix]
        r.append([train, test])
    return r

# determine wether two given feature vectors are a artificially created doppelgaenger pair
#
# Input: vector1, vector2
# Output: final decision
def is_doppel_pair(vector1, vector2):
    if ((str(vector1[-1])[:4] == "8000") and (str(vector2[-1])[:4] == "9000")) or ((str(vector2[-1])[:4] == "8000") or (str(vector1[-1])[:4] == "9000")):
        if str(vector1[-1])[4:] == str(vector2[-1])[4:]:
            return True
        else:
            return False
    else:
        return False

# extract feature matrix for a number of comments for a number of users with a specified minimum text length
#
# Input: feature matrix, number users, number comments, text length
# Output: experiment matrix
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
#
# Input: feauture matrix
# Output: three experiment feature martices
def get_matrix_experiment_two(matrix):
    matrix = get_matrix_experiment_one(matrix, users=60)
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



############################
######### PLOT #############
############################

# plot roc curve
#
# input: fpr, tpr, color, label
# output: /
def plot_roc_curve(fpr, tpr, color, label):
    fig = plt.figure()
    plt.plot(fpr, tpr, color=color, label=label)
    plt.plot([0, 1], [0, 1], color='darkblue', linestyle='--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.legend()
    plt.savefig('ROC.png')

# plot heatmap
#
# input: confusion matrix
# output: /
def plot_heatmap(cm, title):
    #Plot the matrix
    # sns.heatmap(cm, annot=True, fmt = ".2%", cmap="Spectral")
    fig = plt.figure()
    ax = sns.heatmap(cm/np.sum(cm), annot=True, fmt = ".2%", cmap="Spectral")
    ax.set(title=title,
      xlabel="Actual",
      ylabel="Predicted",)
    pdf.savefig(fig)

# close pdf
def closepdf():
    plt.close()
    pdf.close()

