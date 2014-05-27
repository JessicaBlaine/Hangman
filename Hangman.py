'''
This is a small project I started as general programming practice, and
especially practice for the OOP components of Python. The Guesser class
created takes a user given word and will attempt to determine that word
following standard hangman rules, losing after 6 wrong guesses. It is supplied
with a large dictionary of English words for consideration. The board is
printed to the terminal after every guess, and is a beautifully crafted ASCII
masterpiece.

Single words of a-z aplhabetic characters are the only workable inputs. Future
features should include arbitrary length multi-word phrases, and the current
architecture is close to supporting that already. Allowing a user to guess is
also implementable (probably) fairly easily.

The rules of PEP 8 are only a minor influence. The code will be unelegant, the
documentation either unclear or too redundant, and the solutions to what are
(to you) simple problems will be surprisingly verbose sand hackish. I'm sorry,
but at least I got this thing to do what I meant. May this be a history lesson
for both my future self and others.
'''

#Lots of default settings and initializations of global variables.
word = raw_input("What would you like me computer to try and guess?").lower()
spaces = [0] #location of gaps in phrase. emptiness causes errors on single words
board = []
gamestart = 'no'
english = set()
wrong_guesses = []
alphabet = list('abcdefghijklmnopqrstuvwxyz')

#I'm not totally sure how this works, as it's a friend's code. It takes a
#text file of English words and turns it into a useful set of words for the AI
def read_file(name='wordsEn.txt'):
    fil = open(name)
    words = fil.readlines()
    for w in words: #removes the newlines from every word.
        english.add(w.strip())
read_file()

#My first ever class. 
from Guesser import Guesser
guesser_ai = Guesser(english, alphabet, len(word))
guesser_ai.same_len_test() #eliminates any diffenrent length words than target

#Takes a word or phrase and produces a hangman board with the apropiate number
#of underscores, with additional spaces between words.
def generate_board(word):
    global board
    x = 0  #counting where in the word is being tested
    for l in word:  #determines where spaces are in word
        if l == ' ':         #if a letter is a space
            spaces.append(x) #adds the location of that space to list
        x += 1
        
    length = len(word) #used to determine number of '_'s needed
    spaces.append(length - spaces[-1])
        #determines the location of the last character in the word/phrase
    for n in spaces: #creates a list of blanks with extra spaces between words
        board = board + list('_'*n + ' ')

#This outputs the combination of underscores and ASCII art needed for any self
#respecting hangman man game. Body parts of the hanging man and the letters
#guessed responsible for his formation are both printed from here.
def display_board(board):
    lbg = len(wrong_guesses)
    print"""
      _______
     |       |     Wrong Guesses:
     |       |      {} {} {} {} {} {}
     |       {}
     |      {}{}{}
     |      {} {}
     |
    ---

    """.format(
      #displays each wrongly guesses letter to the side
      wrong_guesses[0] if lbg >= 1 else '',
      wrong_guesses[1] if lbg >= 2 else '',
      wrong_guesses[2] if lbg >= 3 else '',
      wrong_guesses[3] if lbg >= 4 else '',
      wrong_guesses[4] if lbg >= 5 else '',
      wrong_guesses[5] if lbg >= 6 else '',
      #displays +1 additional body part for each wrong guess
      'O' if lbg >= 1 else '',
      '/' if lbg >= 2 else '',
      '|' if lbg >= 3 else '',
      '\\' if lbg >= 4 else '',
      '/' if lbg >= 5 else '',
      '\\' if lbg >= 6 else ''
      )
    print ' '.join(board) #I love .join(). No info, just adoration.<3

#This takes a letter and determines if it is in the word (duh). Replaces
#blanks in the word with the correct guess. Assumes guess is False unless
def guess_letter(guess):
    correct_guess = False
    x = 1
    letter_locations = []
    if guess in word:
        #correct letters only belong in certain places in the word, so this
        #lovely for loop figures out where that is and sticks 'em there.
        for L in word: #iterates over every letter in the word
            if L == guess:
                board[x] = "{}".format(L) #swaps out board's blank with letter
                letter_locations.append(x-1) #adds to list of letter's location
                correct_guess = True
            x += 1
    if correct_guess == False:
        wrong_guesses.append(guess) #adds that letter to the list of bad guesses
    return letter_locations, correct_guess #return value vs. modify a global?

#This is called when the AI has only one possible word left in its set. Game
#is ended whether the guess is right or wrong.
def wintest(word, guess):
    global gamestart
    if word == guess:
        board = " " + guess
        display_board(board)
        gamestart = 'end'
        print ""
        print "I've got it! I win!"
    else:
        gamestart = 'end'
        print "That's wrong? I was so sure it was {}.".format(guess)

#generates the board if the game hasn't yet started.
while gamestart == 'no':
    generate_board(word)
    gamestart = 'yes'

while gamestart == 'yes':
    display_board(board)
    if len(wrong_guesses) >=6:
        gamestart = 'end'
        print "I'm out of guesses. That word was too hard for me."
        break
    if len(guesser_ai.words_left) == 1:
        wordguess = list(guesser_ai.words_left)[0]
        wintest(word, wordguess)
    guess = guesser_ai.determine_guess()
    letter_locations, correct_guess = guess_letter(guess)
    guesser_ai.eliminate_words(guess, letter_locations, correct_guess)
    import time
    time.sleep(.5)
