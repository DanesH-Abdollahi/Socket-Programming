from random import Random
import socket
import threading
import prometheus_client
from time import sleep
import json

IP = "127.0.0.1"
PORT = 2000
ADDR = (IP, PORT)
Size = 1024
Format = "UTF-8"

print(f"Running The Server On {IP} : {PORT}")

Num_of_reqs = prometheus_client.Counter(
    "Num_Of_Reqs_total", "Number of Agent's Requests To Connect To The Server", ['IP', "PORT"])

CPU_Usage = prometheus_client.Gauge(
    "CPU_Usage", "CPU Usage In Percent", ['IP', 'PORT'])

RAM_Usage = prometheus_client.Gauge(
    "RAM_Usage", "RAM Memory Usage In Percent", ['IP', 'PORT'])

Random_Num = prometheus_client.Gauge(
    "Random_Num", "Random Number in Period [0 , 1000]", ['IP', 'PORT'])

Num_Of_Connections = prometheus_client.Counter(
    "Num_Of_Connections_total", "Number of Total Connections To The Server")

Num_Of_Active_Connections = prometheus_client.Gauge(
    "Num_Of_Active_Connections_total", "Number of Total Active Connections To The Server")


def New_Client(conn, addr):
    IP = addr[0]
    PORT = addr[1]
    print(f"The New Connection Was Made From {IP} On Port : {PORT}")

    reply = f"{IP} On Port {PORT}"
    conn.sendall(reply.encode(Format))

    while True:
        try:
            msg = conn.recv(Size).decode(Format)
            msg = json.loads(msg)

            CPU_Usage.labels(
                IP, PORT).set(msg["CPU_Percentage"])

            Num_of_reqs.labels(
                IP, PORT)._value.set(msg["Num_Of_Reqs"])

            Random_Num.labels(
                IP, PORT).set(msg["Random_Num"])

            RAM_Usage.labels(IP, PORT).set(msg["RAM_Memory_Usage"])

        except Exception as e:
            print(
                f"Didn't Receive Any Message Correctly from {IP} and Port {PORT}, Because : {e}")
            sleep(2)

        if not msg:
            break

    print(f"The Client From {IP} and Port : {PORT} has Discconected !")

    Num_Of_Active_Connections.dec()
    conn.close()


Sckt = socket.socket()
while True:
    try:
        Sckt.bind(ADDR)
        Sckt.listen(5)
        prometheus_client.start_http_server(8000)
        break

    except Exception as e:
        print(f"Could'nt Bind The Server On -> {IP} : {PORT} , Because : {e}")
        sleep(2)


while True:
    try:
        conn, addr = Sckt.accept()
        Num_Of_Active_Connections.inc()
        Num_Of_Connections.inc()
        thread = threading.Thread(target=New_Client, args=(conn, addr))
        thread.start()

    except Exception as e:
        print(f"Somthing Went Wrong, Because : {e}")

    except KeyboardInterrupt:
        print("\nShutting Down The Server!")
        break


Sckt.close()
