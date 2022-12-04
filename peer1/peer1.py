import hashlib
import socket
import os
import getpass
import sys

IP = socket.gethostbyname(socket.gethostname())
PORT = 5008
PORT2=5009
PORT3=5010
ADDRESS = (IP, PORT)
SIZE = 8192
FORMAT = "utf-8"
BUFFER_SIZE=512
DOWNLOAD_PATH="download"
UPLOAD_PATH = "upload"

def recieve_client(ip,port):
    ADRS=(ip,port)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADRS)
    print("I am Peer-1.\n")

    while True:
        data = client.recv(SIZE).decode(FORMAT)
        data= data.split("$")
        length_data=len(data)
        cmd=data[0]
        msg=data[1]
        if cmd == "KA" and length_data==2 and msg!="NOFILE":
            print(f"{msg}")
        if cmd == "KA" and length_data==2 and msg=="NOFILE":
            print(f"{msg}")
            print("Disconnected from the server")
            cmd_user="DONE"
            client.send(cmd_user.encode(FORMAT))
            client.close()
            return int(0)
        if length_data>2:
            print("type YES and enter to continue")

        user_data = input("> ")
        user_data = user_data.split(" ")
        cmd_user = user_data[0]

        if cmd_user=='YES':
            print("enters client empty")
            client.send(cmd_user.encode(FORMAT))
        if cmd_user == "HELP":
            client.send(cmd_user.encode(FORMAT))
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
                text=data[3]
                filepath = os.path.join(DOWNLOAD_PATH, name)
                with open(filepath, "w") as f:
                    f.write(text)
                    send_data = "KA$File uploaded."
                client.send(send_data.encode(FORMAT))
        else:
            client.send(cmd_user.encode(FORMAT))

def send_server(conn, addr):
    print(f"New Peer at address:{addr} has connected.")
    conn.send("KA$Connected to Peer-1 \nwrite HELP to see all the commands.".encode(FORMAT))
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    while True:
        data = conn.recv(SIZE).decode(FORMAT)
            
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
                print(file_path)
                with open(f"{file_path}", "r") as f:
                    text = f.read()
                send_data += f"{cmd}${filename}${text}"
                print(send_data)
                conn.send(send_data.encode(FORMAT))
            else: 
                send_data+="NOFILE"
                conn.send(send_data.encode(FORMAT))
        elif cmd=="DONE":
            print("Peer-1 Ready.")
            print(f"Peer-1 listening on {IP}:{PORT}.")
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
    print("Peer-1 Ready.")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDRESS)
    server.listen()
    print(f"Peer-1 listening on {IP}:{PORT}.")

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
    op=input("Do you want files from peers:[Y/N]\n>")
    if(op=="Y"):
        print("Input password for Peer-2")
        if passwordVerify("613713a253f66674f3b6c5b710a0bb1fd83e09ed2b73cf17d907492c7400755d3cce19f75b4f0567f9f2fe025dcee962"):
            returnValue = recieve_client(IP,PORT2)
            if returnValue==1:
                main()
        
        print("Input password for Peer-3")
        if passwordVerify("c31263f9a3a0dfde1ea3f5eb2cfd1562821ff42fb273a6bc0982b94669604119affd3b0e73fab5d8317215fec65bf1ea"):
                recieve_client(IP,PORT3)
                main()

    else: 
        listening()
if __name__ == "__main__":
    main()