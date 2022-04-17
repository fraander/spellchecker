import string
from Dictionary import Dictionary


# Plan

# read a char
#   if not whitespace or punctuation:
#       add another letter to the buffer
#   else (is end of word)
#       check against dictionary
#           if in dictionary:
#               write to new file
#           else
#               ask for alternatives

# TODO: cannot handle whitespace at end of file right now

class GrammarChecker:
    def __init__(self, filename="doc.txt"):
        dictionary = Dictionary().data

        with open("output.txt", 'w') as o:
            with open(filename, 'r') as f:
                buffer = ""

                while True:
                    # read by character
                    c = f.read(1)

                    if not c:  # if eof, break
                        break

                    if c not in string.punctuation and c not in string.whitespace and buffer[:-1] + c != "\n":  # if
                        # not
                        # whitespace
                        buffer += c  # increase the buffer
                    else:  # if there is whitespace (new word)buffer

                        w = buffer

                        w = w.replace('=', '')
                        w = w.replace('\n', '')
                        w = w.replace('+', '')
                        w = w.replace('^', '')
                        w = w.replace('.', '')
                        w = w.replace('&', '')
                        w = w.replace('#', '')
                        w = w.replace(':', '')
                        w = w.replace('’', "'")

                        w = w.lower()

                        word_in = False
                        if w in dictionary.keys() or w in string.whitespace:
                            word_in = True
                        else:
                            if len(w) > 2 and w[-2:] == "'s" and w[:-2] in dictionary.keys():
                                word_in = True
                            elif len(w) > 2 and w[-2:] == "s'" and w[:-2] in dictionary.keys():
                                word_in = True
                            elif len(w) > 1 and w[-1] == "s" and w[:-1] in dictionary.keys():
                                word_in = True

                        if not word_in:
                            options = Dictionary().find_similar(w)
                            options = options[::-1]

                            print("**", buffer, "**", sep="")
                            for index, option in enumerate(options):
                                print("[", index, "]", option)
                            print("[" ,len(options), "]", "!! Custom Word !!")

                            opt_in = -1
                            while opt_in == -1:
                                opt_in = input("Which word would you like to use? [#] ")

                                try:
                                    opt_in = int(opt_in)

                                    if opt_in == len(options):
                                        buffer = GrammarChecker.get_custom(w)
                                    else:
                                        buffer = options[opt_in][0]
                                except ValueError:
                                    opt_in = -1
                                    print("Invalid input. Try again.")
                                except KeyError:
                                    opt_in = -1
                                    print("Invalid input. Try again.")
                                except IndexError:
                                    opt_in = -1
                                    print("Invalid input. Try again.")

                        if buffer[:-1] + c == "\n":
                            o.write(buffer + "\n")
                        else:
                            if word_in:
                                o.write(buffer + c)
                                print(buffer + c, end="")
                            else:
                                o.write("**" + buffer + "**" + c)
                                print(buffer + c, end="")

                        buffer = ""  # when done, clear the buffer

    @staticmethod
    def get_custom(w):
        word = input(f"Replace {w} with: ")
        return word
