from fuzzywuzzy import fuzz


class Dictionary:
    def find_similar(self, word):
        # https://towardsdatascience.com/fuzzy-string-matching-in-python-68f240d910fe

        similar = []
        # score each word on number of different letters. Number below threshold makes it a valid suggestion

        ratio_min = 95
        while not similar:
            for entry in self.data.keys():
                ratio = fuzz.ratio(entry, word)
                if 100 > ratio > ratio_min:
                    similar.append([entry, ratio])
            if not similar:
                ratio_min -= 5

        return sorted(similar, key=lambda s: s[1])

    def __init__(self):
        # Read dictionary file
        def add_to_dictionary(filename):
            """
            Read the words in a dictionary file and append them to the dictionary
            :param filename: file to read from
            :return: None
            """
            with open(filename, 'r') as f:  # open file
                for w in f:  # clean up
                    w = w.replace('=', '')
                    w = w.replace('\n', '')
                    w = w.replace('+', '')
                    w = w.replace('^', '')
                    w = w.replace('.', '')
                    w = w.replace('&', '')
                    w = w.replace('#', '')
                    w = w.replace(':', '')

                    w = w.lower()  # set to lowercase

                    d[w] = w  # add to hash map

        d = {}  # create dictionary

        add_to_dictionary('words.txt')  # get a list of words
        add_to_dictionary('contractions.txt')  # get a list of contractions

        self.data = d  # assign
