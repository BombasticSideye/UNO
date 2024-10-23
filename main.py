#To do list:
#Color codes.
#W and s menus.
#Classes.

import random
import os

colour = None
colours = ["Red", "Yellow", "Green", "Blue"]
action_commands = ["Reverse", "Draw", "Skip"]
skips = []

print("UNO in Python")
print("To begin, choose a ruleset (press enter for more details)")
while True:
    rulesets = {
        "Adapted": {
            "description": "The fun UNO game, with adapted rules made up such as: "
                           "Stacking Wild Draw 4s and Draw 2s is legal. "
                           "The first person to 0 cards wins. "
                           "Wild Draw 4s may be placed without sanction on your go.",
            "stacking": True
        },
        "Strict UNO": {
            "description": "This version of UNO uses all the official MATTEL rules. "
                           "You may not stack at all. "
                           "First person to 0 ends the game.",
            "stacking": False
        }
    }

    ruleset = rulesets[user_choice(rulesets)]

    # Display the description of the selected ruleset
    print(ruleset["description"])

    # Prompt the user for confirmation
    if input("Choose this? (Y/N): ").strip().title() == 'Y':
        stacking = ruleset["stacking"]
        break

# Selected ruleset
print(f"You selected: {ruleset}")

cl()

class distribution:
    def __init__(self):
        global deck, player_count

        while True:
            try:
                player_count = int(input("How many players do you want in the game? (2-4): "))
                if 2 <= player_count <= 10:
                    break
                else:
                    print("You need between 2 and 10 players!")
            except ValueError:
                print("That isn't a number.")

        base = random.randint(1, player_count)
        for _ in range(player_count):
            players[f"Player {base}"] = []
            base += 1
            if base > player_count:
                base = 1

        print("\nOrganising cards...\n")

        deck = []
        for color in colours:
            color_cards = {
                "color": color, "cards": [{0: 1}] + [{i: 2} for i in range(1, 10)]
            }
            for special in ["Skip", "Reverse", "Draw 2"]:
                color_cards["cards"].append({special: 2})
            deck.append(color_cards)

        wild_cards = {
            "color": "Wild", "cards": [{special: 4} for special in ["Card", "Draw 4"]]
        }
        deck.append(wild_cards)

        deck = self.flatten_deck(deck)
        random.shuffle(deck)  # Shuffle the deck
        self.deal(players, deck)


    def deal(self, players, deck):
        _players = list(players.keys())
        if random.choice(["Clockwise", "Anticlockwise"]) == "Anticlockwise":
            _players.reverse()

        for player in _players:
            players[player] = [[],{"Debt": 0}]

        for _ in range(7):
            for player in _players:
                players[player][0].append(deck.pop(0))


    def flatten_deck(self, deck):
        flatdeck = []
        for i in deck:
            for card in i['cards']:
                for value, count in card.items():
                    flatdeck.extend([f"{i['color']} {value}"] * count)
        return flatdeck



def shuffle(cards):
    global deck
    for i in range(400000):
        random.shuffle(cards)
    deck = cards


def action(card, player='pile'):
    global can_end, colour, deck, draw, pile, player_id, players, skips, turn
    colour = card.split()[0]
    if "Reverse" in card:
        players = dict(reversed(list(players.items())))
        can_end = True
        print("Uno Reverse!")
    elif "Draw" in card or "Wild" in card:
        if "Wild" in card and "4" not in card:
            while colour.title() not in colours:
                colour = input("Choose a card colour: ")
        if "Draw" in card:
            if "4" in card and player != 'pile':
                turn = "Ended"
                if stacking == True:
                    players[player][1]["Debt"] += 4
                else:
                    draw(4, player_id=player_id+1)
                return "Draw 4"
            elif '2' in card:
                if player == 'pile':
                    draw(2, player_id + 1)
                else:
                    print(players if isinstance(players, dict) else player)
                    print(players[player])
                    print(players[player][1])
                    print(players[player][1]["Debt"])
                    if stacking == True:
                        players[player][1]["Debt"] += 2
                    else:
                        draw(2, player_id=player_id+1)
                turn = "Ended"
                return "Draw 2"
            else:
                print("The deck may not play a Wild Draw 4. Shuffling...")
                deck.insert(random.randint(0, len(deck)-1), pile.pop(0))
                shuffle(deck)
                pile = [deck.pop(0)]
                print("Playing", pile[0])
                action(deck[-1])
    elif "Skip" in card:
          skips.append(player_id+1)
    elif "Pick Up" in card.title():
        draw(players[player][1]["Debt"] + 1)
        players[player][1] = {"Debt":0}
    elif "Deck" in card.title():
        print(deck)
    else:
        can_end = True


def draw( amount='1', player='def'):
    global turn, skip, player_id

    if player == 'def':
        drawing = player_id + 1
    else:
        drawing = str(player)

    for i in range(amount):
        players[drawing][0].append(deck.pop(0))
    turn = "Over"
    if player == 'deck':
        if player_id + 1 > player_count:
            skip.append(1)
        else:
            skip.append(player_id + 1)


def work(card, picked_up):
    global cards, colour, pile
    for i in range(1):
        try:
            card_choice = int(card)
        except Exception:
            card_choice = card
        if isinstance(card_choice, int):
            if card_choice < 1:
                print("Card ID must be greater than 0!")
                break
            else:
                try:
                    card_choice = cards[int(card)-1]
                except Exception:
                    print(f"Card out of card range (1,{len(cards)})")
        if card_choice in [" ", ""]:
            print("Enter something!")
            break
        elif card_choice.title() == "Deck":
            print(cards_display)
            break
        elif card_choice.title() == "Pick Up":
            if not picked_up:
                print("You have already played and cannot pick up!")
                break
            else:
                draw()
                break
        print(f"You are trying to play: {card_choice}")
        if input("Correct?").title() in ["Y","Yes", "OK", "Sure", "T", "True"]:
            if card_choice in cards:
                if validate(card_choice, colour, picked_up):
                    result = action(card_choice, players)
                    print(pile)
                    pile.append(players[player][0].remove(card_choice))
                    print(pile)
                    print(f"Action result: {result}")
                else:
                    print("Card invalid!:")
                    if 'Wild' in card.title():
                        print("Wild cards may not be played after you have picked up")
                    elif colour not in card.title():
                        print("Wrong colour, the colour is", colour)
            else:
                print("Invalid card choice. Try again.")


def validate(card, colour, picked_up) -> bool:
    if 'Wild' in card.title() and picked_up:
        return True
    elif 'Wild' in card.title():
            return False
    try:
        if card.split()[-1] == pile[-1].split()[-1]: # If the number is the same as the last
            return True
    except Exception:
        print(card)
        print(pile[-1])
        print(card.split())
        print(pile[-1].split())
        print(card.split()[-1])
        print(pile[-1].split()[-1])
    if card.split()[1] == "Skip" and pile[-1].split()[1]:
        return True
    elif colour in card.title() and card.split()[1] == "Skip":
        return True
    if colour in card.title(): # If the colour is the same
        return True
    if picked_up: # If you have picked up a card
        if cards[-1].split()[0] == pile[-1].split()[0] and card == cards[-1]: # If the last card you picked had the same colour as the one before and this is the one you're playing
            return True
    return False


def next_turn():
    global player, player_id
    player_id = (int(player.split()[-1]) % player_count) + 1
    player = f"Player {player_id}"


def display():
    global cards_display, cards
    print("Your cards:")
    cards = players[player][0]
    cards_display = ', '.join(cards[:-1]) + ' and ' + cards[-1] if len(cards) > 1 else cards[0] + '.'
    print(cards_display)


if __name__ == "__main__":
    players = {}
    distribution()
    starting = list(players.keys())[0]

    player = starting
    player_id = int(player.split()[1])
    print("Deck is playing:")
    pile = [deck.pop(0)]  # Draw from the top of the deck
    print(f"Deck played a {pile[0]}")

    print(f"{starting} is starting the game.")
    print()

    display()
    action(pile[0])
    print()

    while True:
        if player_id not in skips:
            turn = "Started"
            print(player)
            if starting is None:
                display()

            can_end = False

            while turn == "Started":
                if not can_end:
                    card_choice = input("Choose a card name, card number or deck or pick up: ")
                else:
                    card_choice = input("Choose a card name, card number or deck or end turn: ")
                    if card_choice.title() in ["End Turn", "End", "Finish", "Finish Turn"]:
                        if input("Are you sure? ").title() in ["Y","Yes", "OK", "Sure", "T", "True"]:
                            turn = "Ended"
                if turn != "Ended":
                    work(card_choice, not can_end)
    starting = None
    next_turn()
    if not deck:
        print("The deck is empty. The discard pile becomes the new deck.")
        deck = pile
        pile = []
        shuffle(deck)
