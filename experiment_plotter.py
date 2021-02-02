import re
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pickle

results_svc_10 = ["misc/experiment_results/experiment_heuristic_1a_-_svc_-_users_10_-_split_mode_i_-_2021-01-31 22:14:34.397142.pkl",
                  "misc/experiment_results/experiment_heuristic_1a_-_svc_-_users_10_-_split_mode_ii_-_2021-01-31 22:14:06.078060.pkl",
                  "misc/experiment_results/experiment_heuristic_1a_-_svc_-_users_10_-_split_mode_iii_-_2021-01-31 22:17:09.905436.pkl",
                  "misc/experiment_results/experiment_heuristic_1a_-_svc_-_users_10_-_split_mode_iv_-_2021-01-31 22:17:58.045047.pkl",
                  "misc/experiment_results/experiment_heuristic_1b_-_svc_-_users_10_-_split_mode_test_i_-_2021-01-31 22:17:59.881461.pkl",
                  "misc/experiment_results/experiment_heuristic_1b_-_svc_-_users_10_-_split_mode_test_ii_-_2021-01-31 22:17:37.221874.pkl",
                  "misc/experiment_results/experiment_heuristic_1b_-_svc_-_users_10_-_split_mode_test_iii_-_2021-01-31 22:17:39.000470.pkl",
                  "misc/experiment_results/experiment_heuristic_1b_-_svc_-_users_10_-_split_mode_test_iv_-_2021-01-31 22:16:23.921792.pkl",
                  "misc/experiment_results/experiment_heuristic_1c_-_svc_-_users_10_-_split_mode_test_i_-_2021-01-31 22:16:50.155062.pkl",
                  "misc/experiment_results/experiment_heuristic_1c_-_svc_-_users_10_-_split_mode_test_ii_-_2021-01-31 22:16:06.742121.pkl",
                  "misc/experiment_results/experiment_heuristic_1c_-_svc_-_users_10_-_split_mode_test_iii_-_2021-01-31 22:17:32.254730.pkl",
                  "misc/experiment_results/experiment_heuristic_1c_-_svc_-_users_10_-_split_mode_test_iv_-_2021-01-31 22:17:18.258321.pkl"]


def get_results(files_list):
    results=[]
    for filename in files_list:
        heuristic = re.search("heuristic_..", filename).group()
        split_mode = re.search("(split_mode_((i_)|(ii_)|(iii_)|(iv_)))|(split_mode_test_((i_)|(ii_)|(iii_)|(iv_)))", filename).group()
        model = re.search("(svc)|(randomforest)|(knearestneighbors)", filename).group()
        users = re.search("users_[0-9]{1,3}", filename).group()[6:]
        f = open(filename, "rb")
        data = pickle.load(f)
        results.append([data, heuristic, split_mode, model, users])
    return results


def plot_results(results):
    fig, axn = plt.subplots(3, 4)
    for i, ax in enumerate(axn.flat):
        cm = [[results[i][0][1]["true_positive"], results[i][0][1]["false_positive"]], [results[i][0][1]["false_negative"], results[i][0][1]["true_negative"]]]
        sns.heatmap(cm/np.sum(cm), ax=ax, annot=True, fmt = ".2%", cmap="Spectral")
        ax.set(title=str(results[i][1][:-1]) + "; " + str(results[i][2][:-1]))
        ax.xaxis.set_ticklabels(['True', 'False'])
        ax.yaxis.set_ticklabels(['True', 'False'])
    fig.suptitle("Experiment Results for Model: " + str(results[0][3]) + "; " + str(results[0][4]) + " Users", fontsize=16)
    plt.setp(axn[-1, :], xlabel='Actual')
    plt.setp(axn[:, 0], ylabel='Predicted')
    plt.show()

plot_results(get_results(results_svc_10))