from Dictionary import Dictionary


class SpellCheck:
    def __init__(self):
        self.dic = Dictionary()

    def check_word(self, w):
        """
        Check if word is in the dictionary
        :param w: word to check
        :return: true if in, false if not
        """
        if self.dic.get_word(w):  # word is valid
            return True
        else:
            return False