import tkinter

class EnhancedTextBox(tkinter.Text):
    def __init__(self, master=None,**kw):
        tkinter.Text.__init__(self,master,**kw)
        
    def displayFile(self, file):
        """Given a file opened for reading, will 
        display the contents on the screen."""
        
        self.delete(1.0, tkinter.END)
        
        for line in file:
            self.insert(tkinter.END, line)