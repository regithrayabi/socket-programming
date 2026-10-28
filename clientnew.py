import socket
import threading
import sys

# Function to receive messages from the server/other clients
def receive_from_server(client_socket, stop_flag):
    while not stop_flag[0]:
        try:
            client_socket.settimeout(1.0)
            message = client_socket.recv(1024).decode('utf-8')
            
            if message == "EXIT" or message == "Server telah ditutup.":
                print(f"\n[DISCONNECT] {message}")
                stop_flag[0] = True 
                break
                
            print(f"\n{message}")
            print("Type a message for the server: ", end="", flush=True)
        except socket.timeout:
            continue 
        except Exception:
            if not stop_flag[0]:
                print("\nConnection lost.")
                stop_flag[0] = True
            break

# Function to send messages to the server
def send_to_server(client_socket, stop_flag):
    while not stop_flag[0]:
        try:
            message = input("Type a message for the server: ")
            if message == "EXIT":
                client_socket.send(message.encode('utf-8'))
                print("You have exited the program.")
                stop_flag[0] = True 
                break
                
            client_socket.send(message.encode('utf-8'))
        except:
            break
            
    client_socket.close()

# Function to run the client
def start_client():
    host = "192.168.112.38" # Pastikan IP ini adalah IP Laptop Server
    port = 444 

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client_socket.connect((host, port))
        print(f"Client connected to Server {host} on port {port}")
        print("_____________________________________________________")
        print("|                                                   |")
        print("|   Welcome to the Chat Program by Zidane Putra S   |")
        print("|                   Class TI25I                     |")
        print("|___________________________________________________|")

        stop_flag = [False]
        
        receive_thread = threading.Thread(target=receive_from_server, args=(client_socket, stop_flag))
        receive_thread.daemon = True 
        
        send_thread = threading.Thread(target=send_to_server, args=(client_socket, stop_flag))
        
        receive_thread.start()
        send_thread.start()

        # Menunggu sampai pengguna mengetik EXIT (send_thread selesai)
        send_thread.join()
        print("Client exited.")
        sys.exit()
        
    except Exception as e:
        print(f"Failed to connect to server: {e}")

if __name__ == "__main__":
    start_client()
