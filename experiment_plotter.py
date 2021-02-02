import re
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

results_svc_5 = []
resulst_randomforest_5 = []
results_knearest_5 = []

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

resulst_randomforest_10 = [ "misc/experiment_results/experiment_heuristic_1a_-_randomforest_-_users_10_-_split_mode_i_-_2021-01-31 20:41:17.723276.pkl",
                            "misc/experiment_results/experiment_heuristic_1a_-_randomforest_-_users_10_-_split_mode_ii_-_2021-01-31 20:41:43.361280.pkl",
                            "misc/experiment_results/experiment_heuristic_1a_-_randomforest_-_users_10_-_split_mode_iii_-_2021-01-31 20:42:15.501037.pkl",
                            "misc/experiment_results/experiment_heuristic_1a_-_randomforest_-_users_10_-_split_mode_iv_-_2021-01-31 20:42:35.575134.pkl",
                            "misc/experiment_results/experiment_heuristic_1b_-_randomforest_-_users_10_-_split_mode_test_i_-_2021-01-31 20:42:22.960105.pkl",
                            "misc/experiment_results/experiment_heuristic_1b_-_randomforest_-_users_10_-_split_mode_test_ii_-_2021-01-31 20:42:43.490143.pkl",
                            "misc/experiment_results/experiment_heuristic_1b_-_randomforest_-_users_10_-_split_mode_test_iii_-_2021-01-31 20:42:55.225973.pkl",
                            "misc/experiment_results/experiment_heuristic_1b_-_randomforest_-_users_10_-_split_mode_test_iv_-_2021-01-31 20:43:04.231156.pkl",
                            "misc/experiment_results/experiment_heuristic_1c_-_randomforest_-_users_10_-_split_mode_test_i_-_2021-01-31 20:43:06.922581.pkl",
                            "misc/experiment_results/experiment_heuristic_1c_-_randomforest_-_users_10_-_split_mode_test_ii_-_2021-01-31 20:43:17.965859.pkl",
                            "misc/experiment_results/experiment_heuristic_1c_-_randomforest_-_users_10_-_split_mode_test_iii_-_2021-01-31 20:43:24.197532.pkl",
                            "misc/experiment_results/experiment_heuristic_1c_-_randomforest_-_users_10_-_split_mode_test_iv_-_2021-01-31 20:43:30.942345.pkl"]

results_knearest_10 = ["misc/experiment_results/experiment_heuristic_1a_-_knearestneighbors_-_users_10_-_split_mode_i_-_2021-01-31 20:41:50.780321.pkl",
                        "misc/experiment_results/experiment_heuristic_1a_-_knearestneighbors_-_users_10_-_split_mode_ii_-_2021-01-31 20:42:08.136114.pkl",
                        "misc/experiment_results/experiment_heuristic_1a_-_knearestneighbors_-_users_10_-_split_mode_iii_-_2021-01-31 20:42:26.924856.pkl",
                        "misc/experiment_results/experiment_heuristic_1a_-_knearestneighbors_-_users_10_-_split_mode_iv_-_2021-01-31 20:42:47.819982.pkl",
                        "misc/experiment_results/experiment_heuristic_1b_-_knearestneighbors_-_users_10_-_split_mode_test_i_-_2021-01-31 20:42:51.461612.pkl",
                        "misc/experiment_results/experiment_heuristic_1b_-_knearestneighbors_-_users_10_-_split_mode_test_ii_-_2021-01-31 20:43:01.658287.pkl",
                        "misc/experiment_results/experiment_heuristic_1b_-_knearestneighbors_-_users_10_-_split_mode_test_iii_-_2021-01-31 20:43:11.172334.pkl",
                        "misc/experiment_results/experiment_heuristic_1b_-_knearestneighbors_-_users_10_-_split_mode_test_iv_-_2021-01-31 20:43:14.568513.pkl",
                        "misc/experiment_results/experiment_heuristic_1c_-_knearestneighbors_-_users_10_-_split_mode_test_i_-_2021-01-31 20:43:17.160511.pkl",
                        "misc/experiment_results/experiment_heuristic_1c_-_knearestneighbors_-_users_10_-_split_mode_test_ii_-_2021-01-31 20:43:22.097965.pkl",
                        "misc/experiment_results/experiment_heuristic_1c_-_knearestneighbors_-_users_10_-_split_mode_test_iii_-_2021-01-31 20:43:32.602982.pkl",
                        "misc/experiment_results/experiment_heuristic_1c_-_knearestneighbors_-_users_10_-_split_mode_test_iv_-_2021-01-31 20:43:31.202168.pkl"]

results_svc_20 = []
resulst_randomforest_20 = []
results_knearest_20 = []

resulst_randomforest_50 = []
results_knearest_50 = []

resulst_randomforest_100 = []
results_knearest_100 = []
#TODO: add all file paths to lists

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
        sns.heatmap(cm, ax=ax, annot=True,fmt='g', cmap="Spectral")
        ax.set(title=str(results[i][1]) + "; " + str(results[i][2][:-1]))
        ax.xaxis.set_ticklabels(['True', 'False'])
        ax.yaxis.set_ticklabels(['True', 'False'])
    fig.suptitle("Experiment Results for Model: " + str(results[0][3]) + "; " + str(results[0][4]) + " Users", fontsize=16)
    plt.setp(axn[-1, :], xlabel='Actual')
    plt.setp(axn[:, 0], ylabel='Predicted')
    plt.show()


def select_plots(users):
    results_list = []
    if users == 5:
        results_list.append(get_results(results_svc_5))
        results_list.append(get_results(results_knearest_5))
        results_list.append(get_results(resulst_randomforest_5))
    elif users == 10:
        results_list.append(get_results(results_svc_10))
        results_list.append(get_results(results_knearest_10))
        results_list.append(get_results(resulst_randomforest_10))
    elif users == 20:
        results_list.append(get_results(results_svc_20))
        results_list.append(get_results(results_knearest_20))
        results_list.append(get_results(resulst_randomforest_20))
    elif users == 50:
        results_list.append(get_results(results_knearest_50))
        results_list.append(get_results(resulst_randomforest_50))
    elif users == 100:
        results_list.append(get_results(results_knearest_100))
        results_list.append(get_results(resulst_randomforest_100))
    return results_list


def show_all_plots(users):
    results_list = select_plots(users)
    for results in results_list:
        fig, axn = plt.subplots(3, 4)
        for i, ax in enumerate(axn.flat):
            cm = [[results[i][0][1]["true_positive"], results[i][0][1]["false_positive"]],
                  [results[i][0][1]["false_negative"], results[i][0][1]["true_negative"]]]
            sns.heatmap(cm, ax=ax, annot=True, fmt='g', cmap="Spectral")
            ax.set(title=str(results[i][1]) + "; " + str(results[i][2][:-1]))
            ax.xaxis.set_ticklabels(['True', 'False'])
            ax.yaxis.set_ticklabels(['True', 'False'])
        fig.suptitle("Experiment Results for Model: " + str(results[0][3]) + "; " + str(results[0][4]) + " Users",
                     fontsize=16)
        plt.setp(axn[-1, :], xlabel='Actual')
        plt.setp(axn[:, 0], ylabel='Predicted')
        plt.show()
        plt.close()

show_all_plots(10)