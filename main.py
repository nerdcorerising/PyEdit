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
    
    status = None
    line = None
    column = None
    words = None
    characters = None
    
    font = ("Helvetica", 12)
    
    currentfile = None


    def __init__(self, master=None):
        """Initialize the frame, creating the text area and menus, 
        plus any other necessary widgets."""
        
        tk.Tk.__init__(self, master)   
        self.grid()
        
        self.createWidgets()
        self.createMenu()
        
        
    def createWidgets(self):
        self.status = tk.Frame(self)
        
        self.line = tk.Label(self.status, text="Line number: 0")
        self.line.pack(side=tk.LEFT,fill=tk.Y)
        self.column = tk.Label(self.status, text="Column number: 0")
        self.column.pack(side=tk.LEFT,fill=tk.Y)
        self.characters = tk.Label(self.status, text="Total characters: 0")
        self.characters.pack(side=tk.RIGHT,fill=tk.Y)
        self.words = tk.Label(self.status, text="Total words: 0")
        self.words.pack(side=tk.RIGHT,fill=tk.Y)
        
        self.status.pack(side=tk.BOTTOM,fill=tk.X)
        
        #Width and height are 1 so resizing doesn't get rid of the scrollbar
        self.text = EnhancedTextBox(master=self,width=10,height=10,
            wrap=tk.NONE,undo=True,autoseparators=True,font=self.font)
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
            if(self.currentfile != None and not self.currentfile.closed):
                self.currentfile.close()
            
            outfile = open(output, "w")
            self.text.write(outfile)
            
            self.currentfile = outfile
        except Exception as e:
            print("Error saving file.")
            print(str(e))
        
    def saveCurrent(self):
        if(self.currentfile == None):
            self.saveAs()
        else:
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
     
    def updateWordCount(self):
        word,char = self.text.getCharWordCount()
        s = "Total words: %s" % word
        self.words.configure(text=s)
        s = "Total characters: %s" % char
        self.characters.configure(text=s)
     
    def getPosition(self,event):
        """get the line and column number of the text insertion point"""
        line, column = app.text.index('insert').split('.')
        s = "Line number:%s " % line
        app.line.configure(text=s)
        s = "Column number:%s " % column
        app.column.configure(text=s)
        
    def setFontSize(self, size):
        self.font = (self.font[0], size)
        this.text.setFont(self.font)
    
    def setFontType(self, type):
        self.font = (type, self.font[1])
        this.text.setFont(self.font)
    
if __name__ == "__main__":
    app = Application()                    
    app.title("PyEdit") 
    app.text.bind("<KeyPress>", app.getPosition)
    app.text.bind("<KeyRelease>", app.getPosition)
    app.text.bind("<ButtonRelease>", app.getPosition)
    app.geometry('800x600+0+0')
    app.config(menu=app.menu)
    app.mainloop()
else:
    print("Main is intended to be run, not imported.")