========================README========================================
PEER TO PEER NETWORK USING SOCKET PROGRAMMING IN PYTHON



-------------------Dependencies-------------------
This code was built using Python 3.10 on Windows 10. Working on MacOS/Linux has not been tested.
Python should be added to your PATH variable.
Run "python --version" in a command prompt to check if it is active
Run "pip --version" in a command prompt to check if it is active
Other modules imported are already installed in the native package. No need to explicitly install them.

-------------------Setting up the Code-------------------
Unzip the file into any folder on your local machine. 
The code has been set up in 3 different directories which represent 3 different nodes on the network.
all 3 peers have the ability to send and recieve information and all of them have a password 
associated with them that is needed to access them. The ports have been hardcoded so that all the 
peers have the IP address and ports of all the other peers.


download the 3 folders and open a terminal in all the 3 directories and run the following commands in
diffrent terminal:
- $ python peer1.py
- $ python peer2.py
- $ python peer3.py

To generate the hashes hashing.py should be executed in a diffrent terminal:
- $python hashing.py
Follow the command lines,and before connecting with the peers input the password for the corresponding
peers which have been encoded with the SHA384:
peer1:"peer1"
peer2:"peer2"
peer3:"peer3"

---------------Tests----------------------------
-When peer-1 asks for recieving file, press Y and press N on peer-2 and peer-3.You will be 
prompted to write the password for peer-2 which is "peer2"(excluding exclamation marks) and then
you can write "HELP" and peer-2 will display "data is HELP" and you can see that on peer1 the
help information is there.
-To initiate a data transfer, write "CHECK peer2_t1.txt" which will search the upload folder of
peer2 and if the file peer2_t1.txt is there, the file will be sent to the download folder of
peer1