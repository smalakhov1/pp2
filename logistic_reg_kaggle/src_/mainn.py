from data_preprocess import (
    load_csv,
    select_features_and_target,
    encode_target,
    clean_data
)

from train import (
    train_test_split,
    normalize_features,
    train_logistic_regression,
    prediction
)

from visualization import plot_2d, plot_losses

import numpy as np

def main():
    df = load_csv(path="/Users/rufat/Desktop/progfiles/logistic_reg_kaggle/data/Heart_Disease_Prediction.csv")

    X_df,y=select_features_and_target(df=df)

    y_encoded = encode_target(y)

    X_df_clean, y_clean = clean_data(X_df,y_encoded)


    #EDA
    # plot_2d(X_df_clean,y_clean, "Age", "Cholesterol")
    # plot_2d(X_df_clean,y_clean, "Age", "BP")
    # plot_2d(X_df_clean,y_clean, "Age", "Max HR")
    # plot_2d(X_df_clean,y_clean, "Age", "ST depression")

    # plot_2d(X_df_clean,y_clean, "BP", "Cholesterol")
    # plot_2d(X_df_clean,y_clean, "BP", "Max HR")
    # plot_2d(X_df_clean,y_clean, "BP", "ST depression")

    # plot_2d(X_df_clean,y_clean, "Max HR", "Cholesterol")
    # plot_2d(X_df_clean,y_clean, "Max HR", "ST depression")

    # plot_2d(X_df_clean,y_clean, "ST depression", "Cholesterol")


    X_train, X_test, y_train, y_test = train_test_split(X_df_clean,y_clean, test_size=0.2)

    X_train_norm, X_test_norm, mean, std = normalize_features(X_train, X_test)

    w,b, losses = train_logistic_regression(X_train,y_train,learning_rate = 0.00001, n_iters=1000000)


    probs_test = prediction(X_test_norm, w, b)
    y_pred_test = (probs_test>=0.5).astype(int)
    accuracy = np.mean(y_pred_test==y_test)


    print("Test accuracy: ", accuracy)
    
    plot_losses(losses)

    if __name__ == "__main__":
        main()

main()



