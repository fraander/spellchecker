class PathManager:
    """
    Handles file path and makes it accessible to other classes
    """

    def __init__(self):
        self.read_filename = PathManager.get_valid_filepath()
        self.write_filename = "edited+" + self.read_filename

    @staticmethod
    def get_valid_filepath():
        """
        Ask user for file path and validate it
        :return: valid filepath
        """
        fn = -1
        while fn == -1:
            try:
                fn = input("What is the name of the file you'd like to read from? ")
                f = open(fn, 'r')
                f.close()
            except OSError:
                print("Invalid file name. Try a different one.")
                fn = -1

        return fn