import socket,cv2,time

# create socket

client_socket1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#host_ip1 = '192.168.1.200' # paste your server ip address here
host_ip1 = '127.0.0.1' # paste your server ip address here
#host_ip2 = '192.168.1.201' # paste your server ip address here
portA = 9999
try:
    client_socket1.connect((host_ip1, portA))  # a tuple
    print("Server 1 connected!")
except:
    print("Warning! Server 1 is not connected!")

#client_socket2.connect((host_ip2, portA))  # a tuple
while True:
    try:
        print("Enter 1 to START!")
        val = input("Enter your value: ")

        # Send the message by data stream
        client_socket1.send(bytes(val, "utf-8"))
        #client_socket2.send(bytes(val, "utf-8"))
        print("Sent")

    except:
        print("Error in client side")
        break


print("Client program finished and closed")
client_socket1.close()
client_socket2.close()
