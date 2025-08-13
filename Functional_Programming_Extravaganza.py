# The Data Pipeline Processor

# CONSTRAINTS
# NO classes or objects(except given Enums)
# NO mutations - always return new data structures
# NO loops - use map/filter/reduce/recursion only
# Pure functions - same input always producec same output
# Use all FP concepts: first-class functions, closures, currying, recursion, sum types

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
def main():
    orders = [
        {"id": 1, "customer": "Alice", "tier": CustomerTier.GOLD, "items": [{"name": "laptop", "price": 1000, "qty": 1}], "status": OrderStatus.PENDING},
        {"id": 2, "customer": "Bob", "tier": CustomerTier.BRONZE, "items": [{"name": "mouse", "price": 25, "qty": 2}, {"name": "keyboard", "price": 75, "qty": 1}], "status": OrderStatus.PENDING},
        {"id": 3, "customer": "Carol", "tier": CustomerTier.PLATINUM, "items": [{"name": "monitor", "price": 300, "qty": 2}], "status": OrderStatus.PENDING}
    ]
    five_hundred_validator = validation_stage(500)
    shipping_stage = ship_stage()
    orders, shipping_list = shipping_stage(processing_stage(five_hundred_validator(orders)))
    print(analytics_stage(orders)(shipping_list))

# orders > value threshold valid
# orders <= value threshold: check if customer is silver tier or better, then valid, else invalid
# return tuple (valid_orders, failed_orders)
def validation_stage(value_threshold):
    def validator(orders):
        all_orders = orders.copy()
        non_corrupted = filter(lambda order: param_validation_check(order), all_orders)
        # process orders into tuple (("id", "tier"), all item value)
        processed_orders = list(zip(map(lambda order: (order["id"], order["tier"]), all_orders), get_order_value(non_corrupted)))
        #print(processed_orders)
        # make new list of order ids
        valid_orders_id = list(map(lambda order: order[0][0], (filter(lambda order: order[1] > 500 or (order[0][1] is not CustomerTier.BRONZE and order[0][1] is not None), processed_orders))))
        
        valid_orders = list(map(lambda order: set_status(order, OrderStatus.VALIDATED), filter(lambda order: order["id"] in valid_orders_id, all_orders)))
        failed_orders = list(map(lambda order: set_status(order, OrderStatus.FAILED), filter(lambda order: order["id"] not in valid_orders_id, all_orders)))
        return (valid_orders, failed_orders)
    return validator

def param_validation_check(order):
    exam_taker = order.copy()
    if dict(filter(lambda param: order[param] is None, exam_taker)) == {}:
        if list(exam_taker["items"]) != []:
            return len(exam_taker["items"]) == len(list(filter(lambda item: cart_item_check(item), exam_taker["items"])))
            
def cart_item_check(item):
    exam_item = item.copy()
    return (isinstance(exam_item["name"], str) 
    and isinstance(exam_item["price"], int) and exam_item["price"] > 0
    and isinstance(exam_item["qty"], int) and exam_item["qty"] > 0)

# this functions helps keeping code clean in my opinion
def get_order_value(orders): # orders(list) -> order(dict) -> order["items"](list) -> item(dict) -> item["price"](int) * item["qty"](int)
    return map(lambda item_list: reduce(lambda i1, i2: i1 + i2 , map(lambda item: item["price"] * item["qty"], item_list)), map(lambda order: order["items"], orders))

def set_status(order, status):
    new_order = order
    new_order["status"] = status
    return new_order

# apply tier discounts
# calculate final totals
def processing_stage(all_orders):
    processing_orders = all_orders[0]
    failed_orders = all_orders[1]
    discout_applied = list(map(lambda order: apply_discount(order), processing_orders))
    value_w_no_shipping = list(get_order_value(discout_applied))
    # turns out 'zip()' is so lazy it doesn't work correctly with unprocessed iterables like 'map()'
    orders_w_total_values = list(zip(discout_applied, value_w_no_shipping, strict=True))
    added_total = map(lambda order: add_total(order), orders_w_total_values)
    #print(list(added_total))
    processed_orders = list(map(lambda order: set_status(order, OrderStatus.PROCESSED), added_total))
    return (processed_orders, failed_orders)

def apply_discount(order):
    order_w_discount = order.copy()
    match order_w_discount["tier"]:
        case CustomerTier.BRONZE:
            return order_w_discount

        case CustomerTier.SILVER:
            discounted_list = order_w_discount["items"]
            new_list = list(map(lambda item: {"name": item["name"], "price": item["price"] * 0.95, "qty": item["qty"]}, discounted_list))            
            order_w_discount["items"] = new_list
            return order_w_discount

        case CustomerTier.GOLD:
            discounted_list = order_w_discount["items"]
            new_list = list(map(lambda item: {"name": item["name"], "price": item["price"] * 0.90, "qty": item["qty"]}, discounted_list))
            order_w_discount["items"] = new_list
            return order_w_discount

        case CustomerTier.PLATINUM:
            discounted_list = order_w_discount["items"]
            new_list = list(map(lambda item: {"name": item["name"], "price": item["price"] * 0.85, "qty": item["qty"]}, discounted_list))
            order_w_discount["items"] = new_list
            return order_w_discount

        case _:
            raise Exception("Unknown tier")

def add_total(order): # order is tuple ('order info' dict, 'total value of items' float)
    totaled_order = order[0].copy()
    totaled_order["total"] = order[1]
    return totaled_order

# shipping calculator closure that remembers shipping rates
# add shipping costs
# group orders by shipping method
# recursion for processing shipping groups
def ship_stage():
    shipping_rates = [
        {"order's total over": 0.0 ,"shipping cost": 10.0},
        {"order's total over": 200.0 ,"shipping cost": 5.0}
    ]

    def shipper(orders):
        shipping_orders = orders[0]
        failed_orders = orders[1]
        shipping_groups = [
            [], # express group
            []  # standard group
        ]
        shipping_groups[0] = list(filter(lambda order: order["total"] > 1000, shipping_orders))
        shipping_groups[1] = list(filter(lambda order: order not in shipping_groups[1], shipping_orders))
        processed_groups = process_shipping_groups(shipping_groups)
        pre_shipped_orders = processed_groups[0] + processed_groups[1]
        shipped_orders = list(map(lambda order: set_status(order, OrderStatus.SHIPPED), pre_shipped_orders))
        return (shipped_orders, failed_orders), shipping_groups

    def process_shipping_groups(group):
        processed_group = group.copy()
        if isinstance(processed_group, dict): # base case - "order info" dictionary was passed down
            order_total = group["total"]
            suggested_rates = list(filter(lambda rate: rate["order's total over"] < order_total,shipping_rates))
            shipping_cost = suggested_rates[len(suggested_rates)-1]["shipping cost"]
            processed_group["shipping cost"] = shipping_cost
            return processed_group
        else:
            processed_group = list(map(lambda group: process_shipping_groups(group), processed_group))
            #print(processed_group)
            return processed_group
    
    return shipper

# curried functions for different analytics
# calculate: total revenue, average order value, orders per tier
# use lambda functions for all calculations
# shipping stage function return values are: (,), [] - tuple and a list
def analytics_stage(orders): # tuple of all orders (processed, failed)
    def with_groups(shipping_groups): # list of groups [[], []], 'express' - 0, 'standard' - 1
        report = {
            "processed_orders": orders[0],
            "failed_orders": orders[1],
            "analytics": {
                "total_revenue": 0.0,
                "average_order": 0.0,
                "tier_breakdown": {}
            },
            "shipping_groups": {
                "express": shipping_groups[0] if len(shipping_groups[0]) != 0 else "No express orders",
                "standard": shipping_groups[1] if len(shipping_groups[1]) != 0 else "No standard orders"
            }
        }
        processed_orders = orders[0]
        total_revenue = sum(map(lambda order: order["total"], processed_orders)) # order_value_sum + sum(map('return all shipping costs')) all for processed_orders
        report["analytics"]["total_revenue"] = total_revenue
        average_order = total_revenue / len(processed_orders)
        report["analytics"]["average_order"] = average_order

        # creating supplementary lists to zip them together later
        tiers = [CustomerTier.BRONZE, CustomerTier.SILVER, CustomerTier.GOLD, CustomerTier.PLATINUM]
        tier_params = ["total_revenue", "average_order", "total_orders"]
        tier_breakdown = list(map(lambda tier: list(filter(lambda order: order["tier"] is tier, processed_orders)),CustomerTier))
        # here I zipped tier_params with values I got via using analyze_tier function on one of the orders
        # created dictionary from zipped data and mapped it to the list
        # then zipped list of tiers and list of dictionaries I got previously
        # finally I created dictionary from list of tuples I got from zipping
        orders_per_tier = dict(list(zip(tiers, list(map(lambda tier_values: dict(list(zip(tier_params, tier_values))), map(lambda tier: analyze_tier(tier), tier_breakdown))))))
        report["analytics"]["tier_breakdown"] = orders_per_tier
        # another helper function to reduce repetability          

        return report

    def analyze_tier(orders_of_tier):
        list_of_orders = orders_of_tier.copy()
        num_of_orders = len(list_of_orders)
        if num_of_orders == 0:
            return 0.0, 0.0, 0
        total_revenue = sum(map(lambda order: order["total"], list_of_orders))
        average_order = total_revenue / num_of_orders
        return total_revenue, average_order, num_of_orders

    return with_groups

main()