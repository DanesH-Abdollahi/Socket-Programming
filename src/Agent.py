import socket
import psutil
from time import sleep
import json
import random


IP = "127.0.0.1"
PORT = 2000
ADDR = (IP, PORT)
Size = 1024
Format = "UTF-8"

Num_of_reqs = 0
while True:
    Sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            Sckt.connect(ADDR)
            print(f"Connect Seccesfully To The Server {IP} on Port {PORT}")
            Num_of_reqs += 1
            My_ID = Sckt.recv(Size).decode(Format)
            print(f"I am {My_ID}")
            break

        except Exception as e:
            print(
                f"Failed To Connect to The Server-> {IP}:{PORT}, Because : {e}")
            Num_of_reqs += 1
            sleep(2)

        except KeyboardInterrupt:
            raise SystemExit(f"\nThe Client System is Shutting Down !")

    while True:
        try:
            msg = {
                "Random_Num": random.randrange(1000000000),
                "CPU_Percentage": psutil.cpu_percent(),
                "RAM_Memory_Usage": psutil.virtual_memory()[2],
                "Num_Of_Reqs": Num_of_reqs
            }
            msg = json.dumps(msg)
            Sckt.sendall(bytes(msg, encoding=Format))
            sleep(5)

        except Exception as e:
            print(f"Cant Send Message To The Server , Because : {e}")
            Sckt.close()
            break

        except KeyboardInterrupt:
            raise SystemExit(f"\nThe Client System is Shutting Down !")
