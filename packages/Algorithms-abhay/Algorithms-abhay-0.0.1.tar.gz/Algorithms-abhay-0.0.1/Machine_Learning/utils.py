import numpy as np
import pandas as pd


def file_prep(path):
    FILEDF = pd.read_csv(path)
    cols = FILEDF.columns
    y = FILEDF[cols[-1]]
    X = FILEDF.drop(columns = cols[-1])
    X = X.to_numpy()
    y = y.to_numpy()
    y = encoder(y)
    return X, y, cols
    
def encoder (y):
    unique = list(np.unique(y))
    encoder = lambda x: unique.index(x)
    y_new = 2*np.array(list(map(encoder, y)))-1 
    return y_new

def dict_printer(params):
    for key, value in params.items():
        print(key,value)

def my_train_test_split(X, y, test_size=0.2, random_state=42):
    [row, _] = X.shape
    index = np.arange(row)
    np.random.seed(random_state)
    np.random.shuffle(index)
    stop = int((row-1)*(1-test_size))
    X_train, y_train = X[index[:stop]], y[index[:stop]]
    X_test, y_test = X[index[stop:]], y[index[stop:]]
    return X_train, X_test, y_train, y_test

