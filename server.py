# This code is for the server 
# Lets import the libraries
import socket, cv2, threading
import screeninfo #pip install screeninfo

#
#width = 1920
#height = 1080
cap = cv2.VideoCapture('mon1.mp4')
screen_id = 0
screen = screeninfo.get_monitors()[screen_id]
width, height = screen.width, screen.height
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



playable = True
stop = True
reset = False

def videoPlayback():
    frameCounter = 1
    fps = 20
    window_name = 'Vid'
    global playable
    global stop
    global reset

    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    cv2.moveWindow(window_name, screen.x - 1, screen.y - 1)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while True:


        while (playable):
            if reset:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                frameCounter = 0
                reset = False

            frameCounter += 1
            if cap.get(cv2.CAP_PROP_FRAME_COUNT) == frameCounter:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                frameCounter = 1

            success, img = cap.read()
            img = cv2.resize(img, (width, height))
            cv2.imshow(window_name, img)
            cv2.waitKey(fps)
            if stop == True:
                playable = False
                print("Video Stopped")


def show_client(addr, client_socket):

    global playable
    global stop
    global reset

    print('Client {} connected!'.format(addr))

    waiting = True
    #frameCounter = 1
    #fps = 20
    #window_name = 'Vid'

    if client_socket: # if a client socket exists
        while True:
            #print("Video~~~~~~~~~~~~~")
            #videoPlayback()


            #while waiting:
            try:
                print("In the loop")
                print(bool(client_socket))

                msg = client_socket.recv(16)
                msg = msg.decode("utf-8")
                print("Msg is: ", msg)

                if msg == "1":
                    print("In the condition")
                    waiting = False
                    stop = False
                    playable = True
                    #break
                elif msg == "2":
                    print("Reset")
                    reset = True
                    playable = True
                    stop = True

                else:
                    print("Not in the condition ...")
                    stop = True
                    playable = False

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
    thread_Video = threading.Thread(target=videoPlayback)

    thread.start()
    thread_Video.start()

    print("Total clients ", threading.active_count() - 1)


print("Program completed and closed!")
