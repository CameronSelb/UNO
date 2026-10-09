import random
import os
import time

direction = 1

class UNO_DECK():
    def __init__(self, colour, face, card_type):
        self.colour = colour
        self.face = face
        self.type = card_type


def initilize_deck(d, col, c_face):
   #This function is used to initilize and create the108 uno cards
    for face in c_face:
        if face in ["0", "wild", "wild draw 4"]:
            d.extend([UNO_DECK(colour, face, "classic") for colour in col if face == "0"])
            d.extend([UNO_DECK("black", face, "action") for _ in range(4) if face in ["wild", "wild draw 4"]])
        
        else:
            d.extend([UNO_DECK(colour, face, "action") for colour in col if face in ["draw 2", "skip", "reverse"]] *2)
            d.extend([UNO_DECK(colour, face, "classic") for colour in col if face not in ["draw 2", "skip", "reverse"]] *2)
    
    random.shuffle(d)
    
def hand_out_cards(d, amount_player, computer):
    #Function used to create a hand for the computer and the user
    hands = []
    computer_hand = []

    if computer is True:
        while len(computer_hand) < 7:
            computer_hand.append(d.pop())
        hands.append(computer_hand)

    for _ in range(amount_player):
        hands.append([d.pop() for _ in range(7)])
   
    return hands


def change_colour(card):

    colour_dict = {"r" : "red", "g" : "green", "b" : "blue", "y" : "yellow"}

    while card.colour == "black":
        colour_change = input("Pick a colour to change to ('r'/'g'/'b'/'y'): ").lower()

        if colour_change  not in ["r", "g", "b", "y"]:
            print("Enter a valid colour.")
            continue
        
        card.colour = colour_dict[colour_change] 


def do_action(card, player_decks, game_deck, turn):

    global direction
    #Function used to check the type of action card and do that action
    face = card.face
    
    if face not in ["wild", "wild draw 4"]:
        if face == "draw 2":
            draw_card(2, player_decks[turn], game_deck)
    
        if len(player_decks) > 2 and face == "reverse":  
            if direction == 1:
                direction = -1
            else:
                direction = 1
        return False

    change_colour(card)

    if face == "wild draw 4":
        draw_card(4, player_decks[turn], game_deck)

    return False


def next_turn(p_decks, turn):
    #this function is to change to the next players turn
    turn += direction
    #Checks that the player turn is within the index of player_decks
    if turn > len(p_decks) - 1:
        turn -= len(p_decks) 
    elif turn < 0:
        turn += len(p_decks)

    return turn


def draw_card(amount, player, game_deck):
    #Function used to draw cards
    for _ in range(amount):
        player.append(game_deck.pop())


def shuffle_discard(deck, discard_deck):
    
    #Changes all wild card colour back to black
    for card in discard_deck:
        if card.face in ["wild", "wild draw 4"]:
            card.colour = "black"

    top_card = discard_deck.pop()
    deck.extend([discard_deck.pop() for _ in range(len(discard_deck))])
    discard_deck.append(top_card)
    
    random.shuffle(deck)


    return deck, discard_deck  


def neater_terminal(turn, deck, top, computer_player, player_hands):
    
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"Top card:\n{top.colour, top.face}\n")
    if computer_player is True and turn == len(player_hands) - 1:
        print("Computers turn")
    else:
        print(f"Player {turn + 1}'s turn")
    
    count = 1
    for card in deck:
        print(f"{count}: {card.colour} {card.face}")
        count += 1
    
    return count


def pick_play(deck, top, dis_pile, turn, player_hands, computer_player):
    
    card_pick_up = deck[len(deck) -1]
    
    if computer_player is True and turn == len(player_hands) - 1:
        print(f"Computer picked up a {card_pick_up.colour} {card_pick_up.face}.")
        comp_change_colour(card_pick_up, deck)
        y_n = "y"
    else:
        print(f"Player {turn + 1} picked up a {card_pick_up.colour} {card_pick_up.face}.")
    time.sleep(2)

    if not(card_pick_up.colour == top.colour) and not(card_pick_up.face == top.face) and not(card_pick_up.colour == "black"):
        return
    

    while not(computer_player is True and turn == len(player_hands) - 1):
        y_n = input("Would you like to play the card you picked up y/n: ").lower()
        if y_n not in ["y", "n"]:
            print("Enter either 'y' (yes) or 'n' (no)")
            continue
        break
    

    if card_pick_up.colour == "black" and y_n == "y":
        change_colour(card_pick_up)

    if y_n == "y":
        dis_pile.append(deck.pop())


#Used to let the computer randomly change colour
def comp_change_colour(card, hand):
    if card.colour == "black":

        colour_list = [c for c in hand if c.colour != "black"]
        card_colour_change = random.choice(colour_list)
        colour = card_colour_change.colour
        card.colour = colour

          
def computer(hand, top, discard_pile, turn, player_hands):
    neater_terminal(turn, hand, top, True, player_hands)
    while True:
        card = random.choice(hand)

        if (card.face == top.face or card.colour == top.colour or card.colour == "black") is False:
            continue
        
        print(f"\nComputer played: {card.colour} {card.face}")
        comp_change_colour(card, hand)
        time.sleep(3)

        discard_pile.append(card)
        hand.remove(card)
        break


def find_win(turn, player_hands, computer_player):
    if computer_player is True and turn == len(player_hands) - 1:
        print("Computer WINS!!")
    else:
        print(f"Player {turn + 1} WINS!!")
    
    exit()
