class Dictionary:

    @staticmethod
    def clean_input(w):
        """
        Remove special characters from the word to make searching more efficient
        :param w: word to clean
        :return: cleaned string
        """
        w = w.strip("=+^.&#:’")
        w = w.replace('\n', '')
        w = w.lower()
        return w

    def get_word(self, w):
        """
        Returns word or False if word not in dictionary
        :param w: word to check
        :return: word or False if not in dictionary
        """
        try:
            return self.data[w.lower()]
        except KeyError:
            return False

    def __init__(self):
        self.data = {}

        def read_dictionary_file(filename):
            """
            Read the words in a dictionary file and append them to the dictionary
            :param filename: file to read from
            :return: None
            """
            with open(filename, 'r') as f:  # open file
                for w in f:
                    w = Dictionary.clean_input(w)
                    self.data[w] = w  # add to hash map

        read_dictionary_file('words.txt')
        read_dictionary_file('contractions.txt')
