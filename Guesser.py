class Guesser:

    def __init__(self, words_left, letters_left, word_length):
            self.words_left = words_left
            self.letters_left = letters_left
            self.word_length = word_length

    def determine_guess(self):
        words_per_letter = set()
        for L in self.letters_left:
            nowwl=0 #number of words with letter
            for w in self.words_left:
                if L in w:
                    nowwl += 1
            words_per_letter.add((nowwl, L))
        occurences, letter = max(words_per_letter)
        return letter

    def eliminate_words(self, guess, letter_locations, correct_guess):
        self.letters_left.remove(guess)
        words_to_stay = set()
        if correct_guess == False:
            for w in self.words_left:
                if not guess in w:
                    words_to_stay.add(w)
        elif correct_guess == True:
            for w in self.words_left:
                pos_word = True
                for L in letter_locations:
                    if not w[L] == guess:
                        pos_word = False
                        break
                if pos_word == True:
                    words_to_stay.add(w)
        self.words_left = words_to_stay
                    
    def same_len_test(self):
        words_to_stay = set()
        for w in self.words_left:
            if self.word_length == len(w):
                words_to_stay.add(w)
        self.words_left = words_to_stay
