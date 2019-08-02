"""
Taylor Barmak

Play a simple game of Go Fish against the computer.
"""

import random
import time

"""
show_cards method takes a list of cards and returns a string representation of them
pile - a list of cards
return - a string representation of the list
"""
def show_cards(pile):
    ret = ""
    for card in pile:
        ret += card + " "
    return ret

"""
card_index method checks to see if a card of a given value is contained within the pile
pile - a list of cards
value - a string representing one of the values ace through king
return the index of the card in the pile, or -1 if it was not found
"""
def card_index(pile, value):
    for a in range(len(pile)):
        if pile[a][:-1] == value:
            return a
    return -1

"""
remove_pairs method will take a pile of cards and a pair pile and move the pairs to the pair pile
pile - a list to remove the pairs from
pair_pile - a list where the pairs will go
return True if at least one pair was removed, false otherwise
"""
def remove_pairs(pile, pair_pile):
    # Create a dictionary with the card values as keys and have a list of cards being the value
    ret = False
    dict = {}
    for card in pile:
        if card[:-1] in dict.keys():
            dict[card[:-1]].append(card)
        else:
            dict[card[:-1]] = [card]
    # For each card value
    for a in dict.keys():
        # While there's at least 2 cards
        while len(dict[a]) > 1:
            ret = True
            # Put the first two cards in the pair pile
            pair_pile.append(dict[a][0])
            pair_pile.append(dict[a][1])
            # Remove them from the pile
            pile.remove(dict[a][0])
            pile.remove(dict[a][1])
            # Remove them from the dict
            dict[a].remove(dict[a][0])
            dict[a].remove(dict[a][0])
    return ret

# Lists of the numbers and suits
nums = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
suits = ['H', 'D', 'S', 'C']

# Create the deck
deck = []
for num in nums:
    for suit in suits:
        deck.append(num + suit)

# Shuffle the deck
random.shuffle(deck)

# Deal each player 7 cards
user_pile = deck[:14:2]
comp_pile = deck[1:14:2]

# Variables to store the players' pairs
user_pairs = []
comp_pairs = []

deck = deck[14:]

# Show the user their cards
print("Your cards: ")
print(show_cards(user_pile))
print()
time.sleep(2.5)

# Indicate how many pairs each player removed
remove_pairs(user_pile, user_pairs)
remove_pairs(comp_pile, comp_pairs)
print("*Mr. Computer removes " + str(int(len(comp_pairs)/2)) + " pairs.*")
print("*You remove " + str(int(len(user_pairs)/2)) + " pairs.*")

# Boolean variable to keep track of whose turn it is
# True - User
# False - Computer
turn = False
while len(user_pile) > 0 and len(comp_pile) > 0:
    time.sleep(2.5)
    # Change whose turn it is each time around
    turn = not turn
    # If it's the user's turn
    if turn:
        # Show them their cards
        print()
        print("Your cards: ")
        print(show_cards(user_pile))
        print()
        # Ask the user what card they would like to ask for
        ask = input("What value would you like to ask for (ie " + user_pile[0][:-1] + ")? ")
        # Keep asking until they ask for a value that they have
        while card_index(user_pile, ask) == -1:
            ask = input("You do not have a card of that value. Ask for another value: ")
        print("You: Mr. Computer, do you have any " + ask + "s?")
        time.sleep(2.5)
        # If the computer has a card of that value, give it to the user and remove the pairs
        if card_index(comp_pile, ask) != -1:
            print("Mr Computer: Yes, I do.")
            time.sleep(2.5)
            index = card_index(comp_pile, ask)
            user_pile.append(comp_pile[index])
            comp_pile.remove(comp_pile[index])
            remove_pairs(user_pile, user_pairs)
            print("*You graciously accept the card from Mr. Computer.*")
            time.sleep(2.5)
        # Otherwise, have the player go fish
        else:
            print("Mr. Computer: Go fish, buddy.")
            time.sleep(2.5)
            user_pile.append(deck[0])
            deck = deck[1:]
            print("*You draw a " + user_pile[-1] + ".*")
            if remove_pairs(user_pile, user_pairs):
                print("*You make a pair*")
        # If it is the computer's turn
    else:
        # Have the computer select a random value to ask for
        ask = random.choice(comp_pile)[:-1]
        print()
        print("Mr. Computer: Mr. User, do you have any " + ask + "s?")
        # If the card is in the user's pile, get it from them
        if card_index(user_pile, ask) != -1:
            print("You: Yes, I do.")
            time.sleep(2.5)
            index = card_index(user_pile, ask)
            comp_pile.append(user_pile[index])
            user_pile.remove(user_pile[index])
            remove_pairs(comp_pile, comp_pairs)
            print("*Mr. Computer graciously accepts your card.*")
        # Otherwise, have the computer go fish
        else:
            print("You: Go fish, buddy.")
            time.sleep(2.5)
            comp_pile.append(deck[0])
            deck = deck[1:]
            print("*Mr. Computer draws a card.*")
            if remove_pairs(comp_pile, comp_pairs):
                print("*Mr. Computer places a pair in his pile.*")
    # If a player runs out of cards, have them draw another one
    if len(comp_pile) == 0 and len(deck) > 0:
        print("*Mr. Computer draws one card because he ran out.*")
        comp_pile.append(deck[0])
        deck = deck[1:]
    if len(user_pile) == 0 and len(deck) > 0:
        print("*You draw one card because you ran out.*")
        user_pile.append(deck[0])
        deck = deck[1:]

# Announce the winner
print()
print()
if len(user_pairs) > len(comp_pairs):
    print("*You are victorious with " + str(int(len(user_pairs)/2)) + " pairs to Mr. Computer's " + str(int(len(comp_pairs)/2)) + ".*")
elif len(user_pairs) < len(comp_pairs):
    print("*Mr. Computer is victorious with " + str(int(len(comp_pairs)/2)) + " pairs to your " + str(int(len(user_pairs)/2)) + ".*")
else:
    print("It's a tie with 13 pairs.")