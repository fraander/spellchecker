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
            return len(should_process) > 1 and should_process[-1] != "y" and should_process[-1] == "s" and \
                self.get_word(should_process[:-1])

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
        """
        Suggest words based on the given word using a variety of algorithms to generate new strings to test from
        given string.
        More efficient than comparing similarity to every word in the dictionary.
        param w: word to base suggestions off of
        :return: List of suggestions
        """

        def replace_test(e):
            """
            Replaces every letter in the string with a letter from a->z and checks if that makes a valid word
            :return: suggestions created by this test
            """
            s = []

            for index in range(1, len(e)):
                for c in string.ascii_lowercase:
                    test = e[0:index - 1] + c + e[index:]
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

                s.append(test)

            return s

        def combine_test(e, test_1, test_2):
            """
            Combine two tests with each other
            :param e: word to base tests on
            :param test_1: first test
            :param test_2: second test
            :return: result of combining tests
            """
            out = []
            for word in test_1(e):
                out += test_2(word)
            # print(process_suggestions(out))
            return out

        def process_suggestions(possible):
            """
            Return only the suggestions which are words
            :param possible: possible words
            :return: actual words
            """
            suggestions = []
            for pos in possible:
                if self.is_word(pos) and pos.lower() not in [n.lower() for n in suggestions]:
                    suggestions.append(pos)

            return suggestions

        # make a series of changes to each word and check if those changes produce words in the dictionary
        # try each test once, then combine each with another one time
        p = remove_test(w) + replace_test(w) + insertion_test(w) + shuffle_test(w)

        sugs = process_suggestions(p)
        p = []
        if len(p) < 8:
            p += combine_test(w, insertion_test, insertion_test) + \
                combine_test(w, insertion_test, replace_test) + \
                combine_test(w, insertion_test, shuffle_test) + \
                combine_test(w, insertion_test, remove_test)

        sugs += process_suggestions(p)
        p = []
        if len(p) < 8:
            p += combine_test(w, replace_test, insertion_test) + \
                combine_test(w, replace_test, replace_test) + \
                combine_test(w, replace_test, shuffle_test) + \
                combine_test(w, replace_test, remove_test)

        sugs += process_suggestions(p)
        p = []
        if len(p) < 8:
            p += combine_test(w, shuffle_test, insertion_test) + \
                combine_test(w, shuffle_test, replace_test) + \
                combine_test(w, shuffle_test, shuffle_test) + \
                combine_test(w, shuffle_test, remove_test)

        sugs += process_suggestions(p)
        p = []
        if len(p) < 8:
            p += combine_test(w, remove_test, insertion_test) + \
                combine_test(w, remove_test, replace_test) + \
                combine_test(w, remove_test, shuffle_test) + \
                combine_test(w, remove_test, remove_test)

        return sugs[0:7]  # return only the first 7 results to not overwhelm the user
        # remove the [0:7] to see all suggestions the algorithm produces

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
