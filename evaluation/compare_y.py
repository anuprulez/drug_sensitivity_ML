import sklearn.metrics
import pandas as pd
import numpy as np



def main():
    train_file = "../psl/data/first_model/seed0/cross_val/5fold/fold1_train.txt"
    test_file = "../psl/data/first_model/seed0/cross_val/5fold/fold1_val.txt"
    infer_file = "../psl/result/first_model_cross_val_fold1_result.txt"

    tr_df, val_df, infer_df = load_data(train_file, test_file, infer_file)
    print calculate_accuracy(tr_df, infer_df)
    print calculate_accuracy(val_df, infer_df)


def load_data(train_file, test_file, infer_file):
    dataframes = []
    for each_file in [train_file, test_file, infer_file]:
        rows = []
        with open(each_file, "r") as f:
            for line in f:
                items = line.strip("\n").split("\t")
                cell_drug_pair = items[0] + items[1]
                value = float(items[-1])
                rows.append({"cell_drug_pair": cell_drug_pair, "y": value})
        f.close()
        df = pd.DataFrame(rows)
        dataframes.append(df)
    return dataframes


def calculate_accuracy(truth_df, infer_df):
    infer_df = infer_df.loc[infer_df.cell_drug_pair.isin(truth_df.cell_drug_pair)].copy()
    df = pd.merge(infer_df, truth_df, on="cell_drug_pair", suffixes=["_infer", "_truth"]) 
    mse = sklearn.metrics.mean_squared_error(df.y_truth, df.y_infer)
    accuracy, auc = binary_result(df)

    return mse, accuracy, auc


def binary_result(df):
    """ take >75% as label 1 and <25% as label 0, return accuracy"""
    df.y_truth[df.y_truth >= 0.75] = 1 
    df.y_truth[df.y_truth <= 0.25] = 0
    binary_df = df[(df.y_truth == 1) | (df.y_truth==0)].copy()
    binary_df.y_infer[df.y_infer >= 0.5] = 1 
    binary_df.y_infer[df.y_infer < 0.5] = 0
    accuracy = sklearn.metrics.accuracy_score(binary_df.y_truth, binary_df.y_infer)
    auc = sklearn.metrics.roc_auc_score(binary_df.y_truth, binary_df.y_infer)
    return accuracy, auc 


if __name__=="__main__":
    main()
