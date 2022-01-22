# Lost Item Network Project

Lost item project is a project that shows lost items to Bogazici Members in same network. Found items are broadcasted via UDP with periodic synchronization packets. Synchronization happens in every 30 seconds.

## Why?

- Hard to find lost items in BOUN Campuses
- So many item holders (dorms, securities etc.)
- Students should access where their lost item is held.
- Found items and delivered items should be recorded i.e. legal purposes.

## Get Repository

To clone project, write the below script to terminal in your folder address you want to clone

```bash
git clone https://github.com/onurcanavci/lost-item-network-project.git
```

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install thread library with following command.

```bash
pip install _thread
```

## Run

To run project, write below script to in your terminal

```bash
python workshop3.py
```

## Usage

First the program ask name of user

`My name:`

> Dogukan

Then it will ask the action as below

`What do you want to do? (chat, see_onlines, lost_item_broadcast, lost_items, approve_item, approval_message , found_items , delete_notification, exit):`

> see_onlines

It will prints the online users like below;

`Onur Can`

Then if user enters the lost_item_broadcast command, user should have to enter the lost item details to console as belows;

`When it was found? (dd/mm/yyyy`

> 01/20/2022

`Who found it? (name surname)`

> Dogukan Turksoy

`Where it was found?`

> In front of the New Hall

`Name/type of lost item.`

> Bag

`Brief description of lost item.`

> Brown leather bag.

Then it broadcast the lost items to users. They will view the items as below;

`[1:{name: asdasdas, adsad: dsadasd,}]`

User lost item can be search the items with search command as below;

`search`

`Please enter your lost item name:`

> Bag

`Found item name: [1:{name: bag....}]`

`Please enter your lost item description:`

> Brown leather bag

`Found item description: [1:{name: bag....}]`

`Please enter your lost place name if you remember: `

> New Hall

`found items: [1:{name: bag....}]`

If user find the lost item could not find the lost item, then the program will ask as below;

`Do you want to notified? (yes/no)`

> yes

`Please enter your lost item name: `

> cell phone

`Please enter your lost item description: `

> Iphone 11 Pro Max

`Please enter your lost place name if you remember: `

>

Then if the antother user add the new item like above, then the program will want to notify the user to show lost item. When the new item added to lost items, the program checks the notify items, is there any match. If there is a match from notify items, it will show the below message to user

`An item found: [1{name: apple ....}]`

## Functions

```python
# prints message in red color to console
def print_red(*message)
```

```python
# prints message in green color to console
def print_green(*message)
```

```python
# prints message in cyan color to console
def print_cyan(*message)
```

```python
# prints message in yellow color to console
def print_yellow(*message)
```

```python
# returns validated and parsed message
def validate_and_parse_json(message)
```

```python
# returns online users
def get_users()
```

```python
# returns IP address of a user
def get_user(name)
```

```python
# returns if a user with specified name exists
def check_user(name)
```

```python
# adds an user to specified IP address in the user array
def add_user(ip, name)
```

```python
# removes user from IP address, used when netcat can't connnect to an IP address
def remove_user(name)
```

```python
# connects with ip and port and send name and ip in encoded
def response_to_discovery(ip)
```

```python
# connects with user ip from get_user and port and send name and body in encoded
def send_message(receiver, message)
```

```python
# prints lost item approval
def result_approval(sender, ID,result)
```

```python
# prints lost item approve request
def send_approval(taker, ID):
```

```python
# prints message according to type of message
def handle_connection(conn):
```

```python
# listens the connection
def listen():
```

```python
# listens the message according to get message type
def listen_for_discovery():
```

```python
# broadcasts lost items with udp
def broadcast_lost_item (found_date, founder_name, found_place, lost_item_name, description, ID):
```

```python
# discovery with udp
def discover():
```

```python
# synchronizes lost items with users in 30 seconds
def synchronize():
```

```python
# synchronizes found items with users in 30 seconds
def synchronize_found_items():
```

```python
# broadcasts found items with udp
def broadcast_found_item(item):
```

```python
# main function
# it create socket connections
# creates a new thread and it gets the name of user
# creates new threads for listening discovery, discover, synchronize lost and found items
# finally the program ask the user which command wants to do
# after user choose the command, necessary actions run
try:
```
