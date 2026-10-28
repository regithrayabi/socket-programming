import socket
import threading
import sys

# List untuk menyimpan semua socket client yang aktif
clients = []

# Function to receive messages from client
def receive_from_client(client_socket, client_address, stop_flag):
    while not stop_flag[0]:
        try:
            # Set timeout agar thread bisa mengecek stop_flag
            client_socket.settimeout(1.0)
            message = client_socket.recv(1024).decode('utf-8')
            
            if message == "EXIT":
                print(f"\nClient {client_address} has closed the connection.")
                # Beritahu client lain bahwa orang ini keluar
                exit_msg = f"[Sistem]: Client {client_address[1]} telah meninggalkan obrolan."
                for c in clients:
                    if c != client_socket:
                        try:
                            c.send(exit_msg.encode('utf-8'))
                        except:
                            pass
                break 
            
            # Tampilkan pesan di terminal Server
            print(f"\nFrom Client {client_address}: {message}")
            print("Type a message for the clients: ", end="", flush=True)
            
            # TERUSKAN (BROADCAST) PESAN KE SEMUA CLIENT LAIN
            broadcast_message = f"[Client {client_address[1]}]: {message}"
            for c in clients:
                if c != client_socket: 
                    try:
                        c.send(broadcast_message.encode('utf-8'))
                    except:
                        pass
                        
        except socket.timeout:
            continue
        except Exception:
            break
            
    # Hapus dari daftar jika client ini keluar
    if client_socket in clients:
        clients.remove(client_socket)
    client_socket.close()

# Function to send messages to ALL clients
def send_to_clients(stop_flag):
    while not stop_flag[0]:
        try:
            message = input("Type a message for the clients: ")
            if message == "EXIT":
                print("You have exited the program.")
                stop_flag[0] = True # Indicating the server can exit
                
                # Beritahu semua client bahwa server tutup
                for c in clients:
                    try:
                        c.send("Server telah ditutup.".encode('utf-8'))
                        c.close()
                    except:
                        pass
                break
            
            # Kirim pesan ke SEMUA client
            for c in clients:
                try:
                    c.send(f"[Server]: {message}".encode('utf-8'))
                except:
                    pass
        except:
            break

# Function to run the server
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', 444))
    server_socket.listen(5) 
    
    print("_____________________________________________________")
    print("|                                                   |")
    print("|   Welcome to the Chat Program by Zidane Putra S   |")
    print("|                   Class TI25I                     |")
    print("|___________________________________________________|")
    print("Server is waiting for connections from clients on port 444")

    stop_flag = [False]
    
    # Jalankan thread untuk Server mengetik pesan
    send_thread = threading.Thread(target=send_to_clients, args=(stop_flag,))
    send_thread.start()

    while not stop_flag[0]:
        try:
            server_socket.settimeout(1.0)
            client_socket, client_address = server_socket.accept()
            
            # Masukkan client baru ke list
            clients.append(client_socket)
            
            print(f"\nClient has connected {client_address} on port {client_socket.getpeername()[1]}")
            print("Type a message for the clients: ", end="", flush=True)

            # Buat thread untuk menerima pesan dari client ini
            receive_thread = threading.Thread(target=receive_from_client, args=(client_socket, client_address, stop_flag))
            receive_thread.daemon = True 
            receive_thread.start()
            
        except socket.timeout:
            continue 
        except Exception as e:
            if not stop_flag[0]:
                print(f"Error accepting connections: {e}")
            break

    server_socket.close()
    print("Server is exiting.")
    sys.exit()

if __name__ == "__main__":
    start_server()
