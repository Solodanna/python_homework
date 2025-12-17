def make_hangman(secret_word):
    guesses = []
    
    def hangman_closure(letter):
        guesses.append(letter)
        
        # Building the display word
        display = ''
        for char in secret_word:
            if char in guesses:
                display += char
            else:
                display += '_'
        print(display)
        
        # Checking if all letters are guessed
        unique_letters = set(secret_word)
        if unique_letters.issubset(set(guesses)):
            return True
        else:
            return False
    
    return hangman_closure

# Main game loop
if __name__ == "__main__":
    secret_word = input("Enter the secret word: ")
    hangman = make_hangman(secret_word)
    
    while True:
        guess = input("Guess a letter: ")
        if hangman(guess):
            print("You won!")
            break
