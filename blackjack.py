import cards
import random

# function definitions
def shuffled_deck():
    """
    Creates a shuffled deck of cards.
    """
    d = cards.deck()
    random.shuffle(d)
    return d 


def count_points(some_hand):
    """
    Calculates points in a hand.
    """
    points = 0
    aces = 0 # keeps tracks of aces in points calculation
    
    for cards in some_hand:
        if cards.rank() in ["J", "Q", "K", "T"]:
            points = points + 10
        elif cards.rank() == "A":
            aces = aces + 1 # adds ace to counter
            points = points + 11
        else:
            points = points + int(cards.rank())
    
    while points > 21 and aces > 0: # if points is greater than 21, aces will count for 1 
        points = points - 10 # changes aces's value to 1
        aces = aces - 1 # resets ace counter for next ace drawn
    
    return points 

def ask_for_bets(num_players):
    """
    Asks user(s) how much they want to bet and and appends to list of bets in current turn.
    """
    all_bets = [] # master list of all bets in turn 
    for player in range(num_players):
        print("Player #" + str(player+1) + "\n" + "You have $" +str(player_balance[player]) + ".")
        bet = int(input("How much do you want to bet? "))
        
        while True: # valid bets loop
            
            if bet < 1: # re-enter bet if it's less than 1
                print("Player #" + str(player+1) + "\n" + "You have $" +str(player_balance[player]) + ".")
                bet = int(input("How much do you want to bet? "))
            elif bet > player_balance[player]: # re-enter bet if it's greater than balance
                print("Player #" + str(player+1) + "\n" + "You have $" +str(player_balance[player]) + ".")
                bet = int(input("How much do you want to bet? "))
            else:
                all_bets.append(bet) # apppends valid bets 
                break
    
    return all_bets


def initial_hands(num_players):
    """
    Deals the cards to user(s) hand and dealer's hand at the beginning of each round and returns dealer's and player(s) initial hands.
    """
    all_hands = []
    
    for player in range(num_players):
        hand = [deck.pop(), deck.pop()] # each player starts with two cards
        all_hands.append(hand) # is a list in which every element is a pair of cards

    dealer_hand = [deck.pop(), deck.pop()] # also starts with two cards

    return dealer_hand, all_hands


def display_initial_hands(dealer_hand, all_hands):
    """
    Displays dealer's and player(s) initial hands.
    """
    print("Hands:")
    print("  Dealer:    " + "**" + " " + str(dealer_hand[1])) 
    for player, hand in enumerate(all_hands): # loops through each player's hand and displays them
        print("  Player #" + str(player+1) + ": " + cards.hand_display(hand))


def players_turn(all_hands):
    """
    Loop through the player's turn.
    """
    for player, hand in enumerate(all_hands): # Goes through each player's hand
        hand_value = count_points(hand) 

        print("Player #" + str(player+1)) # prints current player
        print("Cards: " + cards.hand_display(hand) + ", " + "total: " + str(hand_value)) # displays hand and their value

        while True: # Loop for player's options 
            hand_value = count_points(hand) 
            
            if hand_value > 21: # handle busting
                print("Busts!")
                print("")
                break
            
            choice = input("Hit (h) or stand (s)? ").lower()
        
            if choice == "h":
                hand.append(deck.pop()) # deals card from deck to current players hand
                hand_value = count_points(hand)
                print("Cards: " + cards.hand_display(hand) + ", " + "total: " + str(hand_value))

            elif choice == "s":
                print("")
                break # ends loop for current player

            else:
                print('Please enter "h" or "s". ') # continues loop until valid input is entered


def dealers_turn(dealer_hand):
    """
    Dealers's turn.
    """
    dealer_points = count_points(dealer_hand)

    while count_points(dealer_hand) <= 17:
        dealer_hand.append(deck.pop()) # adds to dealer's hand if their hand is less than or equal to 17 in value
        print("Dealer draws " + str(dealer_hand[-1])) # displays the card being added to dealer's hand 
        dealer_points = count_points(dealer_hand) # updates dealer's points value
    print("Dealer's hand: " + cards.hand_display(dealer_hand) + ", " + "total: " + str(dealer_points)) # displays dealer's hand and total points value 
    
    return dealer_hand, dealer_points            


def win_loss_conditions(all_hands, all_bets, player_balance, dealer_points):
    """
    Evaluates the win/loss conditions for the current turn.
    """
    for player, hand in enumerate(all_hands):
        if count_points(hand) > 21:                                                     # if player(s) bust or points value is over 21
            print("Player " + str(player+1) + " loses $" + str(all_bets[player]) + ".")
            player_balance[player] = player_balance[player] - all_bets[player]
        
        else:                                                                           # if player(s) don't bust
            
            if count_points(hand) > dealer_points:                                      # when player has more points than dealer, they win
                print("Player " + str(player+1) + " wins $" + str(all_bets[player]) + ".")
                player_balance[player] = player_balance[player] + all_bets[player]
            elif dealer_points > 21:                                                    # if dealer busts, player wins
                print("Player " + str(player+1) + " wins $" + str(all_bets[player]) + ".")
                player_balance[player] = player_balance[player] + all_bets[player]
            elif count_points(hand) == dealer_points:                                   # dealer points == player points, push 
                print("Player " + str(player+1) + " pushes.")
            elif dealer_points > count_points(hand):                                    # dealer has more points than player, dealer win
                print("Player " + str(player+1) + " loses $" + str(all_bets[player]) + ".")
                player_balance[player] = player_balance[player] - all_bets[player]


def one_turn():
    """
    Plays one full turn by calling all the pre-defined functions need for a turn.
    """
    all_bets = ask_for_bets(num_players)    
    print("")
    
    dealer_hand, all_hands = initial_hands(num_players) 

    display_initial_hands(dealer_hand, all_hands)
    print("")

    players_turn(all_hands)

    dealer_hand, dealer_points = dealers_turn(dealer_hand)

    win_loss_conditions(all_hands, all_bets, player_balance, dealer_points)
    
    input("Please press enter to continue.")
    print("")


# Initialize values
num_players = int(input("How many players? "))
player_balance = [1000] * num_players
deck = shuffled_deck()

# main loop
for i in range(3):
    print("")
    one_turn()

# final balance announcement 
for player, balance in enumerate(player_balance):
    print("Player #" + str(player+1) + ": " + str(balance))