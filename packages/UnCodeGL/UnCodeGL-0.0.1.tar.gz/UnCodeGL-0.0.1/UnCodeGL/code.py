import UnCodeGL.source

class Code:
    """
    Core class for Coding and Decoding.
    It has integrated core metrics to it.

    To create a new Code you need to pass the rule
    for the code as a dictionary. 
    """

    def __init__(code_dictionary):
        """"
        Initiates the class using a code dictionary
        """
        self.D = 2
        self.source_alphabet = ['a','b']
        self.source = ['1','2']

        