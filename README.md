# Multi-Warehouse Inventory

A Python script that combines stock data from several warehouses into one view, so you can see total availability, where stock sits, and where it might need to move.

## How it works
- Parses stock data from three warehouses (East, West, Central) stored as JSON
- Tags each record with its warehouse and combines them into one DataFrame with `pd.concat()`
- Calculates total stock per product across all warehouses
- Builds a pivot table of stock by product and warehouse
- Lists products that are out of stock in every warehouse
- Flags rebalancing candidates: products with a large surplus in one warehouse and none in another

## How to run
```bash
python warehouse_inventory.py
```

## What I learned
- Adding a source column (`warehouse`) before combining datasets so each row keeps its origin
- Using `pd.concat()` to stack DataFrames that share the same columns
- Using `.groupby([...])['stock'].sum()` to total a value per product
- Using `pd.pivot_table()` with `aggfunc='sum'` and `fill_value=0` to reshape data into a product-by-warehouse grid
- Using `.iterrows()` with `row.max()` and `row.min()` to apply a rule to each product's row
- Using a named constant (`MIN_SURPLUS`) instead of a hard-coded number

## Limitations
- A stock of 0 can mean "out of stock" or "this warehouse doesn't carry the product," and the pivot table treats both the same.
- The rebalancing check shows which products are unevenly distributed, but not which warehouse should send to which.

## Dependencies
Requires pandas:
```bash
pip install pandas
```
