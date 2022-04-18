import string
from Dictionary import Dictionary
from FileManager import FileManager


# TODO: cannot handle whitespace at end of file right now

class GrammarChecker:
    @staticmethod
    def print_options(options, buffer):
        print("**", buffer, "**", sep="")
        for index, option in enumerate(options):
            print("[", index, "]", option)
        print("[", len(options), "]", "!! Custom Word !!")

    @staticmethod
    def get_choice(options, w):
        opt_in = -1
        while opt_in == -1:
            opt_in = input("Which word would you like to use? [#] ")

            try:
                opt_in = int(opt_in)

                if opt_in == len(options):
                    return GrammarChecker.get_custom(w)
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
        filename = "doc_wrong.txt"  # FileManager().fn  # file manager

        with open("edited+" + filename, 'w') as o:
            with open(filename, 'r') as f:  # open read and write files
                buffer = ""  # create a buffer so that the program is not limited in memory and can read large files
                capitalize = False

                while True:
                    c = f.read(1)  # read by character

                    if len(buffer) > 1 and buffer[0] in string.ascii_uppercase:
                        capitalize = True

                    if not c:  # if eof, break
                        # TODO: do something at eof since there are eof errors right now
                        break

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

                        o.write(buffer)  # check for type of trailing whitespace
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

    @staticmethod
    def get_custom(w):
        word = input(f"Replace {w} with: ")
        return word
