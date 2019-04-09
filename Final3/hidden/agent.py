

class Agent:
 """ class deffinissant les agents  """"

    def _init_(self):
        """de base type =1"""
        self.type = 1
        self.pos = e1
        self.Nodes= {1,2,3,4}
        self.vitesse = 50
        self.acceleration = 0
    
    def _init_(self,int type ):
        """de base type =1"""
        self.type = type
        self.Nodes= {1,2,3,4}
        self.pos = e1
        self.vitesse = 50
        self.acceleration = 0
    
    def _init_(self, type, node):
        """de base type =1"""
        self.type = type
        self.pos = node
        self.Nodes= {1,2,3,4}
        self.vitesse = 50
        self.acceleration = 0
    

    def _init_(self, type, node, path[]):
        """de base type =1"""
        self.type = type
        self.pos = node
        self.Nodes= {path}
        self.vitesse = 50
        self.acceleration = 0