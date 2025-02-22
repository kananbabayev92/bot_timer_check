import datetime
import time
import os
import pyfiglet 
from termcolor import colored 

def live_time():
    while True:
        os.system("cls")  # Clear the terminal screen
        now_time = datetime.datetime.now().strftime("%H:%M:%S")
        colored_time = colored(pyfiglet.figlet_format(now_time, font="starwars"), "red")
        print(colored_time)
        time.sleep(1)  # Wait for 1 second

live_time()
