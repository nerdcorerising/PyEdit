import tkinter as tk
import menus
from textbox import EnhancedTextBox          
from tkinter.filedialog import askopenfilename 
from tkinter.filedialog import asksaveasfilename  

class Application(tk.Tk):
    wrap = False
    menurow = 0
    textboxrow = 1
    textboxcol = 0
    scrollcol = 1
    
    currentfile = None


    def __init__(self, master=None):
        """Initialize the frame, creating the text area and menus, 
        plus any other necessary widgets."""
        
        tk.Tk.__init__(self, master)   
        self.grid()
        
        self.createWidgets()
        self.createMenu()
        
        
    def createWidgets(self):
        #Width and height are 1 so resizing doesn't get rid of the scrollbar
        self.text = EnhancedTextBox(master=self,width=10,height=10,wrap=tk.NONE,undo=True)
        self.vertscroll = tk.Scrollbar(master=self)
        self.vertscroll.config(command=self.text.yview)
        self.horizscroll = tk.Scrollbar(master=self,orient=tk.HORIZONTAL)
        self.horizscroll.config(command=self.text.xview)
        self.text.config(yscrollcommand=self.vertscroll.set)
        self.text.config(xscrollcommand=self.horizscroll.set)
        
        #self.vertscroll.grid(column=self.vertscrollcol,row=self.textboxrow,sticky="ns")
        #self.text.grid(column=self.textboxcol,row=self.textboxrow)
        
        self.horizscroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.text.pack(side=tk.LEFT,fill=tk.BOTH,expand=tk.YES)
        self.vertscroll.pack(side=tk.RIGHT, fill=tk.Y)
        
    def createMenu(self):
        """Create the menu widget. It is rather long and messy 
        to add all of the options, so it is split into functions."""
        
        self.menu = tk.Menu(master=self)
        self.menu.add_cascade(label="File", menu=menus.createFileMenu(self.menu))
        self.menu.add_cascade(label="Edit", menu=menus.createEditMenu(self.menu))
        self.menu.add_cascade(label="Options", menu=menus.createOptionsMenu(self.menu))
        
    def openFile(self):
        """Opens a file and passes it to the EnhancedTextBox, which
        will display it's contents on the screen."""
        
        filename = askopenfilename()
        
        if(filename):
            try:
                self.currentfile = open(filename, "r")
                self.text.displayFile(self.currentfile)
            except:
                print ("Problem opening file", str(self.currentfile.name))
                self.currentfile = None
        else:
            self.currentfile = None
        
    def save(self,output):
        try:
            #Close the current file, we may be saving to it. Even if not, 
            #we don't want to overwrite it without closing.
            self.currentfile.close()
            
            outfile = open(output, "w")
            self.text.write(outfile)
            
            self.currentfile = outfile
        except Exception as e:
            print("Error saving file.")
            print(str(e))
        
    def saveCurrent(self):
        self.save(self.currentfile.name)
        
    def saveAs(self):
        filename = asksaveasfilename()
        self.save(filename)
    
    def undo(self):
        self.text.edit_undo()
        
    def redo(self):
        self.text.edit_redo()
    
    def wordWrap(self):
        """Toggle the word wrap on and off."""
        
        if(self.wrap):
            self.wrap = False
            self.text.configure(wrap=tk.NONE)
        else:
            self.wrap = True
            self.text.configure(wrap=tk.WORD)

if __name__ == "__main__":
    app = Application()                    
    app.title("PyEdit") 
    app.geometry('800x600+0+0')
    app.config(menu=app.menu)
    app.mainloop()
else:
    print("Main is intended to be run, not imported.")