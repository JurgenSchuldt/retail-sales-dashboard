import pandas as pd

def load_data(filepath):
    df = pd.read_csv(filepath, encoding='utf-8')
    return df

def explore_data(df):
    print("=== DIMENSIONES ===")
    print(f"Filas: {df.shape[0]:,} | Columnas: {df.shape[1]}")
    
    print("\n=== COLUMNAS ===")
    print(df.dtypes)
    
    print("\n=== PRIMERAS 5 FILAS ===")
    print(df.head())
    
    print("\n=== VALORES NULOS ===")
    nulls = df.isnull().sum()
    print(nulls[nulls > 0])
    
    print("\n=== ESTADÍSTICAS BÁSICAS ===")
    print(df.describe())

if __name__ == "__main__":
    df = load_data("data/online_retail_II.csv")
    explore_data(df)