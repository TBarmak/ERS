"""
Author: Taylor Barmak
A GUI to play Egyptian Rat Screw against the computer

Rules of ERS: https://bicyclecards.com/how-to-play/egyptian-rat-screw/

To do:
- Indicate the thickness of the piles throughout the game
- Improve the aesthetic
"""
# Imports
import random
from tkinter import *
from tkinter import ttk

# Global variables to represent the state of the game
player_pile = []
comp_pile = []
slap_pile = []
turn = True # True if player's turn, False if computer's turn
chances = 0 # Number of chances to answer another player's face card (0 means that one is not in play)
setting_blank = False # Variable to stop the dealing of cards while the slap pile is being taken

# Global variables to represent the settings chosen by the players
divorce = False
marriage = False
difficulty = 1

# Global boolean variables to represent if a deck can be slapped
is_slappable = False # Indicates if the cards can be taken
was_slappable = False # Variable to make sure not to penalize slapping second on a pile that was slappable

"""
create_deck will return a shuffled deck of cards in the form of a list
return a list representing a deck of cards
"""
def create_deck():
    # return value
    ret = []
    # Lists of the values and suits
    values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    suits = ['H', 'D', 'S', 'C']
    # Create a deck of cards
    for value in values:
        for suit in suits:
            ret.append(value + suit)
    # Shuffle the deck
    random.shuffle(ret)
    return ret

"""
start_game will create the deck, shuffle it and deal the cards to the players
"""
def start_game():
    # Global variables
    global player_pile
    global comp_pile
    global divorce
    global marriage
    global difficulty
    global chances
    global is_slappable
    global was_slappable

    # Update the info label
    info.config(text='Click "Deal" \nto start play.')

    # Create a deck of cards and deal them to the players
    deck = create_deck()
    player_pile = deck[::2]
    comp_pile = deck[1::2]

    # Change the settings of the game based on the checkboxes
    if 'selected' in divorce_checkbox.state():
        marriage = True
    if 'selected' in marriage_checkbox.state():
        divorce = True
    difficulty = difficulty_slider.get()

    # Reset chances, is_slappable, and was_slappable
    chances = 0
    is_slappable = False
    was_slappable = False

"""
check_slappable will take a pile as an argument and return true if it can be slapped
return True if it can be slapped, False otherwise
"""
def check_slappable():
    # If there aren't at least two cards yet, return False
    if len(slap_pile) < 2:
        return False
    # Check for a pair
    if slap_pile[-2][:-1] == slap_pile[-1][:-1]:
        return True
    # Check for marriage, if the player chose to include that setting
    if marriage:
        if (slap_pile[-2][:-1] == 'Q' and slap_pile[-1][:-1] == 'K') or (slap_pile[-2][:-1] == 'K' and slap_pile[-1][:-1] == 'Q'):
            return True
    # If there aren't at least three cards yet, return False
    if len(slap_pile) < 3:
        return False
    # Check for a sandwich
    if slap_pile[-3][:-1] == slap_pile[-1][:-1]:
        return True
    # Check for divorce, if the player chose to include that setting
    if divorce:
        if (slap_pile[-3][:-1] == 'Q' and slap_pile[-1][:-1] == 'K') or (slap_pile[-3][:-1] == 'K' and slap_pile[-1][:-1] == 'Q'):
            return True
    return False

"""
is_face method will return True for any card that is an J, Q, K, or A
card - a string to represent the card being analyzed
return True if it's a face (as described above), False otherwise
"""
def is_face(card):
    if card[0] == 'J' or card[0] == 'Q' or card[0] == 'K' or card[0] == 'A':
        return True
    return False

"""
set_chances will set the global chance variable depending on the value of the face card
card - a string to represent the card being analyzed
"""
def set_chances(card):
    # Global variables
    global chances
    global turn

    # Set the value if a face card has been played
    if is_face(card):
        value = card[0]
        if value == 'J':
            chances = 1
        elif value == 'Q':
            chances = 2
        elif value == 'K':
            chances = 3
        elif value == 'A':
            chances = 4
        # Update the info label to let the player know what's going on
        if turn:
            player = "Computer has "
        else:
            player = "You have "
        message = player + str(chances) + " chance(s)\n to play a FoA"
        info.config(text=message)
        # It becomes the other player's turn
        turn = not turn
    # Otherwise, only decrement chances if a player did not play a face card
    elif chances != 0:
        chances -= 1
        # Update the info label to let the player know what's going on
        if turn:
            player = "You have "
        else:
            player = "Computer has "
        message = player + str(chances) + " chance(s)\n to play a FoA"
        info.config(text=message)
        # If the chances drops to zero, the pile goes to the player whose turn it is not
        if chances == 0:
            take_pile(not turn)
    # If nothing special has happened with face cards, it becomes the other player's turn
    else:
        turn = not turn
    # If it's a player's turn and they are out of cards, have the other player take the cards
    if turn and len(player_pile) == 0:
        take_pile(False)
    elif not turn and len(comp_pile) == 0:
        take_pile(True)

"""
slap will attempt to slap a pile
player - True if the player is trying to slap, False if the computer is trying to slap
"""
def slap(player):
    # Global variables
    global is_slappable
    global was_slappable
    global slap_pile
    global player_pile
    global comp_pile
    # If the pile is slappable, have the correct person take the cards
    if is_slappable:
        is_slappable = False
        # Reset chances
        chances = 0
        take_pile(player)
        if player:
            info.config(text='Player slapped\n first.')
        else:
            info.config(text='Computer slapped\n first.')
    # If the pile was slappable, there's no penalty
    elif was_slappable:
        pass
    # Otherwise, the player has to burn a card
    else:
        if player:
            info.config(text='Player burned\n a card.')
            slap_pile.insert(0, player_pile[0])
            player_pile = player_pile[1:]
        else:
            info.config(text='Computer burned\n a card.')
            slap_pile.insert(0, comp_pile[0])
            comp_pile = comp_pile[1:]

"""
take_pile will give the slap pile to the player or the computer depending on the boolean argument
player - boolean variable (True if the pile goes to the player, False if it goes to the computer)
"""
def take_pile(player):
    # Global variables
    global slap_pile
    global player_pile
    global comp_pile
    global turn
    global chances
    global setting_blank
    chances = 0
    # If the player is getting the pile, transfer the slap_pile cards to them and make it their turn
    if player:
        for card in slap_pile:
            player_pile.append(card)
        slap_pile = []
        turn = True
    # If the computer is getting the pile, transfer the slap_pile cards to them and make it their turn
    else:
        for card in slap_pile:
            comp_pile.append(card)
        slap_pile = []
        turn = False
    # Set the top card to blank to visually show that the pile was taken
    setting_blank = True
    root.after(700, show_hand)

"""
show_hand method will flash a robot hand or human hand to visually show the pile being taken
"""
def show_hand():
    if turn:
        file_name = 'human_hand.png'
    else:
        file_name = 'robot_hand.png'
    hand = PhotoImage(file=file_name).subsample(back_img_multiplier, back_img_multiplier)
    slap_top_image.configure(image=hand)
    slap_top_image.image = hand
    # If a player is left with no cards after the pile is taken, declare a winner
    if len(player_pile) == 0:
        root.after(750, declare_winner(False))
    elif len(comp_pile) == 0:
        root.after(750, declare_winner(True))
    else:
        root.after(1200, set_card_blank)

"""
set_card_blank changes the image of the slap pile to be a blank card
"""
def set_card_blank():
    global setting_blank
    card_photo = PhotoImage(file='placeholder.png').zoom(card_img_multiplier, card_img_multiplier)
    slap_top_image.configure(image=card_photo)
    slap_top_image.image = card_photo
    # Allow cards to be dealt
    setting_blank = False
    if not turn:
        root.after(2000, lambda: deal_card(False))

"""
deal_card method will have a player deal a card to the slap pile
player - a boolean variable representing which player is trying to deal the card (True if player, False if Computer)
"""
def deal_card(player):
    # Global variables
    global turn
    global player_pile
    global comp_pile
    global slap_pile
    global is_slappable
    global was_slappable

    # Clear the text from the info label
    info.config(text="")

    # If the person who's turn it is and the person who is trying to deal a card match, execute the method
    if player == turn and not setting_blank:
        # Reset the slappable variables to False when a new card is dealt
        is_slappable = False
        was_slappable = False
        # If it's the player's turn, have them deal a card
        if turn:
            if len(player_pile) > 0:
                slap_pile.append(player_pile[0])
                player_pile = player_pile[1:]
        # If it's the computer's turn, have them deal a card
        else:
            if len(comp_pile) > 0:
                slap_pile.append(comp_pile[0])
                comp_pile = comp_pile[1:]
        # Change the image on the slap pile
        card_photo = PhotoImage(file='cards\\' + slap_pile[-1].lower() + '.png').zoom(card_img_multiplier, card_img_multiplier)
        slap_top_image.configure(image=card_photo)
        slap_top_image.image = card_photo
        # Check if the pile has become slappable
        if check_slappable():
            # Don't clear the text of the info label if face cards are in play
            if chances != 0:
                if turn:
                    player = "You have "
                else:
                    player = "Computer has "
                message = player + str(chances) + " chance(s)\n to play a FoA"
                info.config(text=message)
            is_slappable = True
            was_slappable = True
            # Make the computer slap quicker when the difficulty is harder
            time = 0.1*((-1 * difficulty) + 5) + 1
            root.after(int(time * 1000), lambda: slap(False))
        # Change the global turn variable and adjust chances
        set_chances(slap_pile[-1])

        # If it has become the computer's turn, have them deal a card
        if not turn:
            # Have the computer attempt to deal a card three seconds after they are given the chance to
            root.after(1500, lambda: deal_card(False))

"""
declare_winner will have the GUI show who won
winner - True if the player won, False if the computer won
"""
def declare_winner(winner):
    destroy_the_gui()
    if winner:
        message = "Congratulations, you won!"
    else:
        message = "The computer is victorious!"
    winner_label = Label(text=message, font=("Serif", 30))
    winner_label.grid()

"""
create_the_gui will create the game after the user has read the instructions
"""
def create_the_gui():
    # Destroy the instructions screen
    title.destroy()
    instructions.destroy()
    understood.destroy()

    # Images for the card back and front
    back_photo = PhotoImage(file='back.png').subsample(back_img_multiplier, back_img_multiplier)
    card_photo = PhotoImage(file='placeholder.png').zoom(card_img_multiplier, card_img_multiplier)

    comp_pile_image.grid(column=0, row=0, rowspan=2)
    slap_top_image.grid(column=1, row=1, rowspan=2)
    player_pile_image.grid(column=2, row=2, rowspan=2)
    difficulty_slider.grid(column=3, row=1)
    divorce_checkbox.grid(row=0, column=3)
    marriage_checkbox.grid(row=0, column=4)
    start.grid(row=1, column=4)
    slap_button.grid(row=2, column=3, columnspan=5)
    deal.grid(row=3, column=3, columnspan=5)
    info.grid(row=0, column=1)

"""
destroy_the_gui will clear all of the items on the gui
"""
def destroy_the_gui():
    comp_pile_image.destroy()
    slap_top_image.destroy()
    player_pile_image.destroy()
    difficulty_slider.destroy()
    divorce_checkbox.destroy()
    marriage_checkbox.destroy()
    start.destroy()
    slap_button.destroy()
    deal.destroy()
    info.destroy()

# Create the GUI
root = Tk()
root.title("ERS")
# What to multiply the screen height by to get the height of the GUI
sh_to_gh = 0.5
# What to multiply the height of the GUI by to determine the width
aspect_ratio = 1.75
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
gui_height = round(screen_height * sh_to_gh)
gui_width = round(gui_height * aspect_ratio)
root.geometry(str(gui_width) + "x" + str(gui_height))

# These multipliers will get the image heights close to 1/4 the screen height
back_img_multiplier = round((2 * 1040) / gui_height)
card_img_multiplier = round(1 / (2 * 98 / gui_height))

'''
Instruction screen: 
'''
title = Label(root, text="Egyptian Rat Screw", font=("Serif", 24))
title.grid(row=0, column=2, rowspan=3)

f = open("instructions.txt", "r")
instructions_string = ''
for line in f:
    instructions_string += line
f.close()

instructions = Label(root, text=instructions_string, justify="left", padx=10)
instructions.grid(row=4, column=0, rowspan=5, columnspan=5)

understood = Button(root, text="I understand.", command=create_the_gui)
understood.grid(row=9, column=2)

'''
Elements to appear on GUI after the user indicates that the understand the rules of the game
'''
# Images for the card back and front
back_photo = PhotoImage(file='back.png').subsample(back_img_multiplier, back_img_multiplier)
card_photo = PhotoImage(file='placeholder.png').zoom(card_img_multiplier, card_img_multiplier)
# Label for the comp pile
comp_pile_image = Label(root, image=back_photo)
# Label for the slap pile
slap_top_image = Label(root, image=card_photo)
# Label for the player pile
player_pile_image = Label(root, image=back_photo)
# Slider for the difficulty
difficulty_slider = Scale(root, from_=1, to=10, length=round(gui_width/5), cursor='tcross', orient='horizontal', label='Difficulty')
# Checkboxes for divorce and marriage
divorce_checkbox = ttk.Checkbutton(root, text="Divorce")
marriage_checkbox = ttk.Checkbutton(root, text="Marriage")
# Button to start the game
start = Button(root, text="Start Game", command=start_game)
# Button to slap
slap_button = Button(root, text="Slap", height=5, width=40, command=lambda: slap(True))
# Button to deal a card
deal = Button(root, text="Deal", height=5, width=40, command=lambda: deal_card(True))
# Label to indicate what is going on
info = Label(root, text="Click 'Start Game'\n to start a game.")

root.mainloop()
