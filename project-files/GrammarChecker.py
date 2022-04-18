import string
from Dictionary import Dictionary
from FileManager import FileManager


class GrammarChecker:
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
                    return GrammarChecker.get_custom(w)
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
        filename = FileManager().filename  # file manager

        with open("edited+" + filename, 'w') as o:
            with open(filename, 'r') as f:  # open read and write files
                buffer = ""  # create a buffer so that the program is not limited in memory and can read large files
                capitalize = False

                while True:
                    c = f.read(1)  # read by character

                    if not c:  # if eof, break
                        break

                    if len(buffer) > 1 and buffer[0] in string.ascii_uppercase:
                        capitalize = True

                    # if not whitespace
                    if c not in string.punctuation and c not in string.whitespace and buffer[:-1] + c != "\n":
                        buffer += c  # increase the buffer
                    else:  # if there is whitespace (new word), access the buffer
                        w = dictionary.clean_input(buffer)  # clean the buffer for easy searching
                        word_in = dictionary.word_in(w)  # check for the word in the dictionary

                        if not word_in:  # if the word was not found
                            options = dictionary.find_similar(w)  # find similar words
                            GrammarChecker.print_options(options, buffer)  # print options
                            buffer = GrammarChecker.get_choice(options, w)  # get choice from user

                        if buffer[:-1] + c == "\n":  # if new-line, change c to new-line
                            c = "\n"
                        elif buffer[:-1] + c == "\t":  # if a tab, change c to tab
                            c = "\t"

                        if capitalize:
                            buffer = buffer.capitalize()

                        o.write(buffer + c)  # write to new file
                        print(buffer + c, end="")  # output for user to see

                        buffer = ""  # when done, clear the buffer
                        capitalize = False





