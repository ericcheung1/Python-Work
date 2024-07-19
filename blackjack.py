import cards
import random

# creating and shuffling deck function def
def shuffled_deck():
    """
    Creates a shuffled deck of cards.
    """
    d = cards.deck()
    random.shuffle(d)
    return d 

# counting points function definition
def count_points(some_hand):
    """
    Calculates points in a hand
    """
    points = 0
    aces = 0 
    for cards in some_hand:
        if cards.rank() in ["J", "Q", "K", "T"]:
            points = points + 10
        elif cards.rank() == "A":
            aces = aces + 1
            points = points + 11
        else:
            points = points + int(cards.rank())
    
    while points > 21 and aces > 0:
        points = points - 10
        aces = aces - 1 
    
    return points 


#how many players and their balance
num_players = int(input("How many players? "))
player_balance = 1000 * num_players
print(player_balance)
deck = shuffled_deck()

for i in range(3):
    all_hands = []
    all_bets = []

    # asks for how many players
    for player in range(num_players):
        print("Player #" + str(player+1) + "\n" + "You have S1000.")
        bet = input("How much do you want to bet? ")
        all_bets.append(bet)
    print(all_bets)    
    print("")
    
    # deals intial hands for players and dealer
    for player in range(num_players):
        hand = [deck.pop(), deck.pop()]
        all_hands.append(hand)

    dealer_hand = [deck.pop(), deck.pop()]

    # display initial hands for player and dealer
    print("Dealer: " + cards.hand_display(dealer_hand)) 
    for player, hand in enumerate(all_hands):
        print("Player #" + str(player+1) + ": " + cards.hand_display(hand))
    print("")

    # players turn
    for player, hand in enumerate(all_hands): # Goes through each player's hand
    
    
        while True: # Loop for hits or stands or invalid inputs
            hand_value = count_points(hand) 

            # prints player, hand, and hand value
            print("Player #" + str(player+1))
            print("Cards: " + cards.hand_display(hand) + ", " + "total: " + str(hand_value))
            
            # handle busting
            if hand_value > 21: 
                print("Busts!")
                break
            
            choice = input("Hit (h) or stand (s)? ").lower()
        
            if choice == "h":
                hand.append(deck.pop()) # deals card from deck to current players hand
                #print(all_hands)
                print("Player #" + str(player+1))
                print("Cards: " + cards.hand_display(hand) + ", " + "total: " + str(hand_value))
            elif choice == "s":
                break
            else:
                print('Please enter "h" or "s". ')

    # dealer's turn
    dealer_points = count_points(dealer_hand)
    print("Dealer value:", dealer_points)
    while count_points(dealer_hand) <= 17:
        dealer_hand.append(deck.pop())
        print("Dealer draws " + str(dealer_hand[-1]))
        dealer_points = count_points(dealer_hand)
        print("Dealer value:", dealer_points)
    print("Dealer's hand: " + cards.hand_display(dealer_hand) + ", " + "total: " + str(dealer_points))

    # win/loss condition 
    for player, hand in enumerate(all_hands):
        if count_points(hand) > 21:
            print("Player " + str(player+1) + "loses" + all_bets[player])
        else:
            if count_points(hand) > dealer_points:
                print("Player " + str(player+1) + "wins" + all_bets[player])

    