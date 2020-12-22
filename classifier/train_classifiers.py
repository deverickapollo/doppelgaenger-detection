import numpy as np


# get the training and testing data to train a classifier for a specific user
# input: feature matrix, user id
# output: tuple (train_X, test_X, train_y, test_y)
def get_train_test_split(matrix, user_id):
    train = np.array([list for list in matrix if list[-1] != user_id])
    test = np.array([list for list in matrix if list[-1] == user_id])
    train_x, train_y = train[:, :-1], train[:, -1]
    test_x, test_y = test[:, :-1], test[:, -1]
    return (train_x, test_x, train_y, test_y)