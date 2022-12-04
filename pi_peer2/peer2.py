import hashlib
import socket
import os
import getpass
import sys
from urllib3 import Timeout

IP = socket.gethostbyname(socket.gethostname())
PORT = 5009                             #######  EDIT THIS TO MATCH THE PORT OF THE PI IT IS CURRENTLY RUNNING ON
ADDRESS = (IP, PORT)
SIZE = 1048576
FORMAT = "utf-8"
BUFFER_SIZE=4096
DOWNLOAD_PATH="download"
UPLOAD_PATH = "upload"
SEPERATOR='$'


def recieve_client(ip,port):
    ADRS=(ip,port)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADRS)
    print("I am Peer-2.\n")

    while True:
        data = client.recv(SIZE).decode(FORMAT)
        print(data)
        data= data.split("$")
        print(data)
        length_data=len(data)
        cmd=data[0]
        msg=data[1]
        if cmd == "KA" and length_data==2 and msg!="NOFILE":
            print(f"{msg}")
        if cmd == "KA" and length_data==2 and msg=="NOFILE":
            print(f"{msg}")
            print("Disconnected from the server")
            cmd_user="DONE"
            client.send(cmd_user.encode())
            client.close()
            return int(0)
        
        #if length_data>2:
        #    print("type YES and enter to continue")

        user_data = input("> ")
        user_data = user_data.split(" ")
        cmd_user = user_data[0]

        if cmd_user=='YES':
            print("enters client empty")
            client.send(cmd_user.encode(FORMAT))
        if cmd_user == "HELP":
            client.send(cmd_user.encode())
        elif cmd_user=="DONE":
            print("Disconnected from the server.")
            client.send(cmd_user.encode(FORMAT))
            client.close()
            return int(1)
        elif (cmd_user == "CHECK" or msg=="CHECK"):
            if length_data<=3:
                path=user_data[1]
                send_cmd = f"{cmd_user}${path}"
                client.send(send_cmd.encode(FORMAT))
            elif length_data>3:
                name=data[2]
                byting=data[3]
                filepath = os.path.join(DOWNLOAD_PATH, name)

                with open(filepath, "wb") as f:
                    while True:
                #        print("not really")
                        client.settimeout(1.0)
                        try:
                            bytes_read = client.recv(BUFFER_SIZE)
                #            print(bytes_read)
                #            print("writes")
                #            print(bytes_read)
                            f.write(bytes_read)
                #            print("Is stuck?")
                        except socket.timeout as e:
                            f.close()
                            break
                print("Transfer complete")
                send_data = "KA$File uploaded."
                client.send(send_data.encode(FORMAT))
        else:
            client.send(cmd_user.encode(FORMAT))

def send_server(conn, addr):
    print(f"New Peer at address:{addr} has connected.")
    conn.send(f"KA$Connected to Peer-2 \nwrite HELP to see all the commands.".encode())
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    while True:
        data = conn.recv(SIZE).decode()
            
        print(f"data is {data}")
        data = data.split("$")
        cmd = data[0]
        msg="Default"
        length=len(data)

        if length>1:
            msg=data[1]

        if cmd == "KA":
            print(f"{msg}")
        if cmd == "HELP":
            send_data = "KA$"
            send_data += "CHECK<SPACE><path>:Checks if file is there with the peer,if yes then sends the text file .\n"
            send_data += "DONE: Disconnect from the server.\n"
            send_data += "HELP: List all the commands.\n"
            conn.send(send_data.encode(FORMAT))

        elif cmd == "CHECK":
            filename = data[1]
            files = os.listdir(UPLOAD_PATH)
            send_data = "KA$"
            if filename in files:
                file_path = os.path.join(UPLOAD_PATH, filename)
                filesize = os.path.getsize(file_path)                
                conn.send(f"KA${cmd}${filename}${filesize}".encode())
                with open(file_path, "rb") as f:
                    while True:
                        bytes_read = f.read(BUFFER_SIZE)
                    #    print(bytes_read)
                        if not bytes_read:
                            break
                    #    byte_send=bytes_read.decode(FORMAT)
                    #    print(byte_send)
                    #    print(type(byte_send))
                    #    print("sends")
                        conn.send(bytes_read)
                        #print(bytes_read)
                    #    print("sendall works")
            else: 
                send_data+="NOFILE"
                conn.send(send_data.encode(FORMAT))
        elif cmd=="DONE":
            print("Peer-2 Ready.")
            print(f"Peer-2 listening on {IP}:{PORT}.")
            break
        elif cmd=='YES':
            send_data = "KA$"
            send_data += "Enter the next command.\n"
            conn.send(send_data.encode(FORMAT))
        else:
            send_data="KA$"
            send_data+="invalid command-write HELP for info on correct commands"
            conn.send(send_data.encode(FORMAT))

def listening():
    print("Peer-2 Ready.")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDRESS)
    server.listen()
    print(f"Peer-2 listening on {IP}:{PORT}.")

    while True:
        conn, addr = server.accept()
        send_server(conn,addr)

def passwordVerify(encodedPassword):
    password = getpass.getpass("Enter password: ")
    password = password.encode()
    password = hashlib.sha384(password).hexdigest()
    if (password == encodedPassword):
        return True
    else:
        print("Wrong Password, Try again.")
        return passwordVerify(encodedPassword)

def main():
    listening()
if __name__ == "__main__":
    main()
