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
        #Flush is important - small files will never write
        #to disk without it
        output.flush()
        
    def getCharWordCount(self):
        block = self.get(1.0, tk.END)
        c = len(block) - 1
        block = block.split()
        w = len(block)
        return (w,c)
        
    def setFont(self, f):
        self.configure(font=f)
        
    def copy(self, event=None):
        self.clipboard_clear()
        text = self.get("sel.first", "sel.last")
        self.clipboard_append(text)
    
    def cut(self, event=None):
        self.copy()
        self.delete("sel.first", "sel.last")

    def paste(self, event=None):
        text = self.selection_get(selection='CLIPBOARD')
        self.insert('insert', text)
        
    def getCursorPos(self):
        return self.index('insert').split('.')
        
    def totalLines(self):
        #get the index of the last character, split it on '.' to get
        #the line number, then return the int of the first index. The
        #minus one is because of the way the index works
        return int(self.index(tk.END).split(".")[0]) - 1
        
    def magicTab(self,spaces=4,delete=False):
        line, column = self.getCursorPos()
        index = "%s.0" % str(line)
        if(delete):
            if(spaces <= -1):
                if(self.get(index) == "\t"):
                    self.delete(index)
            else:
                endindex = "%s.%s" % (line, str(spaces))
                text = self.get(index,endindex)
                if(text == ' ' * spaces):
                    self.delete(index,endindex)
                elif(text[0] == ' '):
                    range = 0;
                    while(range < len(text) and text[range] == ' '):
                        range = range + 1
                    endindex = "%s.%s" % (line,str(range))
                    self.delete(index,endindex)
        else:
            #shift the whole line over one tab, regardless of where the cursor is in the line
            if(spaces <= -1):
                self.insert(index, '\t')
            else:
                self.insert(index, ' ' * spaces)
        
    def insertTab(self,spaces):
        if(spaces <= -1):
            self.insert(self.index('insert'),'\t')
        else:
            self.insert(self.index('insert'),' ' * spaces)
        
if __name__ == "__main__":
    print ("TextBox is a library.")