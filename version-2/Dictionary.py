import string


class Dictionary:

    def spell_check_word(self, should_process):
        """
        Check if a word is misspelled
        :param should_process: word to check
        :return: True if valid word or whitespace, False otherwise
        """

        def search_plain_word():
            """
            Check if the word is a valid word
            :return: True if valid
            """
            return self.get_word(should_process)

        def search_simple_plural():
            """
            Check singular form of given plural is a word (s -> "")
            :return: True if valid
            """
            return len(should_process) > 1 and should_process[-1] != "y" \
                   and should_process[-1] == "s" and self.get_word(should_process[:-1])

        def search_complex_plural():
            """
            Check if plural form of given word is valid (ies -> y)
            :return: True if valid
            """
            return len(should_process) > 3 and should_process[-3:] == "ies" \
                and self.get_word(should_process[:-3] + "y")

        def search_simple_possessive():
            """
            Check if non-possessive form of word is a valid word (...'s -> ...)
            :return: True if valid
            """
            return len(should_process) > 2 and should_process[-2:] == "’s" and self.get_word(
                should_process[:-2])

        def search_complex_possessive():
            """
            Check if non-possessive form of word is a valid word (...s' -> ...)
            :return: True if valid
            """
            return len(should_process) > 2 and should_process[-2:] == "s’" and self.get_word(
                should_process[:-2])

        def is_whitespace():
            """
            Check if given string is whitespace (" ", "\n", "\t", etc.)
            :return: True if whitespace
            """
            return should_process in string.whitespace

        return search_plain_word() or search_simple_plural() or search_complex_plural() or \
            search_simple_possessive() or search_complex_possessive() or is_whitespace()

    def is_word(self, w):
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
        # TODO: check options have not been filled before generating more suggestions
        # TODO: Improve suggestions for larger errors
        """
        Suggest words based on the given word using a variety of algorithms to generate new strings to test from
        given string.
        More efficient than comparing similarity to every word in the dictionary.
        :param w: word to base suggestions off of
        :return: List of suggestions
        """

        def double_replace_test(e):
            s = []

            for index in range(2, len(e)):
                for c in string.ascii_lowercase:
                    for d in string.ascii_lowercase:
                        test = e[0:index - 2] + c + d + e[index:]
                        if self.is_word(test) and test not in s and test != e:
                            s.append(test)

            return s

        def replace_test(e):
            """
            Replaces every letter in the string with a letter from a->z and checks if that makes a valid word
            :return: suggestions created by this test
            """
            s = []

            for index in range(1, len(e)):
                for c in string.ascii_lowercase:
                    test = e[0:index - 1] + c + e[index:]
                    if self.is_word(test) and test not in s and test != e:
                        s.append(test)
            return s

        def insertion_test(e):
            """
            Inserts a letter a->z at each spot in the word and checks if that makes a valid word
            :return: array of suggestions
            """
            s = []

            for index in range(0, len(e)):
                for c in string.ascii_lowercase:
                    test = e[0:index] + c + e[index:]
                    if self.is_word(test) and test not in s and test != e:
                        s.append(test)
            return s

        def shuffle_test(e):
            """
            Tries rearranging each adjacent set of letters and checks if that makes a valid word
            :return: array of suggestions
            """

            s = []

            for index in range(0, len(e) - 1):
                prev = e[0:index]  # -
                curr = e[index]  # i
                curr_plus_one = e[index + 1]
                rest = e[index + 2:]  # +
                test = prev + curr_plus_one + curr + rest

                if self.is_word(test) and test not in s and test != e:
                    s.append(test)

            return s

        def remove_test(e):
            """
            Tries removing each letter in the word and seeing if that makes a valid word
            :return: array of suggestions
            """

            s = []

            for index in range(1, len(e)):
                test = e[0:index - 1] + e[index:]

                if self.is_word(test) and test not in s and test != e:
                    s.append(test)

            return s

        def space_test():
            """
            add a space at each spot in the word and check if both words are valid words
            :return: no return, just modifies `suggestions` array
            """

            s = []

            for index in range(1, len(w) - 1):
                first = w[0:index]
                last = w[index:]
                if self.is_word(first) and self.is_word(last):
                    s.append(first + " " + last)

            return s

        # make a series of changes to each word and check if those changes produce words in the dictionary
        return (insertion_test(w) + replace_test(w) + shuffle_test(w) + remove_test(w) + double_replace_test(w))[0:9]

    @staticmethod
    def clean_input(w):
        """
        Remove special characters from the word to make searching more efficient
        :param w: word to clean
        :return: cleaned string
        """
        w = w.strip("=+^.&#:’ ")
        w = w.replace('\n', '')
        w = w.replace('\t', '')
        w = w.replace("’", "'")
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
