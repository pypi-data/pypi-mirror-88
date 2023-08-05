class Source:
    """
    Class for Source. Contains a dictionary with the probabilities
    of each simbol it can generate

    Attributes:
        dictionary: 
            Dictionary of probabilities. The keys are the source simbols 
            and the values the probabilities

    Initialization can be done through dictionary or base_string
    but not both
        
    Can be initiated through a given dictionary
    that contains the simbols and the probabilities
    that each symbol occurs. 

    It can also be initiated with a base string that
    will count appearances and obtain probabilities.

    Either dictionary or base_string must be passed, not both

    Args:
        dictionary:
            A dictionary with the simbols and probabilities.
            The sum of the probabilities must be 1. 
        base_string:
            A string of the usual output of the source. It will
            be assumed that is a memoryless source
    """
    
    __alphabet = None

    def __init__(self, *args, **kwargs) :
        """
        Initializes the class
        """
        if 'base_string' in kwargs and (len(args) == 1 or 'dictionary' in kwargs):
            raise Exception ('dictionary and base_string are mutually exclusive parameters')
        if 'base_string' in kwargs :
            self.dictionary = make_dictionary_from_str(kwargs['base_string'])
            return
        if len(args) > 0 :
            self.dictionary = verify_dictionary(args[0])
            return
        if 'dictionary' in kwargs :
            self.dictionary = verify_dictionary(kwargs['dictionary'])
            return
        raise Exception ('No dictionary or base_string found to make the source')
    
    def get_alphabet(self):
        """
        Returns list with simbols of the source
        """
        if self.__alphabet == None :
            self.__alphabet = set()
            for simbol in self.dictionary :
                self.__alphabet.add(simbol)
        return self.__alphabet
    
    def get_simbol_prob(simbol):
        """
        Returns probability for a simbol
        """
        default = 0.0
        if simbol in self.dictionary:
            return dictionary[simbol]
        return default

    def get_entropy(self):
        """Calculates entropy of the source

        Entropy is given by 

        .. math::
                -\sum_{i} p(x_i)\log(p(x_i)) 
        
        Returns:
            Float with the value of the entropy.
        """
        total = 0.0


def make_dictionary_from_str(base_string):
    """Makes a dictionary with probabilities normalized"""
    dictionary = {}
    # Counting occurences
    for simbol in base_string:
        if simbol not in dictionary:
            dictionary[simbol] = 0
        dictionary[simbol] += 1
    # Normalizing
    for key,value in dictionary.items():
        dictionary[key] = float(value) / float(len(base_string))
    return dictionary

def verify_dictionary(dictionary):
    """Verify the sum of the probabilites is 1 to an epsilon"""
    total = 0.0
    epsilon = 0.00001
    for key,value in dictionary.items():
        total += float(value)
    if abs(total - 1.0) > epsilon :
        raise Exception ('dictionary probabilites does not add up to 1')
    return dictionary
    
        
        
