# Student: Antonio Tagaylo
# Student Number: 1898186

import csv
from datetime import datetime

# InventoryItem defines the item with attributes with ID, manufacturing details, type, price, service date, and damage status
class InventoryItem:
    def __init__(self, item_id, manufacturer, item_type, price, service_date, damaged=False):
        self.item_id = item_id
        self.manufacturer = manufacturer
        self.item_type = item_type
        self.price = price
        self.service_date = service_date
        self.damaged = damaged

# read_csv function reads contents of file specified by 'file_path' and return as a list of rows
def read_csv(file_path):
    with open(file_path, mode='r') as file:
        return list(csv.reader(file))
# write_csv function writes given list of rows to CSV file at specified 'file_path', overwriting file as neccesary 
def write_csv(file_path, data):
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)
# merge_data function combines information from three lists—`manufacturer_list`, `price_list`, and `service_date_list`—to create and update `InventoryItem` objects, then returns a collection of these items
def merge_data(manufacturer_list, price_list, service_date_list):
    items = {}
    
    for row in manufacturer_list:
        item_id = row[0]
        manufacturer = row[1].strip()
        item_type = row[2].strip()
        damaged = len(row) > 3 and row[3].strip().lower() == 'damaged'
        items[item_id] = InventoryItem(item_id, manufacturer, item_type, None, None, damaged)
    
    for row in price_list:
        item_id = row[0]
        if item_id in items:
            items[item_id].price = float(row[1].strip())
    
    for row in service_date_list:
        item_id = row[0]
        if item_id in items:
            items[item_id].service_date = datetime.strptime(row[1].strip(), "%m/%d/%Y")
    
    return items.values()
# create_full_inventory function sorts a list of `InventoryItem` objects by manufacturer, formats their details into rows, and writes these rows to a CSV file named "FullInventory.csv".
def create_full_inventory(items):
    sorted_items = sorted(items, key=lambda x: x.manufacturer)
    data = [
        [item.item_id, item.manufacturer, item.item_type, item.price, item.service_date.strftime("%m/%d/%Y"), "damaged" if item.damaged else ""]
        for item in sorted_items
    ]
    write_csv("FullInventory.csv", data)
# create_type_inventories function organizes a list of InventoryItem objects by their type, sorts the items within each type by their ID, and writes each type's data to a separate CSV file named after the item type.
def create_type_inventories(items):
    types = {}
    
    for item in items:
        if item.item_type not in types:
            types[item.item_type] = []
        types[item.item_type].append(item)
    
    for item_type, items in types.items():
        sorted_items = sorted(items, key=lambda x: x.item_id)
        data = [
            [item.item_id, item.manufacturer, item.price, item.service_date.strftime("%m/%d/%Y"), "damaged" if item.damaged else ""]
            for item in sorted_items
        ]
        write_csv(f"{item_type.capitalize()}Inventory.csv", data)
# create_past_service_inventory function generates a CSV file of items with service dates that are past today, sorted by the service date.
def create_past_service_inventory(items):
    today = datetime.today()
    past_items = [item for item in items if item.service_date < today]
    sorted_items = sorted(past_items, key=lambda x: x.service_date)
    data = [
        [item.item_id, item.manufacturer, item.item_type, item.price, item.service_date.strftime("%m/%d/%Y"), "damaged" if item.damaged else ""]
        for item in sorted_items
    ]
    write_csv("PastServiceDateInventory.csv", data)

# create_damaged_inventoryfunction creates a CSV file listing damaged items, sorted by price from highest to lowest.
def create_damaged_inventory(items):
    damaged_items = [item for item in items if item.damaged]
    sorted_items = sorted(damaged_items, key=lambda x: x.price, reverse=True)
    data = [
        [item.item_id, item.manufacturer, item.item_type, item.price, item.service_date.strftime("%m/%d/%Y")]
        for item in sorted_items
    ]
    write_csv("DamagedInventory.csv", data)

# The code reads data from three CSV files into corresponding lists.
manufacturer_list = read_csv("ManufacturerList.csv")
price_list = read_csv("PriceList.csv")
service_date_list = read_csv("ServiceDatesList.csv")

# Merges the corresponding data
items = merge_data(manufacturer_list, price_list, service_date_list)

# Creates the required output files
create_full_inventory(items)
create_type_inventories(items)
create_past_service_inventory(items)
create_damaged_inventory(items)