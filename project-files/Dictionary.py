class Dictionary:
    def find_similar(self, word):

        similar = []
        # Try scoring each word on number of letters different from the given word. Scores that are 1 or 2 get
        # marked as suggestions

        for entry in self.data.keys():
            if len(word) != len(entry):
                break

            print("len:", entry)

            # if len(word) - 1 > len(entry) or len(word) + 1 > len(entry):
            #    break

            diff = 0
            for i, c in enumerate(word):
                if word[i] != entry[i]:
                    diff += 1
                if diff > 2:
                    break

            if diff < 2:
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
