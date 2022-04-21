import string
from Dictionary import Dictionary


class Suggester:

    def __init__(self):
        self.dictionary = Dictionary()

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    def process_suggestions(self, possible):
        """
        Return only the suggestions which are words
        :param possible: possible words
        :return: actual words
        """
        suggestions = []
        for pos in possible:
            if self.dictionary.is_word(pos) and pos.lower() not in [n.lower() for n in suggestions]:
                suggestions.append(pos)

        return suggestions

    def suggest(self, w):
        """
        Suggest words based on w
        :param w: word to base suggestions on
        :return: list of first 7 suggestions
        """
        # make a series of changes to each word and check if those changes produce words in the dictionary
        # try each test once, then combine each with another one time
        p = self.remove_test(w) + self.replace_test(w) + self.insertion_test(w) + self.shuffle_test(w)

        sugs = self.process_suggestions(p)
        p = []
        if len(p) < 8:
            p += self.combine_test(w, self.insertion_test, self.insertion_test) + \
                self.combine_test(w, self.insertion_test, self.replace_test) + \
                self.combine_test(w, self.insertion_test, self.shuffle_test)

        sugs += self.process_suggestions(p)
        p = []
        if len(p) < 8:
            p += self.combine_test(w, self.replace_test, self.insertion_test) + \
                self.combine_test(w, self.replace_test, self.replace_test) + \
                self.combine_test(w, self.replace_test, self.shuffle_test) + \
                self.combine_test(w, self.replace_test, self.remove_test)

        sugs += self.process_suggestions(p)
        p = []
        if len(p) < 8:
            p += self.combine_test(w, self.shuffle_test, self.insertion_test) + \
                self.combine_test(w, self.shuffle_test, self.replace_test) + \
                self.combine_test(w, self.shuffle_test, self.shuffle_test) + \
                self.combine_test(w, self.shuffle_test, self.remove_test)

        sugs += self.process_suggestions(p)
        p = []
        if len(p) < 8:
            p += self.combine_test(w, self.remove_test, self.replace_test) + \
                self.combine_test(w, self.remove_test, self.shuffle_test) + \
                self.combine_test(w, self.remove_test, self.remove_test)

        return sugs[0:7]  # return only the first 7 results to not overwhelm the user
        # remove the [0:7] to see all suggestions the algorithm produces
