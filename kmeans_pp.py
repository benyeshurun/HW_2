import sys
import numpy as np
import pandas as pd
import kmeans.c

# define PY_SSIZE_T_CLEAN
# include <Python.h>

DEFAULT_ITER = 300
MIN_ARGUMENTS = 4


def validate_and_assign_input_user():
    if len(sys.argv) < MIN_ARGUMENTS:
        raise Exception(f"Amount of arguments should be more than 1, amount of arguments={len(sys.argv)}")
    if (not sys.argv[1].isdigit()) or int(sys.argv[1]) < 2:
        raise Exception(f"K input has to be a number and should exceed 0, k={sys.argv[1]}")
    k = int(sys.argv[1])
    max_iter = DEFAULT_ITER
    if len(sys.argv) > 4:
        if (sys.argv[2].isdigit()) and int(sys.argv[2]) > 0:
            max_iter = sys.argv[2]
        else:
            raise Exception(f"max_iter input has to be a number and should exceed 0, max_iter={sys.argv[2]}")
    return k, max_iter


def build_panda():
    try:
        if len(sys.argv) > 4:
            pd_1 = pd.read_csv(sys.argv[3])
            pd_2 = pd.read_csv(sys.argv[4])
        else:
            pd_1 = pd.read_csv(sys.argv[2])
            pd_2 = pd.read_csv(sys.argv[3])
    except FileNotFoundError:
        print("File not accessible")
        return merge_pandas(pd_1, pd_2)


def merge_pandas(df, other):
    a = []
    b = []
    for i in range(len(df.columns)):
        a.append(float(list(df)[i]))
        # for i in range(len(pd_2.columns)):
        b.append(float(list(other)[i]))
    df.loc[-1] = a  # adding a row
    df.index = df.index + 1  # shifting index
    df = df.sort_index()
    other.loc[-1] = a  # adding a row
    other.index = other.index + 1  # shifting index
    other = other.sort_index()
    df.rename(columns={list(df)[0]: 'x'}, inplace=True)  # renaming both first columns for the merge
    other.rename(columns={list(other)[0]: 'x'}, inplace=True)
    df = pd.merge(df, other, how='inner', on='x')
    return df


def choose_random_centrals(vectors, k):
    np.random.seed(593)
    clusters_indexes = np.random.randint(0, len(vectors.index), k)
    clusters_list = []
    for x in clusters_indexes:
        clusters_list.append(vectors.iloc[x,])
    return clusters_list


# prints new central after adjusting for the relevant structure
def print_centrals(list_of_clusters):
    for cluster in list_of_clusters:
        for i in range(len(cluster.curr_central)):  # todo - maybe delete this part
            cluster[i] = "{:.4f}".format(cluster[i])
        print(*cluster, sep=' ')


def main():
    k, max_iter = validate_and_assign_input_user()
    list_of_vectors = build_panda()
    list_of_clusters = choose_random_centrals(list_of_vectors, k)
    dimensions = len(list_of_vectors.columns)  # vectors have extra dimension to hold their cluster allocation
    list_of_clusters_array = list_of_clusters.to_numpy()
    print_centrals(list_of_clusters_array)
    list_of_final_clusters = fit(list_of_vectors, list_of_clusters, k, dimensions)
    print_centrals(list_of_final_clusters)


if __name__ == '__main__':
    main()