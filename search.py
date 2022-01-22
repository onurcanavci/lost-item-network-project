find_items = {}

def searchItemName(query, lost_items):
    if len(lost_items) != 0:
        for item in lost_items:
            if item not in find_items:
                itemName = lost_items[item]['item_name'].lower()
                if query in itemName:
                    print("Found item name: ", lost_items[item])
                    find_items[item] = lost_items[item]
    else:
        print("There isn't any lost item!")

def searchDescription(query):
    deletedItemIds = []
    if len(find_items) != 0:
        for item in find_items:
            itemDescription = find_items[item]['description'].lower()
            if query in itemDescription:
                print("Found item description: ", find_items[item])
            else:
                deletedItemIds.append(item)
    for id in deletedItemIds:
        del find_items[id]

def searchLocation(query):
    deletedItemIds = []
    if len(find_items) != 0:
        for item in find_items:
            itemPlace = find_items[item]['place'].lower()
            if query in itemPlace:
                print("Found item location: ", find_items[item])
            else:
                deletedItemIds.append(item)
                print("query not found in location")
    for id in deletedItemIds:
        del find_items[id]


lost_items = {}

lost_item1 = {}
lost_item1["date"] = 11/11/2011
lost_item1["name"] = "Ahmet"
lost_item1["place"] = "Kuzey Piramit"
lost_item1["item_name"] = "Kirmizi Saat"
lost_item1["description"] = "Kirmizi akıllı saat"
lost_item1["ID"] = 1
lost_items[lost_item1["ID"]] = lost_item1

lost_item2 = {}
lost_item2["date"] = 12/12/2011
lost_item2["name"] = "Mehmet"
lost_item2["place"] = "Kütüphane"
lost_item2["item_name"] = "Cep Telefonu"
lost_item2["description"] = "Beyaz Iphone 11 Pro Max"
lost_item2["ID"] = 2
lost_items[lost_item2["ID"]] = lost_item2

lost_item3 = {}
lost_item3["date"] = 11/12/2011
lost_item3["name"] = "Mert"
lost_item3["place"] = "Kuzey Kapı"
lost_item3["item_name"] = "Beyaz Saat"
lost_item3["description"] = "Deri beyaz saat"
lost_item3["ID"] = 3
lost_items[lost_item3["ID"]] = lost_item3

print(lost_items)

queryItemName = ""
queryDescription = ""
queryPlaceName = ""

print("Please enter your lost item name: ")
queryItemName = input();
searchItemName(queryItemName, lost_items)

if len(lost_items) !=0 and len(find_items) == 0:
    print("Item is not found in lost items!")

if len(find_items) != 0:
    print("Please enter your lost item description: ")
    queryDescription = input();
    searchDescription(queryDescription)
    if len(find_items) != 0:
        print("found items: ", find_items)
    else:
        print("Item is not found in lost items!")
        
if len(find_items) != 0:
    print("Please enter your lost place name if you remember: ")
    queryPlaceName = input();
    searchLocation(queryPlaceName)
    if len(find_items) != 0:
        print("found items: ", find_items)
    else:
        print("Item is not found in lost items!")

