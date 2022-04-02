class Dictionary:
    def find_similar(self, word):
        similar = []
        # score each word on number of different letters. Number below threshold makes it a valid suggestion

        for entry in self.data.keys():
            if entry == word:  # check it's not the same word
                continue

            if len(entry) != len(word):  # check the lengths match
                continue

            diff = 0  # count the number of characters which are different
            thresh = 1 if len(word) < 6 else len(word) // 3
            for index, char in enumerate(word):
                if word[index] != entry[index]:  # TODO: check if the letter is one adjacent to the correct letter
                    diff += 1

                if diff > thresh:  # if above threshold already, next word
                    break

            if diff <= thresh:  # if below the threshold, add to matches list
                similar.append(entry)

        return similar

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
