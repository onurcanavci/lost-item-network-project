def searchItemName(query, lost_items, find_items):
    if len(lost_items) != 0:
        for item in lost_items:
            if item not in find_items:
                itemName = lost_items[item]['item_name'].lower()
                if query in itemName:
                    print("Found item name: ", lost_items[item]["item_name"])
                    find_items[item] = lost_items[item]
    else:
        print("There isn't any lost item!")
    return find_items    

def searchDescription(query, find_items):
    deletedItemIds = []
    if len(find_items) != 0:
        for item in find_items:
            itemDescription = find_items[item]['description'].lower()
            if query in itemDescription:
                print("Found item description: ", find_items[item]["description"])
            else:
                deletedItemIds.append(item)
    for id in deletedItemIds:
        del find_items[id]
    return find_items
def searchLocation(query, find_items):
    deletedItemIds = []
    if len(find_items) != 0:
        for item in find_items:
            itemPlace = find_items[item]['place'].lower()
            if query in itemPlace:
                print("Found item location: ", find_items[item]["place"])
            else:
                deletedItemIds.append(item)
                print("query not found in location")
    for id in deletedItemIds:
        del find_items[id]
    return find_items



