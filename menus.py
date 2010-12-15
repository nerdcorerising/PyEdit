import tkinter as tk

def createFileMenu(master):
    filemenu = tk.Menu(master, tearoff=0)
    filemenu.add_command(label="Open File", command=master.master.openFile)
    filemenu.add_command(label="Save", command=master.master.saveCurrent)
    filemenu.add_command(label="Save As...", command=master.master.saveAs)
    filemenu.add_separator()
    filemenu.add_command(label="Quit", command=master.master.quit)
    return filemenu
    
def createEditMenu(master):
    editmenu = tk.Menu(master, tearoff=0)
    editmenu.add_command(label="Undo",command=master.master.undo)
    editmenu.add_command(label="Redo",command=master.master.redo)
    return editmenu
    
def createOptionsMenu(master):
    optionsmenu = tk.Menu(master, tearoff=0)
    optionsmenu.add_checkbutton(label="Word Wrap", command=master.master.wordWrap)
    return optionsmenu
    
if __name__ == "__main__":
    print ("Menus is a library.")