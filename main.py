#! /usr/bin/python3.1

import tkinter as tk
import menus
import random
import pickle
import os
from textbox import EnhancedTextBox          
from tkinter import messagebox
from tkinter import font
from tkinter.filedialog import askopenfilename 
from tkinter.filedialog import asksaveasfilename
from tkinter import colorchooser

#Fix alignment of scrollbars
#fix tab display size when not using spaces
#not showing dialog when opening new file after modifying current file

class Application(tk.Tk):
    wrap = False
    menurow = 0
    textboxrow = 1
    textboxcol = 0
    scrollcol = 1
    dirty = False
    linesdeleted = True
    oldr = 0
    
    spaces = None
    magic = None
    tabsize = None
    
    status = None
    line = None
    column = None
    autoindent = None
    
    controlSize = None
    controlType = None
    predColors = None
    
    currentfile = None


    def __init__(self, master=None):
        """Initialize the frame, creating the text area and menus, 
        plus any other necessary widgets."""
        
        tk.Tk.__init__(self, master)   
        self.grid()
        
        self.controlSize = tk.IntVar()
        self.controlSize.set(12)
        self.controlType = tk.StringVar()
        self.controlType.set("Consolas")
        self.predColors = tk.StringVar()
        self.autoindent = tk.IntVar()
        
        self.spaces = tk.IntVar()
        self.magic = tk.IntVar()
        self.tabsize = tk.IntVar()
        self.tabsize.set(8)
        
        self.createMenu()
        self.predColors.set("BlackOnWhite")
        
        self.createWidgets()
        
        self.columnconfigure(0,weight=1)
        self.rowconfigure(1,weight=1)
        
        if(os.path.isfile("app.pickle")):
            self.unpickle()
            self.colorPredefined()
            self.updateTabStyle()
        
        self.setFontType()
        self.setFontSize()

        
    def createWidgets(self):
        self.status = tk.Frame(self,takefocus=False)
        
        self.line = tk.Label(self.status, text="Line: 1 ")
        self.line.pack(side=tk.LEFT,fill=tk.Y)
        self.column = tk.Label(self.status, text="Column: 1 ")
        self.column.pack(side=tk.LEFT,fill=tk.Y)
        
        self.status.grid(sticky="ew",row=3,column=0)
        
        #Width and height are 1 so resizing doesn't get rid of the scrollbar
        self.text = EnhancedTextBox(master=self,width=10,height=10,
            wrap=tk.NONE,undo=True,autoseparators=True,
            font=(self.controlType.get(),self.controlSize.get()))
        self.vertscroll = tk.Scrollbar(master=self)
        self.vertscroll.config(command=self.text.yview)
        self.horizscroll = tk.Scrollbar(master=self,orient=tk.HORIZONTAL)
        self.horizscroll.config(command=self.text.xview)
        self.text.config(yscrollcommand=self.vertscroll.set)
        self.text.config(xscrollcommand=self.horizscroll.set)
        
        self.vertscroll.grid(column=1,row=1,sticky="ns")
        self.text.grid(column=0,row=1,sticky="nesw")
        self.horizscroll.grid(column=0,row=2,sticky="ew")
        
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
            self.dirty = False
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
        s = "Line: %s " % line
        self.line.configure(text=s)
        s = "Column: %s " % (int(column) + 1)
        self.column.configure(text=s)
        
    def modified(self,event=None):
        self.dirty = self.dirty ^ True
        
    def setFontSize(self, size=None):
        if(size == None):
            self.setFontSize(self.controlSize.get())
        else:
            self.text.setFont((self.controlType.get(),size))
    
    def setFontType(self, type=None):
        if(type == None):
            self.setFontType(self.controlType.get())
        else:
            self.text.setFont((type,self.controlSize.get()))
    
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
    
    def tabLevel(self,event=None):
        if(self.autoindent.get()):
            line,c = self.text.getCursorPos()
            indent = self.text.getIndent(line) + "\n"
            index = "%s.0" % str(int(line)+1)
            self.text.insert(index,indent)
            self.text.mark_set("insert", "%d.%d" % (int(line)+1, int(c)+1))
            return 'break'
    
    def copy(self, event=None):
        self.text.copy()
    
    def cut(self, event=None):
        self.text.cut()

    def paste(self, event=None):
        self.text.paste()
        
    def lineNumbers(self):
        pass
    
    def colorPredefined(self):
        if(self.predColors.get() == "WhiteOnBlack"):
            textColor = (1,"#ffffff")
            backColor = (1,"#000000")
        elif(self.predColors.get() == "BlackOnWhite"):
            textColor = (1,"#000000")
            backColor = (1,"#ffffff")
        elif(self.predColors.get() == "GreenOnBlack"):
            textColor = (1,"#00ff00")
            backColor = (1,"#000000")
        elif(self.predColors.get() == "ScarletOnGrey"):
            textColor = (1,"#ff0000")
            backColor = (1,"#bebebe")
        elif(self.predColors.get() == "WhiteOnBlue"):
            textColor = (1,"#ffffff")
            backColor = (1,"#0000ff")
        elif(self.predColors.get() == "YellowOnBlack"):
            textColor = (1,"#ffff00")
            backColor = (1,"#000000")
        else:
            textColor = None
            backColor = None
            
        self.setTextColor(textColor)
        self.setBackgroundColor(backColor)
        
    def setTextColor(self,color=None):
        if(color == None):
            self.predColors.set("Garbage")
            color = colorchooser.askcolor(title="Set Text Color")
        if(color[1] != None):
            self.text.configure(foreground=color[1])
            
    def setBackgroundColor(self,color=None):
        if(color == None):
            self.predColors.set("Garbage")
            color = colorchooser.askcolor(title="Set Background Color")
        if(color[1] != None):
            self.text.configure(background=color[1])
    
    def updateDisplay(self,event=None):
        self.getPosition()
        #self.lineNumbers()
        
    def newFile(self,event=None):
        if(self.dirty):
            mod = messagebox.askquestion(title="Save?", 
                message="File Modified, Save Before Opening New File?", default="yes")
            if(mod == "yes"):
                self.saveCurrent()
        self.text.clear()
        self.currentfile = None
        
    def pickle(self):
        output = (  
                    self.wrap,
                    self.menurow,
                    self.textboxrow, 
                    self.textboxcol,
                    self.scrollcol,
                    self.oldr,
                    self.spaces.get(),
                    self.magic.get(),
                    self.tabsize.get(),
                    self.controlSize.get(),
                    self.controlType.get(),
                    self.predColors.get(),
                    self.autoindent.get()
                )
        
        try:
            f = open("app.pickle","wb")
            pickle.dump(output,f)
        except Exception as e:
            print("Problem storing configuration.")
            print(e)
    
    def unpickle(self):
        try:
            f = open("app.pickle","rb")
            input = pickle.load(f)
            
            self.wrap = input[0]
            self.menurow = input[1]
            self.textboxrow = input[2]
            self.textboxcol = input[3]
            self.scrollcol = input[4]
            self.oldr = input[5]
            self.spaces.set(input[6])
            self.magic.set(input[7])
            self.tabsize.set(input[8])
            self.controlSize.set(input[9])
            self.controlType.set(input[10])
            self.predColors.set(input[11])
            self.autoindent.set(input[12])
            
        except Exception as e:
            print("Problem restoring configuration.")
            print(e)
    
    def quit(self, event=None):
        self.pickle()
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
    app.text.bind("<KeyPress>", app.updateDisplay)
    app.text.bind("<KeyRelease>", app.updateDisplay)
    app.text.bind("<ButtonRelease>", app.updateDisplay)
    app.text.bind("<<Modified>>", app.modified)
    app.text.bind("<Shift-Tab>",app.shiftTab)
    app.text.bind("<Tab>", app.insertTab)
    app.text.bind("<Return>",app.tabLevel)
    app.bind("<Control-n>", app.newFile)
    app.geometry('800x600+0+0')
    app.config(menu=app.menu)
    app.mainloop()
else:
    print("Main is intended to be run, not imported.")
    
