import json
import pandas as pd

warehouse_east_json = '''
[
    {"sku": "A100", "product_name": "Blue Shirt", "stock": 25},
    {"sku": "A101", "product_name": "Red Hat", "stock": 10},
    {"sku": "A102", "product_name": "Black Shoes", "stock": 0}
]
'''
warehouse_west_json = '''
[
    {"sku": "A100", "product_name": "Blue Shirt", "stock": 15},
    {"sku": "A102", "product_name": "Black Shoes", "stock": 8},
    {"sku": "A103", "product_name": "Green Jacket", "stock": 20}
]
'''
warehouse_central_json = '''
[
    {"sku": "A101", "product_name": "Red Hat", "stock": 5},
    {"sku": "A103", "product_name": "Green Jacket", "stock": 12}
]
'''

df_east = pd.DataFrame(json.loads(warehouse_east_json))
df_west = pd.DataFrame(json.loads(warehouse_west_json))
df_central = pd.DataFrame(json.loads(warehouse_central_json))

df_east['warehouse'] = 'East'
df_west['warehouse'] = 'West'
df_central['warehouse'] = 'Central'

combined_df = pd.concat([df_east, df_west, df_central], ignore_index=True)

# Total stock per product
total_stock = combined_df.groupby(['sku', 'product_name'])['stock'].sum().reset_index()
print("Total stock across all warehouses:")
print(total_stock)

# Stock per warehouse (aggfunc='sum' so duplicates are added, not averaged)
stock_by_warehouse = combined_df.pivot_table(
    index=['sku', 'product_name'],
    columns='warehouse',
    values='stock',
    aggfunc='sum',
    fill_value=0,
)
print("\nStock by warehouse:")
print(stock_by_warehouse)

# Products with zero stock everywhere
out_of_stock = total_stock[total_stock['stock'] == 0]
print("\n🚨 Completely out of stock (all warehouses):")
print(out_of_stock)

# Rebalancing: one warehouse has a big surplus, another has none
MIN_SURPLUS = 10

print("\n⚖️ Rebalancing candidates:")
for index, row in stock_by_warehouse.iterrows():
    if row.max() >= MIN_SURPLUS and row.min() == 0:
        print(f"{index}: {row.to_dict()}")