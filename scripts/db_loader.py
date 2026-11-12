import os

import pandas as pd
from sqlalchemy import create_engine

DATABASE_URL = os.environ["DATABASE_URL"]
CLEAN_CSV_PATH = '../data/processed/online_retail_clean.csv'


def load_star_schema():
    engine = create_engine(DATABASE_URL)

    df = pd.read_csv(
        CLEAN_CSV_PATH,
        parse_dates=['invoice_date'],
        dtype={'stock_code': str, 'invoice': str},
    )

    dim_customers = df[['customer_id', 'country']].drop_duplicates(subset=['customer_id'])
    dim_customers.to_sql('dim_customers', con=engine, if_exists='replace', index=False)

    dim_products = df[['stock_code', 'description']].drop_duplicates(subset=['stock_code'])
    dim_products.to_sql('dim_products', con=engine, if_exists='replace', index=False)

    fact_transactions = df[[
        'invoice',
        'stock_code',
        'customer_id',
        'quantity',
        'invoice_date',
        'price',
    ]]
    fact_transactions.to_sql('fact_transactions', con=engine, if_exists='replace', index=False)

    print(f'Loaded {len(dim_customers)} customers, {len(dim_products)} products, '
          f'{len(fact_transactions)} transaction rows.')


if __name__ == '__main__':
    load_star_schema()
