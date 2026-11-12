import pandas as pd

RAW_FILE_PATH = '../data/raw/online_retail_II.xlsx'
OUTPUT_PATH = '../data/processed/online_retail_clean.csv'

COLUMN_NAMES = {
    'Invoice': 'invoice',
    'StockCode': 'stock_code',
    'Description': 'description',
    'Quantity': 'quantity',
    'InvoiceDate': 'invoice_date',
    'Price': 'price',
    'Customer ID': 'customer_id',
    'Country': 'country',
}


def clean_retail_data():
    sheets = pd.read_excel(RAW_FILE_PATH, sheet_name=None, engine='calamine')
    print({name: sheet.shape for name, sheet in sheets.items()})
    df = pd.concat(sheets.values(), ignore_index=True)

    df = df.rename(columns=COLUMN_NAMES)

    print('--- DATASET INFO ---')
    df.info()
    print(df.isnull().sum())

    df['invoice_date'] = pd.to_datetime(df['invoice_date'])
    print('Date range:', df['invoice_date'].min(), '->', df['invoice_date'].max())

    df = df.dropna(subset=['customer_id'])
    df['customer_id'] = df['customer_id'].astype(int)

    df['description'] = df['description'].fillna('unknown')
    df['description'] = df['description'].str.strip().str.lower()

    df['stock_code'] = df['stock_code'].astype(str).str.strip().str.upper()

    df['invoice'] = df['invoice'].astype(str)
    df = df[~df['invoice'].str.startswith('C')]
    df = df[df['quantity'] > 0]
    df = df[df['price'] > 0]

    rows_before = len(df)
    df = df.drop_duplicates()
    print(f'Removed {rows_before - len(df)} duplicate rows. Final rows: {len(df)}')

    df.to_csv(OUTPUT_PATH, index=False)
    print(f'Saved clean data to {OUTPUT_PATH}')


if __name__ == '__main__':
    clean_retail_data()
