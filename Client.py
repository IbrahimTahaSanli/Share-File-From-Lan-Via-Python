import socket
import time
import threading
import os
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox


Text1 = "Select File"
text2 = ""
Error1 = ""
Title = "Transmission Error"


BUFFER = 4096
IP = 0
PORT = 0
File = ''

class connection():
    def __init__( self ):
        self.ClientSocket = socket.socket( socket.AF_INET , socket.SOCK_STREAM )
        self.ClientSocket.connect( ( IP , int(PORT) ) )
        self.ListBoxVariable = []


    def FileName( File ):
        print(File)
        i=-1
        while( True ):
            if(File[i]=='/'):
                break
            i-=1

        print(File[i+1:0])
        return File[i+1:0]


    def SendFile( self ):
        global File

        FileSelect()
        print(File)
        Filename = connection.FileName( File )
        self.AddListBox( File )

        self.ClientSocket.send( Filename.encode("ascii") )

        self.ClientSocket.send( "END".encode("ascii") )

        self.ClientSocket.send( bytes(os.stat(File).st_size))
        
        self.ClientSocket.send( "END".encode("ascii") )

        with open( File , "rb" ) as file:
            for i in range(0 , os.stat(File).st_size  + 1 , BUFFER ):
                self.ClientSocket.send( file.read(BUFFER) )
                print("loop %d         ,       %d",i,os.stat(File).st_size)
        
        if(self.ClientSocket.recv(5).decode("ascii") == "ERROR"):
            messagebox.showerror(  )



    def AddListBox( self , File ):
        self.ListBoxVariable.append( File )


    def FileLen( File ):
        i=0

        with open( File , "rb") as File:
            while File.read(1)!='':
                    i+=1

        return i





def startConnection():
    global IP,PORT,root , Client
    
    IP = IP.get()
    PORT = PORT.get()

    Client = connection()
    root.destroy()


def FileSelect():
    global File
    File = filedialog.askopenfilename( initialdir = "C:\\" , title = Text1 , filetypes = [("All Files",".*")] )
   


root = Tk()

IP = Entry( root )
PORT = Entry( root )

IP.grid( row = 0, column = 0)
PORT.grid( row = 0 , column = 1)

button = Button( root , text = "Start" , command=startConnection )
button.grid( row = 0 , column = 2 )

root.mainloop()



root = Tk()

listbox = Listbox( root , listvariable = Client.ListBoxVariable )
listbox.grid( row = 0 , column = 0 )

sendbutton = Button(root , text = Text1 , command = Client.SendFile ) 
sendbutton.grid(row=0,column=1)

root.mainloop()

print()
print()