import tkinter as tk

class Lexer:
    """A flexible lexer that will parse the language according
    to the grammar provided."""
    
    __ready = False
    __buffer = None
    
    def __init__(self,lex=None):
        pass
        
    def insert(self,line):
        self.__ready = True
        self.__buffer = line
        
    def ready(self):
        return self.__ready
    
    def dispense(self):
        """Returns the current word and the color it should be."""
        self.__ready = False
        return self.__buffer, None
    
    
    
if __name__ == "__main__":
    print ("Lexer is a library.")