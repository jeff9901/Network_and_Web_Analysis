# This code checks for internet connection and informs whenever the internet is connected or disconnected
import socket
import urllib.request
import time
from datetime import datetime

import tkinter
from tkinter import messagebox

root = tkinter.Tk()
root.withdraw()
time_now = datetime.now()
read_time = time_now.strftime("%m/%d/%Y, %H:%M:%S")



global current, previous
current = None
previous = None

# This function checks for internet connection
def try_connection():
    time_now = datetime.now()
    read_time = time_now.strftime('%m/%d/%Y, %H:%M:%S')        

    try:
        response=urllib.request.urlopen('http://google.com/',timeout=1)
        return True
    except urllib.request.URLError:
        return False
    except socket.timeout:
        return False
    return False

while True:
    time_now = datetime.now()
    read_time = time_now.strftime('%m/%d/%Y, %H:%M:%S')
    file = open('C:\\Enter\file\Location\Log_file.txt', 'a')
    
    current = try_connection()
    
#Inform user whenever the internet is either connected or disconnected   
    if current != previous:
        if current == True:
            print('Connected to internet at: ' + read_time + 'hrs')
            file.write('Connected to internet at: ' + read_time + '\n')
            messagebox.showinfo('Update','Connected to internet at: ' + read_time + ' hrs' )

            
        else:
            print('Not Connected to internet at:  ' +  read_time + ' hrs')
            file.write('Not Connected to internet at:  ' + read_time + '\n')
            messagebox.showinfo('Update','Not Connected to internet at:  ' + read_time + ' hrs')
    else:
        pass
        
    previous = current

    time.sleep(5)



