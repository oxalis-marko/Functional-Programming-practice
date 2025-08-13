# Functional-Programming-practice

This is my solution to exercise that was given to me.

Base instructions were:
"You're building a data processing system that transforms customer order data through multiple stages using pure functional programming principles."
## What This Project Does
A functional programming pipeline that processes customer orders through four stages:
1. **Validation** - Validates orders based on value and customer tier
2. **Processing** - Applies tier-based discounts and calculates totals  
3. **Shipping** - Adds shipping costs and groups by delivery method
4. **Analytics** - Generates revenue reports and tier breakdowns

## CONSTRAINTS
- ***NO** classes or objects*(except given Enums)
- ***NO** mutations* - always return new data structures
- ***NO** loops* - use map/filter/reduce/recursion only
- *Pure functions* - same input always produces same output
- *Use all FP concepts:* first-class functions, closures, currying, recursion, sum types

## Given code:
```python
from enum import Enum
from functools import reduce

class OrderStatus(Enum):
    PENDING = 1
    VALIDATED = 2
    PROCESSED = 3
    SHIPPED = 4
    FAILED = 5

class CustomerTier(Enum):
    BRONZE = 1
    SILVER = 2
    GOLD = 3
    PLATINUM = 4

# Sample data structure
orders = [
    {"id": 1, "customer": "Alice", "tier": CustomerTier.GOLD, "items": [{"name": "laptop", "price": 1000, "qty": 1}], "status": OrderStatus.PENDING},
    {"id": 2, "customer": "Bob", "tier": CustomerTier.BRONZE, "items": [{"name": "mouse", "price": 25, "qty": 2}, {"name": "keyboard", "price": 75, "qty": 1}], "status": OrderStatus.PENDING},
    {"id": 3, "customer": "Carol", "tier": CustomerTier.PLATINUM, "items": [{"name": "monitor", "price": 300, "qty": 2}], "status": OrderStatus.PENDING}
]
```
## How to run
```python
python3 Functional_Programming_Extravaganza.py
```
## Sample output
```python
{'processed_orders': [{'id': 1, 'customer': 'Alice', 'tier': <CustomerTier.GOLD: 3>, 'items': [{'name': 'laptop', 'price': 900.0, 'qty': 1}], 'status': <OrderStatus.SHIPPED: 4>, 'total': 900.0, 'shipping cost': 5.0}, {'id': 3, 'customer': 'Carol', 'tier': <CustomerTier.PLATINUM: 4>, 'items': [{'name': 'monitor', 'price': 255.0, 'qty': 2}], 'status': <OrderStatus.SHIPPED: 4>, 'total': 510.0, 'shipping cost': 5.0}], 'failed_orders': [{'id': 2, 'customer': 'Bob', 'tier': <CustomerTier.BRONZE: 1>, 'items': [{'name': 'mouse', 'price': 25, 'qty': 2}, {'name': 'keyboard', 'price': 75, 'qty': 1}], 'status': <OrderStatus.FAILED: 5>}], 'analytics': {'total_revenue': 1410.0, 'average_order': 705.0, 'tier_breakdown': {<CustomerTier.BRONZE: 1>: {'total_revenue': 0.0, 'average_order': 0.0, 'total_orders': 0}, <CustomerTier.SILVER: 2>: {'total_revenue': 0.0, 'average_order': 0.0, 'total_orders': 0}, <CustomerTier.GOLD: 3>: {'total_revenue': 900.0, 'average_order': 900.0, 'total_orders': 1}, <CustomerTier.PLATINUM: 4>: {'total_revenue': 510.0, 'average_order': 510.0, 'total_orders': 1}}}, 'shipping_groups': {'express': 'No express orders', 'standard': [{'id': 1, 'customer': 'Alice', 'tier': <CustomerTier.GOLD: 3>, 'items': [{'name': 'laptop', 'price': 900.0, 'qty': 1}], 'status': <OrderStatus.PROCESSED: 3>, 'total': 900.0}, {'id': 3, 'customer': 'Carol', 'tier': <CustomerTier.PLATINUM: 4>, 'items': [{'name': 'monitor', 'price': 255.0, 'qty': 2}], 'status': <OrderStatus.PROCESSED: 3>, 'total': 510.0}]}}
