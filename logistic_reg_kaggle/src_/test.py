import data_preprocess as dpp
import visualization as vis

path = "/Users/rufat/c++/logistic_reg_kaggle/data/Heart_Disease_Prediction.csv"
df = dpp.load_csv(path=path)
X_df, y =dpp.select_features_and_target(df=df)
y_encoded = dpp.encode_target(y)
X_df_clean, y_clean = dpp.clean_data(X_df=X_df,y=y_encoded)

vis.plot_2d(X_df_clean,y_clean, "Age", "Cholesterol")
vis.plot_2d(X_df_clean,y_clean, "Age", "BP")
vis.plot_2d(X_df_clean,y_clean, "Age", "Max HR")
vis.plot_2d(X_df_clean,y_clean, "Age", "ST depression")

vis.plot_2d(X_df_clean,y_clean, "BP", "Cholesterol")
vis.plot_2d(X_df_clean,y_clean, "BP", "Max HR")
vis.plot_2d(X_df_clean,y_clean, "BP", "ST depression")

vis.plot_2d(X_df_clean,y_clean, "Max HR", "Cholesterol")
vis.plot_2d(X_df_clean,y_clean, "Max HR", "ST depression")

vis.plot_2d(X_df_clean,y_clean, "ST depression", "Cholesterol")
