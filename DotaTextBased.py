import os
import sys

#Aakash Shrestha | 1151009 
#This is a text adventure game based on computer game dota2. 
#Players can choose heroes with three different attributes
#Each hero has a unique ability which lets them have a unique item by default
#Players will choose a hero, explore the map, and have 50 gold to spend
#Find, Buy and Sell items 
#Five items are needed to kill the boss
#Each item is unique
#Extra items are also found 
#Every item will deduct gold from the initial gold player had
#Whenever a player sell an item it is sold by 2/3 of initial cost
#Finally the bought items should be matched with the item to kill ROSHAN
#If not the ROSHAN will claim their soul
#If the ROSHAN is killed, player name will be inscribed as ROSHAN slayer
#Players can see the scoreboard to see the names of the ROSHAN slayers

###############################################
#items to slay roshan
kill_roshan = ["basher","boots","khukuri","salve","vanguard"]

#cost of items
courier = {
    "boots":10,
    "vanguard":10,
    "salve":10,
    "khukuri":10,
    "basher":10,

    "divine":30,
    "shadow blade":30,
    "butterfly":15,
    "crystalys":15
}

#heroes to choose
heroes = {"axe" :["you have vanguard and 50 gold to spend"],
          "sniper":["you have boots and 50 gold to spend"],
          "invoker":["you have salve and 50 gold to spend"]
}

#inventory of the player
bagpack = {"item":[],"gold":50}

#map of the game
direction = {"fountain":{"east":"river",\
                        "describe":"\n You are summoned into the fountain \
                        \n go east to reach river",\
                        "items":["boots"]
                        },
            "river":{"east":"jungle",\
                    "west":"fountain",\
                    "north":"sideShop",\
                    "describe":"\n You are at the river \
                    \n go east to reach jungle \
                    \n go west to get back to the fountain \
                    \n go north to find a side shop \
                    \n there is a vast river in the south",\
                    "items":["salve","crystalys","butterfly"]
                    },
            "sideShop":{"south":"river",\
                        "describe":"\n You are at the side shop\
                        \n It seems the only way you can go is south back to the river",\
                        "items":["vanguard"]
                        },
            "jungle":{"east":"roshanPit",\
                    "west":"river",\
                    "south":"secretShop",\
                    "describe":"\n You are at the jungle\
                    \n You can go east to reach the ROSHAN pit\
                    \n You can reach river in the west \
                    \n You can find a secret shop in the south\
                    \n There is a vast jungle in the north",\
                    "items":["khukuri","basher"]    
                    },
            "secretShop":{"north":"jungle",
                        "describe":"\n You are at the secret shop\
                        \n you can go north to reach the jungle\
                        \n other directions are blocked by mountains",\
                        "items":["divine","shadow blade"]
                        },
            "roshanPit":{"describe":"\nYou have finally reached the pit of the mighty ROSHAN",\
                        "west":"jungle",\
                        "items":[]
            }
}

#compass to change direction
compass = ["north", "east", "west", "south"]
#default location of the player
current_lane = direction["fountain"]

###############################################
'''Description of the game'''
def description():
    print("Hello! Welcome to mini dota2 text game."\
        "\nYou are allowed to choose one from three heroes with different attributes"\
        "\nStrength, Agility and Intelligence"\
        "\nYou can carry five items with you before you take on the mighty ROSHAN"\
        "\nCombination of five items is needed to slay the ROSHAN"\
        "\nSearch along the map to buy those items"\
        "\nYou have 50 gold to purchase the items"\
        "\nSpend the money wisely, not every item can kill the mighty ROSHAN"\
        "\nYou will need enough speed, armor, damage, healing power and stun to slay the beast"\
        "\nYou can use the following steps."\
        "\ngo to move east, west, north or south"\
        "\nbuy to take items"\
        "\nsell to drop items"\
        "\ninventory to check your bagpack"\
        "\nlocation to know your location"\
        "\nquit to end the game"\
        "\nscore to see the ROSHAN slayers")
    response = input("Do you want to start the game? y for yes | n for no :").lower().strip()      #user input to start the game
    if response == "y":
        hero()
    elif response =="n":
        print("come play next time")
        sys.exit()
    else:
        print("wrong input")
        description()                   #restarting the introduction

###############################################
'''Location of the map'''
def move(map):
    global current_lane
    if map in compass:
        if map in current_lane:
            current_lane = direction[current_lane[map]]
            print(current_lane["describe"])
            print("You can buy: {}".format(", ".join(current_lane["items"])))
            if current_lane == direction["roshanPit"]:
                roshan() 
        else:
            print("There is no way in that direction")
                
    else:
        print("There is no way in that direction")

###############################################
'''This function is trigerred when player is in roshanPit'''        
def roshan():
    global current_lane
    global bagpack
    fight = input("Do you want to fight roshan. y for yes n for no:  ").lower()     #input to fight
    if fight == "y":
        fails = False
        for each in kill_roshan:
            if each not in bagpack["item"]:                                         #if the item is not enough to kill ROSHAN
                print("You have been owned by ROSHAN"\
                "\n You are not strong enough. Try using better items")
                current_lane = direction["fountain"]
                print(current_lane["describe"])
                print("You can buy: {}".format(", ".join(current_lane["items"])))
                fails = True
                break
        if not fails:                                                               #if the item is enough to kill ROSHAN
            print("You have slayed the ROSHAN")                                     #ROSHAN is killed
            if os.path.isfile("slayers.txt"):                                       #checking to see if the slayers.txt is in the folder
                writefile = open("slayers.txt", "a")                                #writing new slayer name
            else:
                writefile = open("slayers.txt", "w")                                #opening new slayer scoreboard
            toslayer = input ("What is you name ROSHAN slayer? :")                  #input for player name
            writefile.write("\n" + toslayer)
            writefile.close()                                                       #closing the read write function
            print("Your name has been inscribed as a ROSHAN slayer")
            sys.exit()
    elif fight == "n": 
        print("you can come back later")
        current_lane = direction["jungle"]
    else:
        print("invalid input")
        current_lane = direction["jungle"]

###############################################
'''This function is used to buy the item from the location and carry it in bagpack'''
def buying(bought):
    global current_lane
    global gold
    if bought in current_lane["items"] and bagpack["gold"] < courier[bought]:   #if player's gold is less than the cost of item
        print(f"you do not have enough gold to purchase {bought}")      #print no enough gold
    elif bought in current_lane["items"]:           #if player have enough gold and item in the location
        print(f"You have bought {bought} from the location")
        current_lane["items"].remove(bought)
        bagpack["item"].append(bought)                  #adding item to the bagpack
        bagpack["gold"] -= courier[bought]              #deducting gold from bagpack
        print("You can buy: {}".format(", ".join(current_lane["items"])))  

    else:
        print("this item is not here")

'''This function is used to sell the item from the bag and drop in the location'''       
def selling(sold):
    if sold in bagpack["item"]:
        bagpack["item"].remove(sold)
        current_lane["items"].append(sold)
        print(f"you have sold the {sold}.")
        bagpack["gold"] += 2/3 * courier[sold]          #selling the item in 2/3 of the original price
    else:
        print("this item is not here")

'''This function is used to describe the items that are stored in the inventory list'''
def describe_inventory():   
    print("You have {} gold".format(bagpack["gold"]))                           
    print ( "You are currently carrying these items: ")
    for i in bagpack["item"]:
        print(i)       

'''This function is used to choose hero and adding the hero ability in the bagpack'''
def hero():
    hero = input("Choose your hero from AXE | SNIPER | INVOKER : ").lower().strip()
    if hero == "axe":
       print("You picked axe. {}".format(" ".join(heroes["axe"])))      #if hero axe is picked
       bagpack["item"].append("vanguard")                               #adding vanguard to increase strength
       main()
    elif hero == "sniper":
        print("You picked sniper. {}".format(" ".join(heroes["sniper"])))   #if hero sniper is picked
        bagpack["item"].append("boots")                                     #adding boots to increase agility
        main()

    elif hero == "invoker":
        print("You picked invoker. {}".format(" ".join(heroes["invoker"])))    #if hero invoker is picked
        bagpack["item"].append("salve")                                        #adding salve to increase healing
        main()
    else:
        print("wrong input")                    #invalid hero

'''This function is used to quit the game'''
def quit():
    print("You ran in fear of the mighty ROSHAN")
    sys.exit() 

'''This function is used to check the slayers'''
def score():
    if os.path.isfile("slayers.txt"):   #checking if file exists in the location
        workfile = open("slayers.txt", "r")
        slayers = workfile.read()
        print(slayers)
        workfile.close() 
    else:
        print("There has not been any ROSHAN slayers born yet.")

################################################
'''Function to call the user inputs'''
def main():
    print(current_lane["describe"])
    print("You can buy: {}".format(", ".join(current_lane["items"])))
    while True:         #keeping the game on
        step = input(" Enter your next step: ").lower().split()     #changing user input to lowercase and to avoid whitespace
        step = " ".join(step)           #joing the input
        if step.startswith("go "):          #to move player to other direction  
            where = step[3:]
            move(where)
        elif step.startswith ("buy "):      #to take item from location
            bought = step[4:]
            buying(bought)
        elif step.startswith("sell "):      #to drop item to the location
            sold = step[5:]
            selling(sold) 
        elif step == "inventory":           #to check the inventory
            describe_inventory()
        elif step == "location":            #to check the locatio nof player
            print(current_lane["describe"])     
            print("You can buy: {}".format(", ".join(current_lane["items"])))
        elif step == "quit":                #to quit the game
            quit()
        elif step == "score":               #to check the names of the ROSHAN slayers
            score()
        else:
            print("wrong step!!! please use | go | buy | sell | inventory | location | quit | score | commands")
                
if __name__=="__main__":    #the main function
    description()           #starting function