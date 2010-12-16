import tkinter as tk
from lexer import Lexer

class EnhancedTextBox(tk.Text):
    lexer = None
    
    def __init__(self, master=None, lex=None,**kw):
        tk.Text.__init__(self,master,**kw)
        self.lexer = Lexer(lex)
        
    def displayFile(self, file):
        """Given a file opened for reading, will 
        display the contents on the screen."""
        
        self.delete(1.0, tk.END)
        
        for line in file:
            self.lexer.insert(line)
            while(self.lexer.ready()):
                line,color = self.lexer.dispense()
                self.insert(tk.END, line)
    
    def write(self,output):
        """Going to attempt writing the whole file in one
        shot. Is this a good idea? Only time will tell..."""
        
        block = self.get(1.0, tk.END)
        #get rid of trailing newline from string conversion
        block = block[:len(block) - 1]
        output.write(block)
        output.flush()
        
    def getCharWordCount(self):
        block = self.get(1.0, tk.END)
        c = len(block)
        block = block.split()
        w = len(block)
        return (w,c)
        
    def setFont(self, f):
        this.configur(font=f)
        
if __name__ == "__main__":
    print ("TextBox is a library.")