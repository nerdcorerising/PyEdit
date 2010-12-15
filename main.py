import tkinter
import menus

class Application(tkinter.Frame):              
    def __init__(self, master=None):
        """Initialize the frame, creating the text area and menus, 
        plus any other necessary widgets."""
        
        tkinter.Frame.__init__(self, master)   
        self.grid()
        self.wrap = False
        self.menurow = 0
        self.textboxrow = 1
        self.textboxcol = 0
        self.scrollcol = 1
        self.createMenu()
        self.createWidgets()
        
        
    def createMenu(self):
        """Create the menu widget. It is rather long and messy 
        to add all of the options, so it is split into functions."""
        
        self.menu = tkinter.Menu(master=self)
        self.menu.add_cascade(label="File", menu=menus.createFileMenu(self.menu))
        self.menu.add_cascade(label="Edit", menu=menus.createEditMenu(self.menu))
        self.menu.add_cascade(label="Options", menu=menus.createOptionsMenu(self.menu))
        
    def wordWrap(self):
        """Right now, this word wraps the whole text once 
        when pressed. Plans for the future are to have it 
        be an option that will keep word wrapping on."""
        
        self.wrap = True
        
    def createWidgets(self):
        self.text = tkinter.Text(master=self)
        self.scroll = tkinter.Scrollbar(master=self)
        self.scroll.config(command=self.text.yview)
        self.text.config(yscrollcommand=self.scroll.set)
        
        #self.scroll.grid(column=self.scrollcol,row=self.textboxrow,sticky="ns")
        #self.text.grid(column=self.textboxcol,row=self.textboxrow)
        self.text.pack(side=tkinter.LEFT, fill=tkinter.BOTH,expand=tkinter.YES)
        self.scroll.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        


app = Application()                    
app.master.title("PyEdit") 
app.master.config(menu=app.menu)
app.mainloop()    