#final project file 1
#basically an attempt build off of an old asignment. 
#these are for having random events or item placements, roles, writes lore and role descriptions to text files, an user inpt for name and role pick

import os
import random
import textwrap
from typing import List, Dict, Optional

#these are gonna be utilities and player/dev help
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def wrap(text, width= 72):
    return textwrap.fill(text, width=width)


class Item:
    def __init__(self, name:str,kind: str, power: int=0, description: str = ""):
        self.name=name
        self.kind = kind #this is like for weapons, armor, potions, etc
        self.power = power
        self.description = description 

    def __repr__(self):
        return f"{self.name} ({self.kind}, power={self.power})"
class Role:
    def __init__(self, key:str, display_name:str, hp:int, attack:int, defense:int, special:str):
        self.key = key
        self.display_name = display_name
        self.base_hp=hp
        self.base_attack=attack
        self.base_defense=defense
        self.special= special

    def describe(self):
        return f"{self.display_name}: hp {self.base_hp}, atk {self.base_attack}, def {self.base_defense} - special: {self.special}"
    
class Monster:
    def __init__(self, name:str, hp:int, attack:int, loot: Optional[List[Item]]= None):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.loot = loot or []

    def __repr__(self):
        return f"{self.name} (HP {self.hp}, ATK {self.attack})"
    
class Room:
    def __init__(self, id:int, name: str, descripton: str):
        self.id =id
        self.name=name
        self.description = descripton
        self.items: List[Item]= []
        self.monsters: List[Monster] = []
        self.exits: Dict[str, int] ={} #direction->room_id
    
    def __repr__(self):
        return f"Room({self.id}, {self.name})"
    

#these are the role definitions and descriptions

ROLES: Dict[str, Role] = {
    "necromancer": Role("necromancer", "Necromancer", hp =60, attack=8, defense=4,
                        special="raise a skeleton froma  fallen enemy (single ally)"),
    "barbarian": Role("barbarian", "Barbarian", hp=100, attack=14, defense=6,
                      special="Rage: increased attack for a single turn"),
    "rogue": Role("rogue", "Rogue", hp=75, attack=11, defense=5,
                  special='sneak: high chance to avoid first strike'), 
    "ranger": Role("ranger", "Ranger", hp = 80, attack=12, defense =5,
                   special= "pinpoint shot: chance of double damage at range"),
    "cleric": Role("cleric", "Cleric", hp= 85, attack=9, defense=7,
                   special= "Heal: can use mana to restore hp"),
}



#these generate the random items here and a list of items in the game
WEAPONS = [
    ("Rusty Dagger", 3), ("War Axe", 8), ("Short Sword", 6),
    ("Longbow", 7), ("Eldritch Staff", 9)
]

ARMORS = [
    ("Cloth Tunic", 1), ("Leather Aromr", 3), ("Chainmail", 6), ("Plate Vest", 8)
]

POTIONS = [
    ("Minor Healing Potion", 20), ("Major Healing Potion", 50),
    ("Stamina Draught", 0), ("antidote", 0)
]

ARTIFACTS = [
    ("Bone of Whispering", 0), ("Amulet of the Storm", 0), ("Shard of Eternity", 0)
]

def make_item_random() -> Item:
    #created a random item from weighted categories. 
    category = random.choices(
        ["weapon", "armor", "potion", "artifact"], 
        weights= [35, 25, 30, 10],
        k=1
    )[0]
    if category == "weapon":
        name, power = random.choice(WEAPONS)
        return Item(name, "weapon", power, description=f"A {name} that deals{power} base damage")
    if category == "armor":
        name, power = random.choice(ARMORS)
        return Item(name, "armor", power, description=f"Wearable {name} that grants {power} defense. ")
    if category == "potion":
        name, heal = random.choice(POTIONS)
        desc= "Heals HP" if heal >0 else "Grants temproary effect"
        return Item(name, "potion", heal,  description=f"{name}: {desc} ({heal}).")
    name,_=random.choice(ARTIFACTS)
    return Item(name, "artifact", power=0, description=f"a mysterious artifact called{name}.")


#these here are making the world and path needed to progress the game
def generate_rooms(n_rooms: int=9) -> Dict[int, Room]:
    rooms={}
    for i in range(n_rooms):
        room = Room(i, f"Chamber {i+1}", descripton=f"A dark, dusty chamber numbered {i+1}. ")
        rooms[i] = room
        #if it is possible connect the room as a 3x3 grid to have enough room but not too confusing to get lost in
        side = int(round(n_rooms ** 0.5))
        if side * side !=n_rooms:
            side = max(1,int(n_rooms ** 0.5))
        for i in range(n_rooms):
            r=room[i]
            row = i //side
            col = i%side
            #north south west and east
            if (row - 1)>=0:
                r.exits["north"] = (row - 1) * side+col
            if (row + 1) < side and (row+1) * side+ col <n_rooms:
                r.exits["south"] = (row+1)* side+col
            if (col - 1) >=0:
                r.exits["west"] = row* side+ (col-1)
            if (col + 1) < side and row *side +(col +1) <n_rooms:
                r.exits["east"] = row *side +(col + 1)
        #room descriptions for the adventure
        for i, r in rooms.items():
            r.description += " " +random.choice([
                "you walk in and reaks of rot", "scratches across the walls tell of past struggles", 
                "a chill breeze whispers", "you can feel the magic in this place but can't tell what kind"
            ])
        return rooms
def place_items_randomly(rooms: Dict[int, Room], n_items: int = 10):
    #this is the random item placement generator
    room_ids = list(rooms.keys())
    for _ in range(n_items):
        item = make_item_random()
        chosen = random.choice(room_ids)
        rooms[chosen].items.append(item)

def place_monsters_randomly(rooms: Dict[int, Room], n_monsters: int =6):
    monster_names = ["Goblin", "wight", "skeleton", "jar innards", "curseblade"]
    room_ids = list(rooms.keys())
    for _ in range(n_monsters):
        name= random.choice(monster_names)
        hp = random.randint(12, 35)
        attack = random.randint(3, 10)
        loot = [make_item_random() for _ in range(random.randint(0,2))]
        chosen = random.choice(room_ids)
        rooms[chosen].monsters.append(Monster(name, hp, attack, loot))

#lore file and role text writer

def write_lore_file(filename: str, rooms:dict[int, Room], nuggets: int =5):
    lines = []
    lines.append("---- LORE: The Castle Front ----\n")
    for i in range(nuggets):
        lines.append(random.choice([
            "long ago there where people in these halls, only corpses and monsters now", 
            "the warrior before me died, in their arms is an amulet full of memories", 
            "the gaurdsman's key is here but he isnt, his body is likely somewhere with another item"
            "a prophet once told me that the deep vault must never be opened for the wrath of evil strike down if so"

        ]))
    lines.append("\nROOM TEASERS\n")
    for r in rooms.values():
        lines.append(f"{r.name}: {textwrap.shorten(r.description, width=00)}\n")
        with open(filename, "w", encoding="utf-8") as f:
            r.writelines(lines)
        print(f"[saved lore to {filename}]")

def write_roles_file(filename: str, roles: Dict[str, Role]):
    #write role descriptions to a text file for the player to inspect later
    lines= ["---- ROLES ----\n"]
    for k, role in roles.items():
        lines.append(f"{role.describe()}\n")
    with open(filename, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print(f"[saved roles to {filename}]")


class Player:
    def __init__(self, name:str, role:Role, start_room: int=0):
        self.name = name
        self.role = role
        self.max_hp = role.base_hp
        self.hp = role.base_hp
        self.attack = role.base_attack
        self.defense = role.base_defense
        self.room = start_room
        self.inventory: List[Item]=[]
        self.skeletons: int=0 #this is not enemies but for the necromancer


    def status(self):
        inv = ", ".join(i.name for i in self.inventory) or "empty"
        return(f"{self.name} the {self.role.display_name}  | HP: {self.hp}/{self.max_hp} | "
               f"ATK: {self.attack} | DEF:{self.defense} | Inventory: {inv}")
    

    def pick_item(self, item: Item):
        self.inventory.append(item)
        #auto equip and simple improvement
        if item.kind == "weapon":
            self.attack += item.power
            print(f"You equipped {item.name}. Attack increased by {item.power}. ")
        elif item.kind == "armor":
            self.defense += item.power
            print(f"you wore {item.name}. Defense increased by {item.power}. ")
        elif item.kind == "potion":
            print(f"You stowed away a {item.name} in your pocket. ")
        else:
            print(f"You pocket the {item.name} - it feels strange. ")

    def use_potion(self, potion_name: str):
        for i, it in enumerate(self.inventory):
            if it.kind == "potion" and potion_name.lower() in it.name.lower():
                heal =it.power
                if heal >0:
                    self.hp = min(self.max_hp, self.hp + heal)
                    print(F"you used {it.name} and healed {heal} HP. ")
                else:
                    print(f"You used {it.name} but nothing obvious happend. ")
                del self.inventory[i]
                return True
            print("no such potion in inventory.")
            return False

#combat and interactions
def combat(player: Player, monster: Monster) -> bool:
    #this is going to be a simple turn based combat because of the text game
    print(f"A {monster.name} appeared and it is ravenous (HP {monster.hp}, ATK {monster.attack})")
    while monster.hp >0 and player.hp >0:
        #this is the players turn first
        action = input("Choose action[attack/use potion/run]: ").strip().lower()
        if action == "attack":
            damage = max(0, player.attack - random.randint(0, monster.attack //2))
            monster.hp -= damage
            print(f"You strike the {monster.name} for {damage} damage (monster HP {max(0, monster.hp)})")
        elif action.startswith("use"):
            #using a potion
            parts = action.split(maxsplit=1)
            if len(parts) == 2:
                player.use_potion(parts[1])
            else:
                name = input("which potion name? ")
                player.use_potion(name)
        elif action == "run":
            if random.random() < 0.5:
                print("You slip away from the angry creature")
                return True
            else:
                print("you fail to escape")
        else:
            print("Invalid action. Try attack/use/run. ")
        #this is the monsters turn if its still alive
        if monster.hp >0:
            m_damage = max(0, monster.attack - random.randint(0, player.defense))
            player.hp -= m_damage
            print(f"The {monster.name} hits you for {m_damage} damage (your HP {max(0, player.hp)}. )")
    if player.hp > 0:
        print(f"You defeated the {monster.name}!")
        #loot drop
        if monster.loot:
            print("it dropped:")
            for it in monster.loot:
                print(" -", it)
                player.pick_item(it)
        #necromancer raise skeleton chance
        if player.role.key == "necromancer" and random.random() <0.5:
            player.skeletons +=1
            print("you raise a skeleton to fight along with you from the fallen corpse")
        return True
    else:
        print("you have been slain... You Died.")
        return False
    
#game loop
def describe_room(room: Room):
    print(f"\n == {room.name} == ")
    print(textwrap.fill(room.description, width =80))
    if room.items:
        print("You see the following items:")
        for i, it in enumerate(room.items, start=1):
            print(f"  [{i}] {it.name} - {it.description}")
    if room.monsters:
        print("Monsters present: ")
        for m in room.monsters:
            print(f"  - {m}")

    if room.exits:
        print("exits:", ", ".join(room.exits.keys()))
    else:
        print("There are no obvious exits. ")

def apply_room_encounters(player: Player, room:Room) -> bool:
    #this resolves monsters in the room. return True if continue playing, false if player dies
    while room.monsters:
        monster = room.monsters.pop(0)
        #if necromancer has skeletons, they fight first
        if player.role.key == "necromancer" and player.skeletons >0:
            print(f"Your skeleton minion attacks the {monster.name}, dealing a little damage. ")
            monster.hp -= 5
            player.skeletons -=1
            if monster.hp <=0:
                print(f"the skelton crushed the {monster.name}!")
                if monster.loot:
                    for lt in monster.loot:
                        player.pick_item(lt)
                continue
        survived = combat(player, monster)
        if not survived:
            return False
    return True

def move_player(player: Player, rooms:Dict[int, Room], direction:str):
    current = rooms[player.room]
    if direction not in current.exits:
        print("You can't go that way.")
        return
    player.room = current.exits[direction]
    print(f"You move {direction} to {rooms[player.room].name}. ")

def save_game(player: Player, rooms: Dict[int,Room], filename: str = "savegame.txt"):
    lines=[]
    lines.append(f"player|{player.name}|{player.role.key}|{player.hp}|{player.room}\n")
    for it in player.inventory:
        lines.append(f"inv|{it.name}|{it.kind}|{it.power}\n")
    #this is an optional save room function item count and monster description
    with open(filename, "w", encoding= "utf-8") as f:
        f.writelines(lines)
    print(f"[game saved to {filename}]")

#now we need a funtion to load the game again
def load_game(filename: str = "savegame.txt") -> Optional[Dict]:
    if not os.path.exists(filename):
        print("No save file found")
        return None
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
    data = {"player": None, "inventory": []}
    for ln in lines:
        parts = ln.strip().split("|")
        if parts[0] == "player":
            _, name, role_key, hp_key, hp_str, room_str =parts
            role = ROLES.get(role_key, list(ROLES.values())[0])
            p = Player(name, role, start_room=int(room_str))
            p.hp = int(hp_str)
            data["player"] =p
        elif parts[0] == "inv":
            _, name, kind, power = parts
            data["inventory"].append(Item(name, kind, int(power)))
    return data

def choose_role_prompt() -> Role:
    print("choose a role:")
    for key, role in ROLES.items():
        print(f" - {role.display_name} ({key}): HP {role.base_hp}, ATk {role.base_attack}, DEF {role.base_defense}")
        print(f"   Special: {role.special}")
    while True:
        choice =input("Enter role key (e.g., necromancer) or 'list' to see roles again. ").srtip().lower()
        if choice == "list":
            for k,r in ROLES.items():
                print(r.describe())
        elif choice in ROLES:
            return ROLES[choice]
        else:
            print("Invalid role. try again. ")

def show_help():
    print("""
          Available commands:
          look            - describe current room
          go <dir>        - move(north, south, east, west)
          take <num|name> - pick up an item in the room by number or name
          inv             - show inventory
          use <potion>    - use a potion from inventory by name
          save            - save game
          help            - show this help
          quit            - quit game
""".strip())
    
def main():
    print("Welcome to The Caslte Morne- A procedural text adventure. ")
    #optional load
    if os.path.exists("savegame.txt"):
        if input("Load previous save? (y/n): ").strip().lower() == "y":
            data = load_game("savegame.txt")
            if data and data["player"]:
                player = data["player"]
                for it in data:
                    player.inventory.append(it)
                #regenerate rooms
                rooms= generate_rooms()
                place_items_randomly(rooms, n_monsters=5)
                print(f"Loaded player {player.name}")
            else:
                print("starting new game instead. ")
                player = None
        else:
            player=None
    else:
        player=None

    if player is None:
        name= input("enter your name: ").strip() or "Wanderer"
        role = choose_role_prompt()
        player = Player(name, role, start_room=0)

    rooms = generate_rooms(n_rooms=9)
    place_items_randomly(rooms, n_items=12)
    place_monsters_randomly(rooms, n_monsters=6)

    #Write lore files and role files
    write_lore_file("lore.txt", rooms)
    write_roles_file("roles.txt", ROLES)

    print("\nGame Start!")
    show_help()
    playing = True
    while playing:
        current_room = rooms[player.room]
        print("\n" + "-"*40)
        print(player.status())
        describe_room(current_room)
        #handle immeadiate enemies in the room
        cont= apply_room_encounters(player, current_room)
        if not cont:
            print("You Died.")
            break

        cmd= input("\n> ").strip()
        if not cmd:
            continue
        parts= cmd.split(maxsplit = 1)
        verb = parts[0].lower()
        arg = parts[1] if len(parts)>1 else""


        if verb == "help":
            show_help()
        elif verb == "look":
            describe_room(current_room)
        elif verb == "take":
            if not arg:
                print("Take what? number or name required. ")
                continue
            #try a number
            taken= False
            if arg.isdigit():
                idx= int(arg) - 1
                if 0 <= idx < len(current_room.items):
                    item = current_room.items.pop(idx)
                    player.pick_item(item)
                    taken= True
            else:
                #by name
                for i, it in enumerate(current_room.items):
                    if arg.lower() in it.name.lower():
                        item = current_room.items.pop(i)
                        player.pick_item(item)
                        taken=True
                        break
            if not taken:
                print("No item to take. ")
        elif verb == "inv":
            print("Inventory:")
            for it in player.inventory:
                print(" -", it)
        elif verb == "use":
            if arg:
                player.use_potion(arg)
            else:
                name= input("Which potion name? ")
                player.use_potion(arg)
        elif verb == "save":
            save_game(player, rooms)
        elif verb == "quit":
            if input("are you sure you want to quit? (y/n): ").strip().lower() == "y":
                print("intill next time. ")
                playing = False
        else:
            print("Unknown command. Type 'help' for commands")
if __name__ == "__main__":
    main()