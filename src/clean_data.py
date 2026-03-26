import pandas as pd

def load_and_clean(filepath):
    df = pd.read_csv(filepath, encoding='utf-8')
    
    print(f"Filas originales: {len(df):,}")
    
    # Eliminar filas sin Customer ID
    df = df.dropna(subset=['Customer ID'])
    print(f"Tras eliminar sin Customer ID: {len(df):,}")
    
    # Eliminar devoluciones (Quantity o Price negativos)
    df = df[(df['Quantity'] > 0) & (df['Price'] > 0)]
    print(f"Tras eliminar devoluciones: {len(df):,}")
    
    # Convertir fecha
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    
    # Crear columna de ingresos
    df['Revenue'] = df['Quantity'] * df['Price']
    
    # Extraer mes y año
    df['Year'] = df['InvoiceDate'].dt.year
    df['Month'] = df['InvoiceDate'].dt.month
    df['YearMonth'] = df['InvoiceDate'].dt.to_period('M').astype(str)
    
    # Customer ID como entero
    df['Customer ID'] = df['Customer ID'].astype(int)
    
    print(f"Filas finales limpias: {len(df):,}")
    print(f"Periodo: {df['InvoiceDate'].min()} → {df['InvoiceDate'].max()}")
    print(f"Países únicos: {df['Country'].nunique()}")
    print(f"Clientes únicos: {df['Customer ID'].nunique():,}")
    
    return df

if __name__ == "__main__":
    df = load_and_clean("data/online_retail_II.csv")