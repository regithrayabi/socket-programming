import socket
import threading
import sys

# Function to receive messages from the server
def receive_from_server(client_socket, stop_flag):
    while not stop_flag[0]:
        try:
            # Set timeout agar thread bisa mengecek stop_flag secara berkala
            client_socket.settimeout(1.0)
            message = client_socket.recv(1024).decode('utf-8')
            
            if message == "EXIT":
                print("\n[DISCONNECT] Server has closed the connection.")
                stop_flag[0] = True # Indicating the client can exit
                break
                
            print(f"\n{message}")
            print("Type a message for the server: ", end="", flush=True)
        except socket.timeout:
            continue # Lanjutkan loop jika tidak ada pesan masuk
        except Exception:
            if not stop_flag[0]:
                print("\nConnection lost.")
                stop_flag[0] = True
            break
            
    # Socket ditutup di fungsi main/send saja agar tidak bentrok

# Function to send messages to the server
def send_to_server(client_socket, stop_flag):
    while not stop_flag[0]:
        try:
            message = input("Type a message for the server: ")
            if message == "EXIT":
                client_socket.send(message.encode('utf-8'))
                print("You have exited the program.")
                stop_flag[0] = True # Indicating the client can exit
                break
                
            client_socket.send(message.encode('utf-8'))
        except:
            break
            
    client_socket.close()

# Function to run the client
def start_client():
    host = "10.102.35.193" # Pastikan IP ini sama dengan laptop server
    port = 444 

    # Create client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client_socket.connect((host, port))
        print(f"Client connected to Server {host} on port {port}")
        print("_____________________________________________________")
        print("|                                                   |")
        print("|   Welcome to the Chat Program by Zidane Putra S   |")
        print("|                   Class TI25I                     |")
        print("|___________________________________________________|")

        # Flag to indicate when the program should stop
        stop_flag = [False]
        
        # Create threads for receiving and sending messages
        receive_thread = threading.Thread(target=receive_from_server, args=(client_socket, stop_flag))
        receive_thread.daemon = True # Thread penerima otomatis mati jika program keluar
        
        send_thread = threading.Thread(target=send_to_server, args=(client_socket, stop_flag))
        
        receive_thread.start()
        send_thread.start()

        # Hanya perlu menunggu send_thread selesai, receive_thread jalan di background
        send_thread.join()
        print("Client exited.")
        sys.exit()
        
    except Exception as e:
        print(f"Failed to connect to server: {e}")

if __name__ == "__main__":
    start_client()
