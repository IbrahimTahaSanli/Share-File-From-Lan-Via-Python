import socket
import time
import threading
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog



BUFFER = 4096
port = 9999
SaveLocation = ''
Files = []


Error1 = "File Corrupted"
Title1 = "Transmission Error"
Error2 = "File Recived"
Title2 = "Transmission Complited"



class connection():
    def __init__(self):
        global port
        self.ServerSocket = socket.socket( socket.AF_INET , socket.SOCK_STREAM )

        self.HostName = socket.gethostname()

        self.ServerSocket.bind(( "0.0.0.0" , port ))

        self.ServerSocket.listen()

        self.Connections = []


    def AcceptConnection( self ):
        global thread1
        self.Connections.append( [  ] )

        self.Connections[-1].append( self.ServerSocket.accept() )
        print("Thread")
        thread1.start()
        



    def ReciveFile(self , Socket , FileName):
        byte = 0
        while(byte[-3:-1]!="END"):
            print("Thread3")
            byte += Socket.recv( BUFFER ).decode(encoding = "ascii")
        
        with open( SaveLocation + FileName , "wb" ) as File:
            print("Thread2")
            for i in range(0,byte,1):
                File.write( Socket.recv(BUFFER) )

            if(File.tell() != byte):
                self.ServerSocket.sendto("ERROR".encode("ascii"),Socket)
                messagebox.showerror(Title1 , Error1)

            else:
                self.ServerSocket.sendto( "Done".encode("ascii"),Socket )
                messagebox.showerror( Title2 , Error2 )

            print("Thread1")


    def loopSocketListener(self):
        data = ''
        while(True):
            if(len(self.Connections)!=1):
                for Socket , IP in self.Connections:
                    data = Socket.recv(128).decode( "ascii" )
                    print("loop1")
                    if ( data != '' ):
                        while(data[-3:-1] != "END"):
                            data += Socket.recv(128).decode("ascii")
                            print("loop2")
                        Files.append( data )
                        self.ReciveFile( Socket , data[0:-3] )
                        print("loop3")

            data = ''

    def SetSaveLocation():
        global SaveLocation
        SaveLocation = filedialog.askdirectory()


root = Tk()

Server = connection()

print(len(Server.Connections))

thread = threading.Thread( target = Server.loopSocketListener , daemon = True )
thread.start()

thread1 = threading.Thread( target = Server.AcceptConnection , daemon = True )


listbox = Listbox( root , listvariable = Files )
listbox.grid( row = 0 , column = 0 )

button = Button( root , text = "Set Save Location" , command= connection.SetSaveLocation )
button.grid( row = 0 , column = 0 )

text = Text( root )
text.grid( row = 0 , column = 1 )

root.mainloop()

# port Tanimlama