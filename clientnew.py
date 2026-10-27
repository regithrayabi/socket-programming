import socket
import threading

# Function to receive messages from the server
def receive_from_server(client_socket, stop_flag):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message == "EXIT":
                print("Server has closed the connection.")
                stop_flag[0] = True # Indicating the client can exit
                break
            print(f"From Server: {message}")
            print("Type a message for the server:")
        except:
            break
    client_socket.close()

# Function to send messages to the server
def send_to_server(client_socket, stop_flag):
    while True:
        message = input("Type a message for the server: ")
        if message == "EXIT":
            client_socket.send(message.encode('utf-8'))
            print("You have exited the program.")
            stop_flag[0] = True # Indicating the client can exit
            break
        client_socket.send(message.encode('utf-8'))
    client_socket.close()

# Function to run the client
def start_client():
    host = "10.102.35.193" # Default host
    port = 444 # Default port

    # Create client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print(f"Client connected to Server {host} on port {port}")
    print("_____________________________________________________")
    print("| |")
    print("| Welcome to the Chat Program by Zidane Putra S |")
    print("| Class TI25I |")
    print("|____________________________________________________|")

    # Flag to indicate when the program should stop
    stop_flag = [False]
    # Create threads for receiving and sending messages
    receive_thread = threading.Thread(target=receive_from_server, args=(client_socket, stop_flag))
    send_thread = threading.Thread(target=send_to_server, args=(client_socket, stop_flag))
    receive_thread.start()
    send_thread.start()

    # Wait for both threads to finish
    receive_thread.join()
    send_thread.join()
    print("Client exited.")

if __name__ == "__main__":
    start_client()