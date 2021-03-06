# magic card game
# each player has a wizard with hitpoints
# the wizards battle against each other until only the sole survivor is victor
# each wizard gets some random cards from a stack, forming his card-deck
# (every wizard can only see his own card-deck)
# type of cards:
# direct-damage (like Flame Bolt), directly damages one enemy figure
# summoning: summons a monster that fights for the wizard
# buffs: improves friendly figures
# nerfs: nerfs enemy figures
# trading of cards:
# each wizard has the option to trade several cards against a unknown card of a higher level
# turns:
# planning phase:
# each player say the server (computer) witch card he wants to play
# execution phase:
# the computer calculates the result of all actions and displays the to the wizards
# Discord Text: https://www.writebots.com/discord-text-formatting/
# Bolded Text = **Example**  
# Italized Text = *Example*
# Underlined Text = __Example__
# You can combine the types of texts 


import random


class Game:
    monsternumber = 0
    time = 0


class Monster:

    def __init__(self):
        self.number = Game.monsternumber
        Game.monsternumber += 1
        self.hp = 100
        self.attack = "2d6"
        self.defense = "1d10"
        self.damage = "1d4"
        self.buffs = []
        # ----- resitances ------
        self.resist_fire = 0
        self.resist_cold = 0
        self.resist_poision = 0
        self.resist_electro = 0
        # ---- elemental damage ----
        self.damage_fire = 0
        self.damage_cold = 0
        self.damage_poision = 0
        self.damage_electro = 0
        # ---- other ---
        self.age = 0
        self.__post_init__()

    def __post_init__(self):
        pass

    def ai(self):
        pass


class Wizard(Monster):

    def __post_init__(self):
        self.hp = 150
        self.attack = "4d4"
        self.defense = "2d6"
        self.damage = "2d4"
        self.deck = []
        self.i = None
        self.army = [self]

    def show_deck(self):
        for index, card in enumerate(self.deck):
            print("index:", index, "card:", card)


class Minion(Monster):

    def __post_init__(self):
        self.hp = 50
        self.attack = "2d4"
        self.defense = "1d4"
        self.damage = "1d4"


class HellHound(Monster):

    def __post_init__(self):
        self.hp = 80
        self.attack = "1d20"
        self.defense = "1d6"
        self.damage = "3d4"
        self.resist_fire = 20
        self.resist_cold = -10
        self.damage_fire = 5


class Simon(Monster):

    def __post_init__(self):
        self.hp = 1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
        self.attack = "100D50"
        self.defense = "100D50"
        self.damage = "100D50"


class Maxi(Monster):

    def __post_init__(self):
        self.hp = "NICHT VORHANDEN"
        self.attack = "NICHT VORHANDEN"
        self.defense = "NICHT VORHANDEN"
        self.damage = "NICHT VORHANDEN"

        self.hp = 1
        self.attack = "1d1"
        self.defense = "1d1"
        self.damage = "1d1"


class Hornet(Monster):

    def __post_init__(self):
        self.hp = 40
        self.attack = "1d6"
        self.defense = "1d20"
        self.damage = "1d2"
        self.damage_poison = 10


class DirectDamage:

    def __init__(self):
        self.damage = 1
        self.victims = 1
        # ---- elemental damage ----
        self.damage_fire = 0
        self.damage_cold = 0
        self.damage_poision = 0
        self.damage_electro = 0
        self.__post_init__()

    def __post_init__(self):
        pass


class Thunderbolt(DirectDamage):

    def __post_init__(self):
        self.damage = "1d6"
        self.damage_electro = "4d6"


class Fireball(DirectDamage):

    def __post_init__(self):
        self.damage = "2d6"
        self.damage_fire = "2d6"
        self.victims = "1d3+2"


class PoisonCloud(DirectDamage):
    pass


class Dwarf(Monster):
    pass


class Card:
    cards = {
        0: Thunderbolt,
        25: Fireball,  # 46-25 = 20%
        46: PoisonCloud,  # 50-46 = 1%
        50: Hornet,
        65: Maxi,
        70: Simon,
        80: Minion,
        85: Dwarf,  # up-low = 90-85 = 5%
        90: HellHound,
    }

    def __init__(self):
        self.r = random.randint(1, 100)
        cardranks = Card.cards.keys()
        for x in range(100):
            if x <= self.r and x in cardranks:
                self.effect = Card.cards[x]
                self.lower_limit = x
            if x > self.r and x in cardranks:
                self.upper_limit = x
                break
        else:
            self.upper_limit = 100
        self.percentage = self.upper_limit - self.lower_limit

    def __repr__(self):
        return f"Level: {self.r:>2} | Effect: {self.effect.__name__:>20} | Probability: {self.percentage:>7.1f}%"


def dicethrow(dicestring="1d6+0"):
    if "+" in dicestring:
        fix = int(dicestring.split("+")[1])
        rest = dicestring.split("+")[0]
    else:
        fix = 0
        rest = dicestring
    if not "d" in rest.lower():
        raise ValueError("dicestring must have a 'd' like '1d6+2'")
    if "D" in dicestring:
        rerolling = True
    else:
        rerolling = False
    throws = int(rest.lower().split("d")[0])
    die = int(rest.lower().split("d")[1])
    # --- roll ---
    #print("rolling " + dicestring + ": ", end="")
    total = 0
    for number in range(throws):
        if rerolling:
            roll = reroll(die)
        else:
            roll = random.randint(1, die)
            #print(roll, end="")
        #print("+", end="")
        total += roll
    #print(fix, end="")
    #print("=", total + fix)
    return total + fix


def reroll(sides):
    """
    dicestring must have a capital D like '1D6'
    the part before the 'D' is number of dice
    the parte after 'D' is number of sides per die
    when a die rolls the highest number, it is counted as
    (sides -1) and rolls again (this can repeated theoretically endless)
    """
    total = 0
    roll = random.randint(1, sides)
    #print(roll, end="")
    if roll == sides:
        #print("-1+", end="")
        total += (sides - 1) + reroll(sides)
    else:
        total += roll
    return total


# -----

def main():
    players = []
    while True:
        c = input(f"Enter name of player{len(players)+1} >>> ")
        if c == "":
            break
        p = Wizard()
        p.name = c
        players.append(p)
    print("Each player gets 5 cards")
    for p in players:
        for _ in range(5):
            p.deck.append(Card())

    # ----- turns -----
    while True:
        for player in players:
            print(player.name, "Please choose your card")
            player.show_deck()
            try:
                i = int(input("Index? >>> "))
            except ValueError:
                print("Please enter an integer, NOT a string\n")
                continue
            player.i = i
            print(f"{player.name}'s choice is {player.deck[player.i].effect.__name__}.")
        print("battle")
        # ----- battle... ----
        for player in players:
            card = player.deck[player.i]
            print(f"Card-Type: {card.effect.__name__}")
            if Monster in card.effect.__bases__:
                player.army.append(card.effect())
                print(f"A {card.effect.__name__} joins the army of {player.name}!")
            elif DirectDamage in card.effect.__bases__:
                print(f"{player.name} uses his card {card.effect.__name__}!")
            print("----- Players -----")
            for p in players:
                print(f"Name: {p.name} | Index: {players.index(p)}")
            vic = input(f"Choose your victim by index, {player.name} >>> ")
        # ----- ...TO BATTLEEEEE!!! -----
        print("Calculating Battle Consequences...") # ;)
        for player in players:
            card = player.deck[player.i]
            victim = vic
            if DirectDamage in card.effect.__bases__:
                real_victim = random.choice(victim.army)
                effect = card.effect()
                damage = dicethrow(effect.damage)
                real_victim.hp -= damage
                print(f"{real_victim.__class__.__name__} of {victim.name}'s army suffers {damage} damage. ({real_victim.hp} left)")
            # ----- Army strikes back -----
            for monster in player.army:
                if monster == player:
                    continue
                real_victim = random.choice(victim.army)
                attack = dicethrow(monster.attack)
                defense = dicethrow(real_victim.defense)
                damage = dicethrow(monster.damage)

                print(f"{monster.__class__.__name__} of {player.name}'s army attacks {real_victim.__class__.__name__} of {victim.name}'s army.")
                if defense >= attack:
                    print("Attack fails :(")
                else:
                    real_victim.hp -= damage
                    print(f"{real_victim.__class__.__name__} of {victim.name}'s army suffers {damage} damage. ({real_victim.hp} left)")
        # ----- CLEANSING of the army -----
        for player in players:
            if player.hp <= 0:
                print("You are so bad at this game", player.name)
            player.army = [m for m in player.army if m.hp > 0]

if __name__ == "__main__":
    main()
    # for _ in range(10):
    #    print(Card())

# ---- testing ----
# dicethrow("3d6")
# dicethrow("4d4+2")
# for _ in range(20):
#    dicethrow("1d20")





