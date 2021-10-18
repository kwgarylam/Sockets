import socket,cv2,time

# create socket
client_socket1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

host_ip = '127.0.0.1' # paste your server ip address here
portA = 9999
client_socket1.connect((host_ip, portA))  # a tuple
while True:
    try:
        print("Enter 1 to START!")
        val = input("Enter your value: ")

        # Send the message by data stream
        client_socket1.send(bytes(val, "utf-8"))
        print("Sent")

    except:
        print("Error in client side")
        break


print("Client program finished and closed")
client_socket1.close()