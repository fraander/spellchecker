import string
from Dictionary import Dictionary
from PathManager import PathManager


class SpellCheck:
    """
    Processes business logic for checker, handles reading/writing files, asking user for replacement words
    """

    def edit_word(self, should_process):
        options = self.dictionary.suggest_words(should_process)
        self.print_options(options, buffer=should_process)
        choice = self.get_choice(options, w=should_process)
        print("~", choice, "~", sep="", end="")

    @staticmethod
    def get_custom(w):
        """
        Ask user for custom word to replace given word with
        :param w: given word
        :return: custom word
        """
        word = input(f"Replace {w} with: ")
        return word

    @staticmethod
    def print_options(options, buffer):
        """
        Formats options for suggested words to choose from
        :param options: options user has
        :param buffer: current word they are replacing
        :return: None
        """
        print("**", buffer, "**", sep="")
        for index, option in enumerate(options):
            print("[", index, "]", option)
        print("[", len(options), "]", "!! Custom Word !!")
        print("[", len(options) + 1, "]", "-- Don't change --")

    @staticmethod
    def get_choice(options, w):
        """
        Ask user for word or custom word to replace given word
        :param options: options to choose from
        :param w: current word
        :return: User's choice
        """
        opt_in = -1
        while opt_in == -1:
            opt_in = input("Which word would you like to use? [#] ")

            try:
                opt_in = int(opt_in)

                if opt_in == len(options):
                    return SpellCheck.get_custom(w)
                elif opt_in == len(options) + 1:
                    return w
                else:
                    return options[opt_in]
            except ValueError:
                opt_in = -1
                print("Invalid input. Try again.")
            except KeyError:
                opt_in = -1
                print("Invalid input. Try again.")
            except IndexError:
                opt_in = -1
                print("Invalid input. Try again.")

    @staticmethod
    def plain_output_word(c, should_process):
        print(should_process, sep="", end="")
        print(c, end="")

    def spell_check_word(self, should_process):
        def search_plain_word():
            return self.dictionary.get_word(should_process)

        def search_simple_plural():
            return len(should_process) > 1 and should_process[-1] != "y" \
                   and should_process[-1] == "s" and self.dictionary.get_word(should_process[:-1])

        def search_complex_plural():
            return len(should_process) > 3 and should_process[-3:] == "ies" \
                   and self.dictionary.get_word(should_process[:-3] + "y")

        def search_simple_possessive():
            return len(should_process) > 2 and should_process[-2:] == "’s" and self.dictionary.get_word(
                should_process[:-2])

        def search_complex_possessive():
            return len(should_process) > 2 and should_process[-2:] == "s’" and self.dictionary.get_word(
                should_process[:-2])

        return search_plain_word() or search_simple_plural() or search_complex_plural() or \
            search_simple_possessive() or search_complex_possessive()

    def __init__(self):
        self.dictionary = Dictionary()  # dictionary
        self.filename = PathManager().filename  # path-manager

        with open("edited+" + self.filename, 'w') as o:  # TODO: output file
            with open(self.filename, 'r') as f:  # open read and write files
                buffer = ""  # create a buffer so that the program is not limited in memory and can read large files
                should_process = False

                while True:
                    c = f.read(1)  # read by character

                    if not c:  # reached eof
                        break

                    # run a series of checks for what word to process
                    if c in string.punctuation or c in string.whitespace:
                        # process word up to, then write punctuation
                        should_process = buffer

                    if should_process:
                        if self.spell_check_word(should_process):
                            self.plain_output_word(c, should_process)
                        else:  # word not in dictionary
                            if should_process in string.whitespace:
                                print(should_process, end="")
                            elif len(should_process) > 0 and should_process[0] in string.whitespace:
                                print(should_process[0], end="")
                                self.edit_word(should_process)
                            else:
                                self.edit_word(should_process)
                            print(c, end="")
                        buffer = ""
                        should_process = None
                    else:
                        buffer += c
