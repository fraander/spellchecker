import string
from Dictionary import Dictionary
from PathManager import PathManager


class SpellCheck:
    """
    Processes business logic for checker, handles reading/writing files, asking user for replacement words
    """
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
                if opt_in == len(options) + 1:
                    return w
                else:
                    return options[opt_in][0]
            except ValueError:
                opt_in = -1
                print("Invalid input. Try again.")
            except KeyError:
                opt_in = -1
                print("Invalid input. Try again.")
            except IndexError:
                opt_in = -1
                print("Invalid input. Try again.")

    def __init__(self):
        dictionary = Dictionary()  # dictionary
        filename = PathManager().filename  # path-manager

        with open("edited+" + filename, 'w') as o:
            with open(filename, 'r') as f:  # open read and write files
                buffer = ""  # create a buffer so that the program is not limited in memory and can read large files
                capitalize = False

                while True:
                    c = f.read(1)  # read by character

                    if not c:  # reached eof
                        break

                    if c in string.punctuation or c in string.whitespace:
                        if buffer in string.whitespace:
                            print(buffer, end="")
                        elif not dictionary.check_word(buffer):
                            print("**", buffer, "**", c, sep="", end="")
                        else:
                            print(buffer + c, end="")
                        buffer = ""
                    else:
                        buffer += c