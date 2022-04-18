class FileManager:
    """
    Handles file path and makes it accessible to other classes
    """
    def __init__(self):
        self.filename = FileManager.validate_filepath()

    @staticmethod
    def validate_filepath():
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
