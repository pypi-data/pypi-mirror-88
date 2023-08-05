from UnCodeGL.source import Source
from UnCodeGL.data_structures.trie import Trie
from UnCodeGL.data_structures.encoder import Encoder
from UnCodeGL.data_structures.huffman_generator import Huffman_Generator
import re

class Code:
    """
    Core class for Coding and Decoding.
    It has integrated core metrics to it.

    To create a new Code you need to pass the rule
    for the code as a dictionary. 


    Attributes:
        arity:
            An integer representing the code arity
        code_alphabet:
            A set containing the code alphabet
        source_alphabet:
            A set containing the source alphabet
    """
    __code_trie = None
    __source_trie = None
    __uniquely_decodable = None

    def __init__(self, code_dictionary):
        """"
        Initiates the class using a code dictionary
        """
        self.code = validate_dictionary(code_dictionary)
        self.code_alphabet = set()
        self.source_words = set()
        self.code_words = set()
        self.source_alphabet = set()
        self.__reverse_code ={}
        coding_output =  ''
        source_input = ''
        for key, value in self.code.items():
            self.source_words.add(key)
            coding_output += value
            source_input += key
            self.code_words.add(value)
            self.__reverse_code[value] = key
        for simbol in coding_output:
            self.code_alphabet.add(simbol)
        for simbol in source_input :
            self.source_alphabet.add(simbol)
        self.arity = len(self.code_alphabet)

        if self.is_prefix() :
            self.__decoder = Encoder(self.code_alphabet, self.__reverse_code)
        self.__encoder = Encoder(self.source_alphabet, self.code)
        
    def get_arity(self):
        """Returns arity of the code
        
        Return:
            Integer value of the arity
        """
        return self.arity

    def is_prefix(self):
        """
            Uses a Trie data structure to determine
            if the code is prefix

            Returns:
                A boolean True if the code is prefix, False
                otherwise
        """
        return self.get_code_trie().is_prefix()

    @staticmethod
    def kraft_inequality_metric(words_length, arity):
        """
        Calculates Kraft Inequality for given word lengths
        
        Measures Kraft Inequality Metric defined as 

        .. math::
            \sum_{i} r^{-l_i} 

        where r means arity, and l sub i the length of 
        the ith word
        
        Also returns if an instantaneous code can be made with said words

        Typical Usage:

        .. highlight:: python
        .. code-block:: python

            >>> metric, can_be_inst = kraft_inequality_metric(words_length=[4,4,3,6],arity=2)
            >>> print(metric, can_be_inst)
            0.265625 True
            
            
        Args:
            words_length:
                An list with the length of the words
            arity:
                Arity of the code

        Returns:
            metric , can_be_instantaneous.
            Kraft Inequality metric.
            A boolean refering to whether or not a code
            with this word lenghts and arity exists.
            This is dependant on the metric being less than 1
        """
        
        if arity == None:
            raise Exception('arity can not be null')
        if type(arity) != int :
            raise Exception('arity must be an int')
        if words_length == None:
            raise Exception('words_length can not be null')
        
        metric = 0.0
        epsilon = 0.00001
        for l in words_length:
            metric += float(arity)**float(-l)
        return metric, metric + epsilon < 1

    
    def get_code_trie(self):
        """
            Returns a Trie data structure 
            from the words in the code
        """
        if self.__code_trie == None:
            self.__code_trie = Trie(self.code_alphabet)
            for word in self.code_words:
                self.__code_trie.insert(word)
        return self.__code_trie
    
    def __repeated_C_n(self):
            """True if C_n has began a cycle, False otherwise"""
            if len(self.__C_n ) <= 3:
                return False
            for i in range(1,len(self.__C_n)-1) :
                if self.__C_n[-1] == self.__C_n[i] and self.__C_n[-2] == self.__C_n[i-1] :
                    return True
            return False

    def is_uniquely_decodable(self):
        """Returns boolean specifying whether or not is uniquely decodable
        
        For the code to be uniquely decodable means that the function 
        code that takes a string from a the source and codifies it
        is inyective. 

        Returns:
            True if the code is uniquely decodable, False otherwise
        """
        if self.__uniquely_decodable == None :
            self.__C_n = [self.code_words]
            trie_0 = Trie(self.code_alphabet , words = self.code_words )
            while True:
                new_words = set()
                trie_n = Trie(self.code_alphabet , words = self.__C_n[-1])

                for word_i in self.__C_n[-1]:
                    for new_word in trie_0.complete_word(word_i) :
                        new_words.add(new_word)
                for word_i in self.__C_n[0]:
                    for new_word in trie_n.complete_word(word_i) :
                        new_words.add(new_word)
                if new_words == set() or self.__repeated_C_n() :
                    break
                self.__C_n.append(new_words)
            
            self.__C_infty = set()
            for i in range(1,len(self.__C_n)) :
                for word in self.__C_n[i] :
                    self.__C_infty.add(word)

            self.is_uniquely_decodable = len( self.__C_infty & self.__C_n[0] ) == 0
            
        return self.is_uniquely_decodable
            
    def encode(self, sentence):
        """"Encodes a given sentence
        """
        
        return self.__encoder.encode_sentence(sentence)
    
    def __encode_brute_force(self, sentence):
        """Encodes a given sentence using bruteforce
        """
        encoding = ''
        curr_idx = 0
        sentence_length = len(sentence)
        while curr_idx < sentence_length :
            advance = False
            for word in self.source_words :
                if re.match('^'+word , sentence[curr_idx:]) :
                    curr_idx += len(word)
                    encoding += self.code[word]
                    advance = True
                    break
            if not advance :
                raise Exception('No match found to encode {} '.format(sentence[curr_idx:]))
        return encoding
        
    def decode(self, sentence, get_any = True):
        """Decodes a given sentence, in case
        multiple outputs are possible it returns 
        any of them if the get_any flag is True. 
        
        Args:
            sentence:
                Sentence to be decoded. It must compel
                with the source alphabet.
            get_any:
                True by default. It gives a string when
                multiple answers are possible. When False
                it gives the answer in a set of possible answers. 
        
        Returns:
            A string with the decoded sentence
        """
        if self.is_prefix() :
            return self.__decoder.encode_sentence(sentence)
        result = self.__decode_brute_force(sentence)

        if len(result) == 0 :
            raise Exception ('No decoding possible')

        if get_any:
            return result.pop()
        return result
    
    def __decode_brute_force(self, sentence, curr_idx = 0):
        results = set()
        # Base Case
        if curr_idx >= len(sentence):
            return ['']
        
        for word in self.code_words :
            if re.match('^'+word , sentence[curr_idx:]) :
                for result in self.__decode_brute_force(
                    sentence,
                    curr_idx = curr_idx + len(word),
                    ) :
                    results.add(self.__reverse_code[word] + result)
        return results

    def get_word_length(self, source):
        """Gets the average word lenght of the code
        for a given Source

        Args:
            source:
                A source of type Source
        
        Returns:
            A float with the value of the word lenght of 
            the code for the given source.
        """
        if type (source) != Source :
            raise Exception('source must be of type source')
        word_length = 0.0
        for word, probability in source.dictionary.items() :
            if word not in source.dictionary :
                raise Exception ('{} not part of the code source '.format(word))
            
            word_length += probability * float(len(self.code[word]))
        return word_length

    @staticmethod
    def make_huffman_code(source, code_alphabet={'0','1'}):
        """Generates an optimal Huffman Code
        
        Args:
            source:
                A source of type Source
            code_alphabet:
                Iterable with the alphabet. The items should be
                of type str
        Returns:
            Optimal huffman code for the given source and
            with arity of the given code_alphabet
        """
        if type (source) != Source :
            raise Exception('source must be of type source')

        base_nodes  = [(probability, word) for word,probability in source.dictionary.items()]
        arity = len(code_alphabet)

        while len(base_nodes)  % arity != 1 :
            base_nodes.append((float(0), ''))
        huffman = Huffman_Generator(simbols = code_alphabet, base_nodes = base_nodes, arity = len(code_alphabet))

        return Code(huffman.make_huffman_code())


def validate_dictionary(code_dictionary):
    """
    Validates that a given dictionary is good to use as a code
    """
    if type(code_dictionary) != dict :
        raise Exception('code_dictionary must be of type dict')

    for key,value in code_dictionary.items():
        if type(key) != str :
            raise Exception('code_dictionary keys must be of type str')
        if type(value) != str : 
            raise Exception('code_dictionary keys must be of type str')
    return code_dictionary

        