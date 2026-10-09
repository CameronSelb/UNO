from logic import initilize_deck, hand_out_cards, shuffle_discard, do_action, next_turn, neater_terminal, draw_card, pick_play, find_win, computer
import random
import time
import os


card_face = ["0", "1", "2", "3", "4", "5", "6", "7" ,"8" ,"9", "draw 2", "skip", "reverse", "wild", "wild draw 4"]
colour = ["green", "red", "blue", "yellow"]
deck = []
discard = []


def uno():

    computer_yn = False
    played_card = True
    count = 0
    player_amount = 2
    player_turn = 0
    

    while True:
        num_player = input("Enter the Number of players. max is 8: ")
        if (num_player.isdigit() and  0 < int(num_player) < 9) is False:
            print("Enter number of players 1-8.")
            continue
        
        player_amount = int(num_player)
        if player_amount == 1:
            computer_yn = True
        break 
            
    initilize_deck(deck, colour, card_face)
    players_cards = hand_out_cards(deck, player_amount, computer_yn) 
    discard.append(deck.pop())
    
    play(players_cards, played_card, count, player_turn, computer_yn)

    
def play(player_decks, card_in_play, c_count_dis, turn, comp_player):
    global deck, discard
    while True:
        top_discard = discard[-1]
        playable_card = False
        
        #This code checks and makes sure the first card on the discard pile is not the wild draw 4
        if top_discard.face == "wild draw 4" and c_count_dis == 0:
            deck.append(discard[0])
            random.shuffle(deck)
            discard = []
            discard.append(deck.pop())
            return
        else:
            c_count_dis += 1

        
        #Checks if there are less then 4 cards left in the pickup pile, then shuffles discard if not
        if len(deck) < 4 and len(discard) > 1:
            deck, discard = shuffle_discard(deck, discard)
            
        current_players_deck = player_decks[turn]
        
        #Checks if the top card on the pile is an action card, and then does the action
        if top_discard.type == "action" and card_in_play is True:
            
            #If statement to make sure if first card is a +2 the 1st player will get +2
            if c_count_dis == 1 and top_discard.face == "draw 2":
                turn = 0

            #Print top card if its not a wild or wild draw 4   
            if top_discard.face not in ["wild", "wild draw 4"]:
                print(f"Top card:\n{top_discard.colour, top_discard.face}\n")

            card_in_play = do_action(top_discard, player_decks, deck, turn)

            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"Top card:\n{top_discard.colour, top_discard.face}\n")
            
            #If statement checks for wild card then stays on player who didnt play the card
            if top_discard.face == "wild":
               continue

            #Prints the action that happens to the player
            if top_discard.face == "wild draw 4":
                effect = "draws 4"
            elif top_discard.face == "draw 2":
                effect = "draws 2"
            elif top_discard.face == "skip":
                effect = "got skipped"
            elif top_discard.face == "reverse":
                effect = "got reversed"

            if comp_player is True and turn == len(player_decks) - 1:
                print (f"Computer {effect}")
            else:
                print(f"Player {turn + 1} {effect}.")

            time.sleep(3)

            turn = next_turn(player_decks, turn)
        
            if top_discard.face == "reverse" and len(player_decks)  > 2:
                turn = next_turn(player_decks, turn) 
            continue
        

        #Checks the current players deck to see if they have a playable cardprint("\nTOP CARD: ",(discard_deck[len(discard_deck) -1]).colour, (discard_deck[len(discard_deck) -1]).face, "\n")
        for c in current_players_deck:
            if c.colour == top_discard.colour or c.face == top_discard.face or c.colour == "black":
                playable_card = True

        count = neater_terminal(turn, current_players_deck, top_discard, comp_player, player_decks)
        
        #This code checks if the player has a card they can play.
        if playable_card is False:
            draw_card(1, current_players_deck, deck)
            if comp_player is True and turn == len(player_decks) - 1:
                print("\nComputer cannot play.")
            else:
                print(f"\nPlayer {turn + 1} cannot play.")
            pick_play(current_players_deck, top_discard, discard, turn, player_decks, comp_player)
            turn = next_turn(player_decks, turn)
            continue

        #Uses the computer if the conditions are met
        if comp_player is True and turn == len(player_decks) - 1:
            computer(current_players_deck, top_discard, discard, turn, player_decks)
            card_in_play = True
            if len(current_players_deck) != 0:
                turn = next_turn(player_decks, turn)
                continue

            find_win(turn, player_decks, comp_player)
            

        play_yn = input("\nWould you like to 'pickup' or 'play'?: ").lower()
        if play_yn not in ["play", "pickup"]:
            print("Enter either 'pickup' or 'play'!")
            time.sleep(1)
            continue

        if play_yn == "pickup":
            draw_card(1, current_players_deck, deck)
            pick_play(current_players_deck, top_discard, discard, turn, player_decks, comp_player)
            turn = next_turn(player_decks, turn)
            continue

        while True:

            card_selected = (input("Selected a card using the number infront e.g '1' or '2': "))

            #If statement to check if the card selected can be played
            if card_selected.isalpha() or int(card_selected) not in [x for x in range(count)]:
                print("Please enter a numbered card shown.")
                continue

            card_selected = int(card_selected) - 1
            current_card = current_players_deck[card_selected]

            #Checks if the card selected is playable
            if (current_card.face == top_discard.face or current_card.colour == top_discard.colour or current_card.colour == "black") is False:
                print("Please select a playable card.")
                continue
                
            #Uses the input to play the selected card 
            discard.append(current_players_deck[card_selected])
            del current_players_deck[card_selected]
            card_in_play = True
            c_count_dis += 1
            break
        
        
        #This is the win condition
        if len(current_players_deck) != 0:
            turn = next_turn(player_decks, turn)
            continue

        find_win(turn, player_decks, comp_player)

if __name__ == "__main__":
    uno()
