import queue


class Huffman_Node :
    def __init__(self, simbols, probability, word=None): 
        self.children = {}
        for simbol in simbols:
            self.children[simbol]=None
        self.probability = probability
        self.assigned_word = word

class Huffman_Generator :
    """
    Utility class to generate Huffman Code
    """
    def __init__(self, simbols, base_nodes , arity):
        self.base_nodes = base_nodes
        self.simbols = [simbol for simbol in simbols]
        self.arity = arity
    
    def make_node(self , probability, word = None): 
        """Returns new node (initialized to NULLs) """
        return Huffman_Node(self.simbols, probability, word=word)
    
    def make_huffman_code(self):
        nodes = [self.make_node(prob, word = word) for prob,word in self.base_nodes]
        # Huffman Algorithm
        while len(nodes) > 1 :
            nodes.sort(key=lambda x : x.probability)
            new_node = self.make_node(0.0)
            new_prob = 0.0
            for i in range(self.arity):
                if nodes[i].probability > 0.0 :
                    new_node.children[self.simbols[i]] = nodes[i]
                new_prob += nodes[i].probability
            new_node.probability = new_prob
            nodes.append(new_node)
            nodes = nodes[self.arity:]
        # Make the dictionary with BFS
        self.root = nodes[0]
        result = {}
        q = queue.Queue()
        q.put((self.root,''))
        while not q.empty() :
            current_node , acum = q.get()
            if current_node.assigned_word :
                result[current_node.assigned_word] = acum 
            for simbol in self.simbols:
                if current_node.children[simbol]  != None:
                    q.put((current_node.children[simbol], acum + simbol))

        return result