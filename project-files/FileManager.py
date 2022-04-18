class FileManager:
    def __init__(self):
        fn = -1
        while fn == -1:
            try:
                fn = input("What is the name of the file you'd like to read from? ")
                f = open(fn, 'r')
                f.close()
            except OSError:
                print("Invalid file name. Try a different one.")
                fn = -1

        self.fn = fn