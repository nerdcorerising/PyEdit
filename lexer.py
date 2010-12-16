import tkinter as tk

class Lexer:
    """A flexible lexer that will parse the language according
    to the grammar provided."""
    
    __lexfile = None
    __ready = False
    __buffer = None
    __color = None
    
    def __init__(self,lex=None):
        if(lex != None):
            self.__lexfile = lex
        
    def insert(self,line):
        if(self.__lexfile == None):
            self.__ready = True
            self.__buffer = line
        
    def ready(self):
        return self.__ready
    
    def dispense(self):
        """Returns the current word and the color it should be."""
        self.__ready = False
        tempbuff, tempcolor = self.__buffer, self.__color
        self.__buffer, self.__color = (None, None)
        return (tempbuff, tempcolor)
    
    
    
if __name__ == "__main__":
    print ("Lexer is a library.")