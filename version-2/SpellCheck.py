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
                        if dictionary.get_word(should_process):
                            print(should_process, sep="", end="")
                            print(c, end="")
                        else:
                            if should_process in string.whitespace:
                                print(should_process, end="")
                            elif len(should_process) > 0 and should_process[0] in string.whitespace:
                                print(should_process[0], end="")
                                print("**", should_process[1:], "**", sep="", end="")  # TODO: process word
                            else:
                                print("**", should_process, "**", sep="", end="")  # TODO: process word
                            print(c, end="")
                        buffer = ""
                        should_process = None
                    else:
                        buffer += c

