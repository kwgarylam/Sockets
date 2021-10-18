# This code is for the server 
# Lets import the libraries
import socket, cv2, threading

#
width = 1920
height = 1080
dim = (width, height)



# Socket Create
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print('HOST IP:', host_ip)
port = 9999
socket_address = (host_ip, port)

# Socket Bind
server_socket.bind(socket_address)

# Socket Listen
server_socket.listen(5)
print("Server started ...")
print("LISTENING AT:", socket_address)

cap = cv2.VideoCapture('sampleVideo.mp4')

def show_client(addr, client_socket):

    print('Client {} connected!'.format(addr))

    waiting = True
    frameCounter = 1
    fps = 20

    if client_socket: # if a client socket exists
        while True:
            frameCounter += 1
            if cap.get(cv2.CAP_PROP_FRAME_COUNT) == frameCounter:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                frameCounter = 1

            success, img = cap.read()
            img = cv2.resize(img, (width,height))
            cv2.namedWindow("Vid")
            cv2.moveWindow("Vid", 0, 0)
            cv2.imshow("Vid", img)
            cv2.waitKey(fps)
            #print("Video~~~~~~~~~~~~~")
            while waiting:
                try:
                    print("In the loop")
                    print(bool(client_socket))

                    msg = client_socket.recv(16)
                    msg = msg.decode("utf-8")
                    print("Msg is: ", msg)

                    if msg == "1":
                        print("In the condition")
                        waiting = False
                        break

                    else:
                        print("Not in the condition ...")

                    if not client_socket:
                        print("client socket closed")
                        print("Socket", bool(client_socket))


                    #client_socket.close()

                except Exception as e:
                    print(f"Client {addr} Disconnected ...")
                    break

        client_socket.close()
        print("Client Socket closed ...")

# Socket Accept
while True:
    client_socket, addr = server_socket.accept()
    print('GOT CONNECTION FROM:', addr)
    thread = threading.Thread(target=show_client, args=(addr, client_socket))
    thread.start()
    print("Total clients ", threading.active_count() - 1)


print("Program completed and closed!")
