class EncoderNode :
    def __init__(self, simbols): 
        self.children = {}
        for simbol in simbols:
            self.children[simbol]=None
  
        self.assigned_word = None

class Encoder:
    """
    Encoder based on Trie.
    See more in :
    https://en.wikipedia.org/wiki/Trie#:~:text=In%20computer%20science%2C%20a%20trie,the%20keys%20are%20usually%20strings.
    """

    def __init__(self, simbols, dictionary):
        """"Inits the encoder
        """
        self.simbols = simbols
        self.root = self.getNode() 

        for key, values  in dictionary.items() :
            self.insert(key, values)
    
    def getNode(self): 
        """Returns new trie node (initialized to NULLs) """
        return EncoderNode(self.simbols)
        
    def insert(self, word, assigned_word): 
        """
        If not present, inserts key into trie 
        If the key is prefix of trie node,  
        just marks leaf node 
        """
        current_node = self.root 
        for current_simbol in word: 
            # if current character is not present 
            if not current_node.children[current_simbol]: 
                current_node.children[current_simbol] = self.getNode() 
            current_node = current_node.children[current_simbol] 
  
        # mark last node as leaf 
        current_node.assigned_word = assigned_word
    
    def encode_sentence(self, sentence):
        """
        Returns string with the given word to search.
        None if invalid seach
        """
        current_node = self.root 
        encoding = ''

        for simbol in sentence:
            # When it finds a word it encodes it inmediatly         
            if not current_node.children[simbol]: 
                return None
            current_node = current_node.children[simbol] 
            if current_node.assigned_word != None :
                encoding += current_node.assigned_word
                current_node = self.root
                continue
  
        return encoding
