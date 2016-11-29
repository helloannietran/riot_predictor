from scipy.stats.stats import pearsonr, spearmanr

from sknn.mlp import Classifier, Layer

import numpy as np
import urllib
from sknn.mlp import Classifier, Layer, Native
from lasagne import layers as lasagne, nonlinearities as nl

# print(dataset.shape)

# np.random.seed(993)
# 0.75 in avg 1500
# 0.793671519159 in 1000
# 0.77 1300
# 0.79 for 800
# 0.80 800
# 0.76 500
# 0.78 700
def make_neural_network():
    dataset = np.loadtxt("/Users/BARNES_3/Documents/niki/courses/Decision making/riot_predictor/data_for_neural.csv", delimiter=",")

    score_total = 0
    for i in xrange(0, 5):
        msk = np.random.rand(len(dataset)) < 0.8
        train = dataset[msk]
        test = dataset[~msk]
        x_train = train[:,0:6]
        y_train = train[:,6]
        x_test = test[:,0:6]
        y_test = test[:,6]
        # print type(x_test)
        # score = 0.797035347777
        # 0.801596351197
        nn = Classifier(
            layers=[
                # Layer("Tanh", units = 1000),
                # Layer("Sigmoid", units = 1000),
                # Layer("Linear")],
                Layer("ExpLin", units = 800),
                Layer("Softmax"),
                ],
            learning_rate=0.0002,
            n_iter=20)
        nn.fit(x_train, y_train)
        score = nn.score(x_test, y_test)
        score_total += score
    print score_total/5
    # print score
    return nn

def get_result(nn, arr):
    new_arr = []
    new_arr.append(arr)
    x_test = np.array(new_arr)
    y_valid = nn.predict(x_test)
    # predict_proba
    return y_valid[0,0]

nn = make_neural_network()
# get_result(nn, [[0.7], [2],[0],[3],[0.473398142],[10]])
# get_result(nn, [10.7,2,0,3,0.473398142,10])
# score = 0.74
# nn = Classifier(
#     layers=[
#         Layer("Linear")],
#     learning_rate=0.02,
#     n_iter=20)

# nn = Classifier(layers=[
#         Native(lasagne.DenseLayer, num_units=256, nonlinearity=nl.leaky_rectify)
#        ])



