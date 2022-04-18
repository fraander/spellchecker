import string
from fuzzywuzzy import fuzz


class Dictionary:
    """
    Handles dictionary data and string convenience methods such as finding similar words, cleaning strings,
    and checking if the word is in the dictionary.
    """
    def find_similar(self, word):
        """
        Find words similar to given word
        :param word: word to search for words that are similar
        :return: similar words
        """
        similar = []
        ratio_min = 95  # set initial fuzzy-wuzzy threshold

        while len(similar) < 3 and ratio_min > 50:
            for entry in self.data.keys():  # get ratio for each word
                ratio = fuzz.ratio(entry, word)

                if 100 > ratio > ratio_min:
                    if [entry, ratio] in similar:
                        pass
                    else:
                        similar.append([entry, ratio])

            if len(similar) < 3:
                ratio_min -= 3

        similar = sorted(similar, key=lambda s: s[1])  # return words sorted by ratio
        similar = similar[::-1]
        similar = similar[0:3]
        return similar

    @staticmethod
    def clean_input(w):
        """
        Remove special characters from the word to make searching more efficient
        :param w: word to clean
        :return: cleaned string
        """
        w = w.replace('=', '')  # clean up
        w = w.replace('\n', '')
        w = w.replace('+', '')
        w = w.replace('^', '')
        w = w.replace('.', '')
        w = w.replace('&', '')
        w = w.replace('#', '')
        w = w.replace(':', '')
        w = w.replace('’', "'")

        return w.lower()  # set to lowercase

    def word_in(self, w):
        """
        Check if the word is in the dictionary
        :param w: word to check
        :return: boolean, true if in
        """
        word_in = False
        if w in self.data.keys() or w in string.whitespace:
            word_in = True
        else:  # otherwise...
            if len(w) > 2 and w[-2:] == "'s" and w[:-2] in self.data.keys():
                word_in = True  # possessive form
            elif len(w) > 2 and w[-2:] == "s'" and w[:-2] in self.data.keys():
                word_in = True  # other possessive form
            elif len(w) > 1 and w[-1] == "s" and w[:-1] in self.data.keys():
                word_in = True  # simple plural form
        return word_in

    def __init__(self):

        # Read dictionary file
        def add_to_dictionary(filename):
            """
            Read the words in a dictionary file and append them to the dictionary
            :param filename: file to read from
            :return: None
            """
            with open(filename, 'r') as f:  # open file
                for w in f:
                    w = Dictionary.clean_input(w)
                    d[w] = w  # add to hash map

        d = {}  # create dictionary

        add_to_dictionary('words.txt')  # get a list of words
        add_to_dictionary('contractions.txt')  # get a list of contractions

        self.data = d  # assign
