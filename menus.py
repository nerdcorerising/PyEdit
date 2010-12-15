import tkinter

def createFileMenu(master):
    filemenu = tkinter.Menu(master, tearoff=0)
    filemenu.add_command(label="Open File", command=master.master.openFile)
    filemenu.add_separator()
    filemenu.add_command(label="Quit", command=master.master.quit)
    return filemenu
    
def createEditMenu(master):
    editmenu = tkinter.Menu(master, tearoff=0)
    return editmenu
    
def createOptionsMenu(master):
    optionsmenu = tkinter.Menu(master, tearoff=0)
    optionsmenu.add_command(label="Word Wrap", command=master.master.wordWrap())
    return optionsmenu