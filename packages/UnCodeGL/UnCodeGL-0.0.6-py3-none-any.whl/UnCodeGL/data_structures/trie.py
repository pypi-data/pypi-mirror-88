import queue

class TrieNode :
    def __init__(self, simbols): 
        self.children = {}
        for simbol in simbols:
            self.children[simbol]=None
  
        # is_end_of_word is True if node represent the end of the word 
        self.is_end_of_word = False

class Trie:
    """
    Data structure Trie.
    See more in :
    https://en.wikipedia.org/wiki/Trie#:~:text=In%20computer%20science%2C%20a%20trie,the%20keys%20are%20usually%20strings.
    """

    def __init__(self, simbols, **kwargs):
        """"Inits the Trie
        
        If given optional parameter words, then it
        creates a Trie with given words inserted.
        """
        self.simbols = simbols
        self.root = self.getNode() 

        if  'words' in kwargs :
            for word in kwargs['words'] :
                self.insert(word)
  
    def getNode(self): 
        """Returns new trie node (initialized to NULLs) """
        return TrieNode(self.simbols)


    def insert(self, word): 
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
        current_node.is_end_of_word = True

    def search(self, word): 
        """  
        Search key in the trie 
        Returns true if key presents  
        in trie, else false 
        """
        current_node = self.root 
        for simbol in word: 
            if not current_node.children[simbol]: 
                return False
            current_node = current_node.children[simbol] 
  
        return current_node != None and current_node.is_end_of_word

    def is_prefix(self):
        """
        Search for prefixes of words
        """
        q = queue.Queue()
        q.put(self.root)
        while not q.empty() :
            current_node = q.get()
            has_childs = False
            for simbol in self.simbols:
                if current_node.children[simbol]  != None:
                    has_childs=True
                    q.put(current_node.children[simbol])
            if has_childs and current_node.is_end_of_word:
                return False

        return True
    
    def complete_word(self, word):
        """Finds if there is a way to complete the word
        to make it belong to the Trie
        """
        result  =  set()

        current_node = self.root 
        for simbol in word: 
            if not current_node.children[simbol]: 
                return result
            current_node = current_node.children[simbol] 
  
        if current_node == None :
            return result
        q = queue.Queue()
        q.put( (current_node, "") )
        while not q.empty() :
            current_node, acum_str = q.get()
            for simbol in self.simbols:
                if current_node.children[simbol]  != None:
                    q.put((current_node.children[simbol], acum_str + simbol))
            if acum_str != "" and current_node.is_end_of_word:
                result.add(acum_str)

        return result