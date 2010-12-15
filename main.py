import tkinter
import menus
from textbox import EnhancedTextBox          
from tkinter.filedialog   import askopenfilename   

class Application(tkinter.Tk):
    wrap = False
    menurow = 0
    textboxrow = 1
    textboxcol = 0
    scrollcol = 1
    
    currentfile = None


    def __init__(self, master=None):
        """Initialize the frame, creating the text area and menus, 
        plus any other necessary widgets."""
        
        tkinter.Tk.__init__(self, master)   
        self.grid()
        
        self.createWidgets()
        self.createMenu()
        
        
    def createWidgets(self):
        #Width and height are 1 so resizing doesn't get rid of the scrollbar
        self.text = EnhancedTextBox(master=self,width=10,height=10,wrap=tkinter.NONE)
        self.vertscroll = tkinter.Scrollbar(master=self)
        self.vertscroll.config(command=self.text.yview)
        self.horizscroll = tkinter.Scrollbar(master=self,orient=tkinter.HORIZONTAL)
        self.horizscroll.config(command=self.text.xview)
        self.text.config(yscrollcommand=self.vertscroll.set)
        self.text.config(xscrollcommand=self.horizscroll.set)
        
        #self.vertscroll.grid(column=self.vertscrollcol,row=self.textboxrow,sticky="ns")
        #self.text.grid(column=self.textboxcol,row=self.textboxrow)
        
        self.horizscroll.pack(side=tkinter.BOTTOM, fill=tkinter.X)
        self.text.pack(side=tkinter.LEFT,fill=tkinter.BOTH,expand=tkinter.YES)
        self.vertscroll.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        
    def createMenu(self):
        """Create the menu widget. It is rather long and messy 
        to add all of the options, so it is split into functions."""
        
        self.menu = tkinter.Menu(master=self)
        self.menu.add_cascade(label="File", menu=menus.createFileMenu(self.menu))
        self.menu.add_cascade(label="Edit", menu=menus.createEditMenu(self.menu))
        self.menu.add_cascade(label="Options", menu=menus.createOptionsMenu(self.menu))
        
    def openFile(self):
        filename = askopenfilename()
        
        if(filename):
            self.currentfile = open(filename, "r")
            self.text.displayFile(self.currentfile)
        
    
    def wordWrap(self):
        """Right now, this word wraps the whole text once 
        when pressed. Plans for the future are to have it 
        be an option that will keep word wrapping on."""
        
        self.wrap = self.wrap ^ True
        
        if(self.wrap):
            self.text.tag_config("SEL",wrap=tkinter.WORD)
        else:
            self.text.tag_config("SEL",wrap=tkinter.NONE)


app = Application()                    
app.title("PyEdit") 
app.geometry('800x600+0+0')
app.config(menu=app.menu)
app.mainloop()    