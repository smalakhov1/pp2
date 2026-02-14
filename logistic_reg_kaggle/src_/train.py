import numpy as np
import pandas as pd


def train_test_split(X_df,y,test_size=0.2,random_state=20):

    X = X_df.to_numpy()
    y = y.to_numpy()

    n_samples = X.shape[0]
    
    rng =  np.random.default_rng(random_state)
    indicies = np.arange(n_samples)
    rng.shuffle(indicies)

    test_count = int(test_size*n_samples)

    test_idx = indicies[:test_count]
    train_idx = indicies[test_count:]

    X_train = X[train_idx]
    X_test = X[test_idx]

    y_train = y[train_idx]
    y_test = y[test_idx]

    return X_train, X_test, y_train, y_test



def normalize_features(X_train, X_test):
    mean = X_train.mean(axis=0)
    std = X_train.std(axis=0)

    std[std==0]=1.0

    X_train_norm = (X_train - mean)/std
    X_test_norm = (X_test - mean)/std

    return X_train_norm, X_test_norm, mean, std

def sigmoid(z):
    return 1/(1+np.exp(-z))

def prediction (X,w,b):
    z = np.dot(X,w)+b
    y_pred=sigmoid(z)
    return y_pred

def compute_loss(y_true, y_pred):
    eps = 1e-15
    y_pred = np.clip(y_pred, eps, 1-eps)
    loss = -np.mean((y_true* np.log(y_pred))+(1-y_true)*np.log(1.0-y_pred))
    return loss

def compute_gradients(X, y_true,y_pred):
    m = X.shape[0] #n_samples
    error = y_pred - y_true
    dw =(X.T @ error) / m
    db = np.mean(error)
    return dw, db

def train_logistic_regression(X,y, learning_rate = 0.1, n_iters=1000):
    n_samples, n_features = X.shape # m,n
    w=np.zeros(n_features)
    b = 0.0
    losses =[] #cost_history
    train_losses = []
    test_losses = []
    for i in range(n_iters):

        y_pred = prediction(X,w,b)
        loss = compute_loss(y, y_pred)
        losses.append(loss)

        dw, db =compute_gradients(X,y,y_pred)

        w = w - learning_rate*dw
        b = b - learning_rate*db
        

    return w,b,losses
