def get_secret():
    """
    Gets the secret word/phrase.
    """
    return input("Enter a secret word: ")

secret = get_secret() # Gets secret word from player


print("\n" * 60)

# Initialize Variables 
display = "_" * len(secret) # Create display string which uses underscores to represent letters
misses = 0 # Counts the number of incorrect guesses
correct = 0 # Counts the number of correct guesses
unguessed = display.count("_") # Keeps track of unguessed letter by counting the underscores in display string

def do_turn(display, misses):
    """
    Display the current status for the user and let them make a guess. 
    """
    print("Word so far: " + display)
    print("Misses: " + str(misses))
    guess = input("What letter would you like to guess? ")
    print("\n")
    return guess


def new_display(secret, display, guess):
    """
    Updates display string after user has made a guess and counts correct guesses.
    """
    newdisp = "" # Where the new display string is saved to 
    count = 0 # Counts the correct guesses in this turn

    if len(guess) == 1: # Checks for one letter in input
        for i in range(len(secret)):
            if secret[i] == guess:
                newdisp = newdisp + guess # Adds correctly guessed letter to display string
                count = count + 1 # Adds 1 to count if guess is correct
            else: 
                newdisp = newdisp + display[i] # Keeps underscore in display string when guessed letter is not in the secret word

    else:
        print("You must print a single letter.")
        return display, 0 # returns previous display string if guess is invalid, and sets correct guesses to 0
    
    return newdisp, count


# Main Loop
while unguessed != 0 and misses < 6: # Loops until there are 0 unguessed letters or they guess 5 times 
    guess = do_turn(display, misses) # Assigns guess to variable
    display, count = new_display(secret, display, guess) # Updates display and count variable
    
    if count > 0:
        correct = correct + count # Keeps track of correct guess in the current game
    
    elif count <= 0 and len(guess) == 1: 
        misses = misses + 1 # Counts misses if are 1 letter long 
    
    unguessed = display.count("_") # Updates unguessed variable


# End of game messages
if display == secret:
    print("You guessed the secret correctly:", display)
if misses > 5:
    print("You lose. The secret was:", secret)