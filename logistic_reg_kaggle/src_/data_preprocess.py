import pandas as pd

def load_csv(*,path):
    df = pd.read_csv(path)
    if df.empty:
        raise ValueError("CSV файл пуст")
    return df

FEATURE_COLUMNS=["Age","BP", "Cholesterol","Max HR", "ST depression", "Number of vessels fluro", "Thallium"]
TARGET_COLUMN = "Heart Disease"

def select_features_and_target(*,df):

    missing_features = set(FEATURE_COLUMNS) - set(df.columns)
    if missing_features:
        raise ValueError(f"Отсутвуют колонки {missing_features}")
    # if TARGET_COLUMN not in df.columns:
    #     raise ValueError (f"Отсутвует target колонка {TARGET_COLUMN}")
    
    X_df = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]
    return X_df,y
def encode_target (y):
    
    mapping = {"Presence": 1,
               "Absence": 0}
    y_encoded = y.map(mapping)

    if y_encoded.isnull().any():
        raise ValueError("Target содержит неожиданные значения")
    
    return y_encoded
def clean_data(X_df,y):

    df = X_df.copy()
    df["target"] = y
    df = df.dropna()

    y_clean = df["target"]
    X_df_clean = df.drop(columns=["target"])
    X_df_clean = X_df_clean.astype(float)

    return X_df_clean, y_clean