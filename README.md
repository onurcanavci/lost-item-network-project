# Lost Item Network Project

Lost item project is a project that shows lost items to Bogazici Members in same network. Found items are broadcasted via UDP with periodic synchronization packets. Synchronization happens in every 30 seconds.

## Why?

- Hard to find lost items in BOUN Campuses
- So many item holders (dorms, securities etc.)
- Students should access where their lost item is held.
- Found items and delivered items should be recorded i.e. legal purposes.

## To Watch Project Video

> https://www.youtube.com/watch?v=jC46nJLbR8s

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

To run in lost item holder role, write below script to in your terminal

```bash
python lost_item_holder.py
```

To run in the university student role, write below script to in your terminal

```bash
python user.py
```

## Usage

First the program ask name of user

`My student number:`

> 2017400000

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

> Kpark

`Name/type of lost item.`

> bag

`Brief description of lost item.`

> brown leather bag

Then it broadcast the lost items to users. They will view the items as below;

`Name: bag `

`Description: brown leather bag`

`Found at: Kpark`

`Found date: 21/12/2021`

`Now at: Kpark`

`ID of the item: 499631b0325df25a`

User lost item can be search the items with search command as below;

`search`

`Please enter your lost item name:`

> clock

`Found item name: [1:{name: bag....}]`

`Please enter your lost item description:`

> digital blue clock

`Found item description: [1:{name: bag....}]`

`Please enter your lost place name if you remember: `

> Kpark

`Name: clock `

`Description: digital blue clock`

`Found at: Kpark`

`Found date: 21/12/2021`

`Now at: Kpark`

`ID of the item: ad47d8d0325df25a`

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

`Name: cell phone `

`Description: iphone 11 pro max`

`Found at: Library`

`Found date: 29/12/2021`

`Now at: North Campus Security`

`ID of the item: ad421dwfg311f25a`
