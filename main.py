import tkinter as tk
import menus
from textbox import EnhancedTextBox          
from tkinter import messagebox
from tkinter import font
from tkinter.filedialog import askopenfilename 
from tkinter.filedialog import asksaveasfilename

#Fix alignment of scrollbars
#fix tab display size when not using spaces
#save options to file, reload on open

class Application(tk.Tk):
    wrap = False
    menurow = 0
    textboxrow = 1
    textboxcol = 0
    scrollcol = 1
    dirty = False
    
    spaces = None
    magic = None
    tabsize = None
    
    status = None
    line = None
    column = None
    
    controlSize = None
    controlType = None
    
    #What if a system doesn't have helvetica?
    font = ("Helvetica", 10)
    
    currentfile = None


    def __init__(self, master=None):
        """Initialize the frame, creating the text area and menus, 
        plus any other necessary widgets."""
        
        tk.Tk.__init__(self, master)   
        self.grid()
        
        self.createWidgets()
        
        self.controlSize = tk.IntVar()
        self.controlType = tk.StringVar()
        self.spaces = tk.IntVar()
        self.magic = tk.IntVar()
        self.tabsize = tk.IntVar()
        self.tabsize.set(8)
        
        self.createMenu()
        
        
    def createWidgets(self):
        self.status = tk.Frame(self,takefocus=False)
        
        self.line = tk.Label(self.status, text="Line number: 1")
        self.line.pack(side=tk.LEFT,fill=tk.Y)
        self.column = tk.Label(self.status, text="Column number: 1")
        self.column.pack(side=tk.LEFT,fill=tk.Y)
        
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
        
        self.horizscroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.text.pack(side=tk.LEFT,fill=tk.BOTH,expand=tk.YES)
        self.vertscroll.pack(side=tk.RIGHT, fill=tk.Y)
        
    def createMenu(self):
        """Create the menu widget. It is rather long and messy 
        to add all of the options, so it is split into functions."""
        
        self.menu = tk.Menu(master=self,takefocus=False)
        self.menu.add_cascade(label="File", menu=menus.createFileMenu(self.menu))
        self.menu.add_cascade(label="Edit", menu=menus.createEditMenu(self.menu))
        self.menu.add_cascade(label="Options", menu=menus.createOptionsMenu(self.menu,
            self.controlSize,self.controlType,font.families()))
        
    def openFile(self):
        """Opens a file and passes it to the EnhancedTextBox, which
        will display it's contents on the screen."""
        
        filename = askopenfilename()
        
        if(filename):
            try:
                self.currentfile = open(filename, "r")
                self.text.displayFile(self.currentfile)
                self.dirty = False
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
        if(filename != ""):
            self.save(filename)
    
    def undo(self):
        self.text.edit_undo()
        
    def redo(self):
        self.text.edit_redo()
    
    def wordWrap(self):
        """Toggle the word wrap on and off."""
        #Could use control variable here, simplify code
        if(self.wrap):
            self.wrap = False
            self.text.configure(wrap=tk.NONE)
        else:
            self.wrap = True
            self.text.configure(wrap=tk.WORD)
     
    def updateWordCount(self):
        word,char = self.text.getCharWordCount()
        s = "Total words: %s\nTotal characters: %s" % (word,char)
        messagebox.showinfo(title="Count",message=s)
        
    def getPosition(self,event=None):
        """get the line and column number of the text insertion point"""
        line, column = self.text.getCursorPos()
        s = "Line number: %s " % line
        self.line.configure(text=s)
        s = "Column number: %s " % (int(column) + 1)
        self.column.configure(text=s)
        
    def modified(self,event=None):
        self.dirty = self.dirty ^ True
        
    def setFontSize(self, size=None):
        if(size == None):
            self.setFontSize(self.controlSize.get())
        else:
            self.font = (self.font[0], size)
            self.text.setFont(self.font)
    
    def setFontType(self, type=None):
        if(type == None):
            self.setFontType(self.controlType.get())
        else:
            self.font = (type, self.font[1])
            self.text.setFont(self.font)
    
    def updateTabStyle(self):
        pass
        #self.text.configure(
    
    def insertTab(self,event=None):
        if(self.spaces.get() == 0):
            if(self.magic.get()):
                self.text.magicTab(-1)
            else:
                self.text.insertTab(-1)
        else:
            if(self.magic.get()):
                self.text.magicTab(self.tabsize.get())
            else:
                self.text.insertTab(self.tabsize.get())
        #Overrides default handler.
        return 'break'
    
    
    def shiftTab(self,event=None):
        if(self.spaces.get() == 0):
                self.text.magicTab(-1,delete=True)
        else:
                self.text.magicTab(self.tabsize.get(),delete=True)
        #Overrides default handler.
        return 'break'
    
    def copy(self, event=None):
        self.text.copy()
    
    def cut(self, event=None):
        self.text.cut()

    def paste(self, event=None):
        self.text.paste()
        
    def quit(self, event=None):
        if(not self.dirty):
            tk.Tk.quit(self)
        else:
            mod = messagebox.askquestion(title="Really Quit?", 
                message="File modified, quit anyways?", default="no")
            if(mod == "yes"):
                tk.Tk.quit(self)
        
if __name__ == "__main__":
    app = Application()                    
    app.title("PyEdit") 
    app.text.bind("<KeyPress>", app.getPosition)
    app.text.bind("<KeyRelease>", app.getPosition)
    app.text.bind("<ButtonRelease>", app.getPosition)
    app.text.bind("<<Modified>>", app.modified)
    app.text.bind("<Shift-Tab>",app.shiftTab)
    app.text.bind("<Tab>", app.insertTab)
    app.geometry('800x600+0+0')
    app.config(menu=app.menu)
    app.mainloop()
else:
    print("Main is intended to be run, not imported.")