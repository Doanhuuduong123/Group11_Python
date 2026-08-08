import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Set seed for reproducibility
np.random.seed(42)

# Parameters
num_records = 650

categories = {
    'Furniture': ['Bookcases', 'Chairs', 'Tables', 'Furnishings'],
    'Office Supplies': ['Labels', 'Storage', 'Art', 'Binders', 'Appliances', 'Paper'],
    'Technology': ['Phones', 'Accessories', 'Copiers', 'Machines']
}

regions = ['North', 'South', 'East', 'West']
segments = ['Consumer', 'Corporate', 'Home Office']

customer_pool = [
    (f"CUST-{1000 + i}", f"Customer {i+1}") for i in range(120)
]

start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 12, 31)

records = []
for i in range(1, num_records + 1):
    order_id = f"CA-2024-{10000 + i % 400}"  # Some orders have multiple items
    order_days_offset = np.random.randint(0, (end_date - start_date).days)
    order_date = start_date + timedelta(days=order_days_offset)
    ship_date = order_date + timedelta(days=np.random.randint(1, 6))
    
    cust_id, cust_name = customer_pool[np.random.randint(0, len(customer_pool))]
    segment = np.random.choice(segments, p=[0.5, 0.3, 0.2])
    region = np.random.choice(regions)
    
    cat = np.random.choice(list(categories.keys()), p=[0.3, 0.5, 0.2])
    sub_cat = np.random.choice(categories[cat])
    product_name = f"{cat} - {sub_cat} Model {np.random.randint(100, 999)}"
    
    # Financials
    base_unit_price = np.random.uniform(15, 500)
    quantity = np.random.randint(1, 8)
    discount = np.random.choice([0.0, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5], p=[0.4, 0.2, 0.15, 0.1, 0.08, 0.04, 0.03])
    
    sales = round(base_unit_price * quantity * (1 - discount), 2)
    # Profit logic: high discount harms profit margin
    profit_margin = 0.25 - (discount * 0.8) + np.random.uniform(-0.05, 0.05)
    profit = round(sales * profit_margin, 2)
    
    records.append({
        'Order ID': order_id,
        'Order Date': order_date.strftime('%Y-%m-%d'),
        'Ship Date': ship_date.strftime('%Y-%m-%d'),
        'Customer ID': cust_id,
        'Customer Name': cust_name,
        'Segment': segment,
        'Region': region,
        'Category': cat,
        'Sub-Category': sub_cat,
        'Product Name': product_name,
        'Sales': sales,
        'Quantity': quantity,
        'Discount': discount,
        'Profit': profit
    })

df = pd.DataFrame(records)

# Introduce a tiny controlled missing values / duplicates for testing preprocessing
df.loc[15, 'Sales'] = np.nan
df.loc[42, 'Profit'] = np.nan

# Save to raw data directory
os.makedirs(os.path.join('data', 'raw'), exist_ok=True)
df.to_csv(os.path.join('data', 'raw', 'Superstore.csv'), index=False)
print(f"Successfully generated dataset with {len(df)} rows at data/raw/Superstore.csv")
