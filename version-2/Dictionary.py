import string


class Dictionary:

    def check_word(self, w):
        """
        Check if word is in the dictionary
        :param w: word to check
        :return: true if in, false if not
        """
        if self.get_word(w):  # word is valid
            return True
        else:
            return False

    def suggest_words(self, w):

        def replace_test():
            """
            Replaces every letter in the string with a letter from a->z and checks if that makes a valid word
            :return: suggestions created by this test
            """
            s = []

            for index in range(1, len(w)):
                for c in string.ascii_lowercase:
                    test = w[0:index-1] + c + w[index:]
                    if self.check_word(test) and test not in s and test != w:
                        s.append(test)

            print("replace", s)
            return s

        def insertion_test():
            """
            Inserts a letter a->z at each spot in the word and checks if that makes a valid word
            :return: array of suggestions
            """
            s = []

            for index in range(0, len(w)):
                for c in string.ascii_lowercase:
                    test = w[0:index] + c + w[index:]
                    if self.check_word(test) and test not in s and test != w:
                        s.append(test)

            print("insert", s)
            return s

        def shuffle_test():
            """
            Tries rearranging each adjacent set of letters and checks if that makes a valid word
            :return: array of suggestions
            """

            s = []

            for index in range(0, len(w) - 1):
                prev = w[0:index]  # -
                curr = w[index]  # i
                curr_plus_one = w[index + 1]
                rest = w[index + 2:]  # +
                test = prev + curr_plus_one + curr + rest

                # print(prev, curr, curr_plus_one, rest, test)

                if self.check_word(test) and test not in s and test != w:
                    s.append(test)

            print("shuffle", s)
            return s

        def remove_test():
            """
            Tries removing each letter in the word and seeing if that makes a valid word
            :return: array of suggestions
            """

            s = []

            for index in range(1, len(w)):
                test = w[0:index-1] + w[index:]

                if self.check_word(test) and test not in s and test != w:
                    s.append(test)

            return s


        def space_test():
            """
            add a space at each spot in the word and check if both words are valid words
            :return: no return, just modifies `suggestions` array
            """

            s = []

            for index in range(1,len(w)-1):
                first = w[0:index]
                last = w[index:]
                if self.check_word(first) and self.check_word(last):
                    s.append(first + " " + last)

            print("space", s)

            return s

        # make a series of changes to each word and check if those changes produce words in the dictionary
        suggestions = []

        suggestions = suggestions + insertion_test()
        suggestions = suggestions + replace_test()
        suggestions = suggestions + shuffle_test()
        # suggestions = suggestions + space_test()

        output = list(set(suggestions))  # remove duplicate values

        return sorted(output)

    @staticmethod
    def clean_input(w):
        """
        Remove special characters from the word to make searching more efficient
        :param w: word to clean
        :return: cleaned string
        """
        w = w.strip("=+^.&#:’ ")
        w = w.replace('\n', '')
        w = w.lower()
        return w

    def get_word(self, w):
        """
        Returns word or False if word not in dictionary
        :param w: word to check
        :return: word or False if not in dictionary
        """
        w = self.clean_input(w)
        w = w.lower()
        try:
            return self.data[w]
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
