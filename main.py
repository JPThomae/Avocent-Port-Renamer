from tkinter import *
import tkinter.messagebox
import os
from netmiko import ConnectHandler
import time
import threading


main_prompt = '--:- / cli->'
BLACK = "#100F0F"
DARK_GRAY = "#0F3D3E"
TAN = "#E2DCC8"
WHITE = "#F1F1F1"

def add():
    device = {
        'device_type': 'terminal_server',
        'ip': ipv4_entry.get(),
        'username': user_entry.get(),
        'password': password_entry.get()
    }

    connection = ConnectHandler(**device)
    time.sleep(3)

    if '~]#' in connection.find_prompt():
        connection.send_command('cli', read_timeout=2, expect_string=main_prompt)

    port_names = []
    with open('port_names.txt') as file:
        for line in file:
            port_names.append(line.strip())

    if connection.find_prompt() == main_prompt:
        connection.send_command("cd ports/serial_ports/", read_timeout=3, expect_string='--:- serial_ports cli->')
        for x in range(int(starting_port_entry.get()), int(starting_port_entry.get()) + len(port_names)):
            connection.send_command_timing(f'cd {x}/', read_timeout=0)
            connection.send_command_timing('cd cas/', read_timeout=0)
            connection.send_command_timing(f'set port_name={port_names[x - 1 - int(starting_port_entry.get())]}', read_timeout=0)
            connection.send_command_timing('save', read_timeout=0)
            
            site_text = Label(text=f"Port {x} rename complete.", font=("Rockwell", 10), bg=TAN)
            site_text.place(x=180, y=190)
            tv.update_idletasks()

    tkinter.messagebox.showinfo("Process End", "Port Rename Complete.")
            

def check_saved():
    os.startfile(r'port_names.txt')


def readme_file():
    os.startfile(r'readme.txt')


def test_connection():
    device = {
        'device_type': 'terminal_server',
        'ip': ipv4_entry.get(),
        'username': user_entry.get(),
        'password': password_entry.get()
    }

    connection = ConnectHandler(**device)

    time.sleep(3)

    current_prompt = connection.find_prompt()
    print(current_prompt)

    if connection:
        tkinter.messagebox.showinfo("Connection Test", "Connected.")
    
    

tv = Tk()
tv.minsize(width=400, height=400)
tv.maxsize(width=400, height=400)
tv.title("Avocent Port Namer")
tv.config(bg="white")

canvas = Canvas(width=400, height=200, highlightthickness=0, bg="white")
logo = PhotoImage(file="avocent_cool_logo.png")
canvas.create_image(180, 115, image=logo)
canvas.place(x=20, y=-25)

canvas2 = Canvas(width=500, height=50, highlightthickness=0, bg=DARK_GRAY)
canvas2.place(x=0, y=0)

canvas3 = Canvas(width=500, height=500, highlightthickness=0, bg=TAN)
canvas3.place(x=0, y=180)

site_text = Label(text="Avocent IP:", font=("Rockwell", 10), bg=TAN)
site_text.place(x=25, y=230)

user_text = Label(text="Username:", font=("Rockwell", 10), bg=TAN)
user_text.place(x=25, y=260)

password_text = Label(text="Password:", font=("Rockwell", 10), bg=TAN)
password_text.place(x=25, y=290)

starting_port = Label(text="Starting Port:", font=("Rockwell", 10), bg=TAN)
starting_port.place(x=200, y=325)

add_button = Button(height=1, width=12, text="Rename Ports", font=("Rockwell", 10),
                    relief="flat", bg=WHITE, command=threading.Thread(target=add).start)
add_button.place(x=20, y=360)

saved_button = Button(height=1, width=12, text="Modify Names", font=("Rockwell", 10),
                      relief="flat", bg=WHITE, command=check_saved)
saved_button.place(x=20, y=325)

readme_button = Button(height=1, width=12, text="How to Use", font=("Rockwell", 10),
                      relief="flat", bg=WHITE, command=readme_file)
readme_button.place(x=20, y=190)

test_button = Button(height=1, width=20, text="Test Connection", font=("Rockwell", 10),
                      relief="flat", bg=WHITE, command=test_connection)
test_button.place(x=190, y=360)

ipv4_entry = Entry(width=42, bg=WHITE)
ipv4_entry.place(x=127, y=232)

user_entry = Entry(width=42, bg=WHITE)
user_entry.place(x=127, y=263)

password_entry = Entry(width=42, bg=WHITE)
password_entry.place(x=127, y=293)

starting_port_entry = Entry(width=4, bg=WHITE)
starting_port_entry.insert(END, "1")
starting_port_entry.place(x=288, y=328)

data_box = Text(height=8, width=32)

tv.mainloop()
