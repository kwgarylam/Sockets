# This code is for the server 
# Lets import the libraries
import socket, cv2, threading

# Socket Create
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print('HOST IP:', host_ip)
port = 9998
socket_address = (host_ip, port)

# Socket Bind
server_socket.bind(socket_address)

# Socket Listen
server_socket.listen(5)
print("Server started ...")
print("LISTENING AT:", socket_address)

def show_client(addr, client_socket):
    try:
        print('Client {} connected!'.format(addr))
        if client_socket: # if a client socket exists

            msg = client_socket.recv(16)
            msg = msg.decode("utf-8")
            print("Msg is: ", msg)

            if msg == "1":
                print("In the condition")

            else:
                print("Not in the condition ...")



            #client_socket.close()

    except Exception as e:
        print(f"Client {addr} Disconnected ...")
        pass

# Socket Accept
while True:
    client_socket, addr = server_socket.accept()
    print('GOT CONNECTION FROM:', addr)
    thread = threading.Thread(target=show_client, args=(addr, client_socket))
    thread.start()
    print("Total clients ", threading.active_count() - 1)


print("Program completed and closed!")
