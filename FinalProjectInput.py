# Student: Antonio Tagaylo
# Student Number: 1898186

import csv
from datetime import datetime

class InventoryItem:
    def __init__(self, item_id, manufacturer, item_type, price, service_date, damaged=False):
        self.item_id = item_id
        self.manufacturer = manufacturer
        self.item_type = item_type
        self.price = price
        self.service_date = service_date
        self.damaged = damaged

def read_csv(file_path):
    with open(file_path, mode='r') as file:
        return list(csv.reader(file))

def write_csv(file_path, data):
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

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

def create_full_inventory(items):
    sorted_items = sorted(items, key=lambda x: x.manufacturer)
    data = [
        [item.item_id, item.manufacturer, item.item_type, item.price, item.service_date.strftime("%m/%d/%Y"), "damaged" if item.damaged else ""]
        for item in sorted_items
    ]
    write_csv("FullInventory.csv", data)

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

def create_past_service_inventory(items):
    today = datetime.today()
    past_items = [item for item in items if item.service_date < today]
    sorted_items = sorted(past_items, key=lambda x: x.service_date)
    data = [
        [item.item_id, item.manufacturer, item.item_type, item.price, item.service_date.strftime("%m/%d/%Y"), "damaged" if item.damaged else ""]
        for item in sorted_items
    ]
    write_csv("PastServiceDateInventory.csv", data)

def create_damaged_inventory(items):
    damaged_items = [item for item in items if item.damaged]
    sorted_items = sorted(damaged_items, key=lambda x: x.price, reverse=True)
    data = [
        [item.item_id, item.manufacturer, item.item_type, item.price, item.service_date.strftime("%m/%d/%Y")]
        for item in sorted_items
    ]
    write_csv("DamagedInventory.csv", data)

# Paths to your CSV files
manufacturer_list = read_csv("ManufacturerList.csv")
price_list = read_csv("PriceList.csv")
service_date_list = read_csv("ServiceDateList.csv")

# Merge data
items = merge_data(manufacturer_list, price_list, service_date_list)

# Create output files
create_full_inventory(items)
create_type_inventories(items)
create_past_service_inventory(items)
create_damaged_inventory(items)