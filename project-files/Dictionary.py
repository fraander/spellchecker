class Dictionary:
    def find_similar(self, word):
        similar = []
        # Try scoring each word on number of letters different from the given word. Scores that are 1 or 2 get
        # marked as suggestions

        for entry in self.data.keys():
            if entry == word:  # check it's not the same word
                continue

            if len(entry) != len(word):  # check the lengths match
                continue

            diff = 0  # count the number of characters which are different
            thresh = 1 if len(word) < 6 else len(word) // 3
            for index, char in enumerate(word):
                if word[index] != entry[index]:
                    diff += 1

                if diff > thresh:
                    break

            if diff <= thresh:
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
            with open(filename, 'r') as f:
                for w in f:
                    w = w.replace('=', '')
                    w = w.replace('\n', '')
                    w = w.replace('+', '')
                    w = w.replace('^', '')
                    w = w.replace('.', '')
                    w = w.replace('&', '')
                    w = w.replace('#', '')
                    w = w.replace(':', '')

                    w = w.lower()

                    d[w] = w

        d = {}

        add_to_dictionary('words.txt')  # get a list of words
        add_to_dictionary('contractions.txt')  # get a list of contractions

        self.data = d
