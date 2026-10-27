import socket
import threading
import sys

# Tambahan: List untuk menyimpan semua socket client yang aktif
clients = []

# Function to receive messages from client
def receive_from_client(client_socket, client_address, stop_flag):
    while not stop_flag[0]:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message == "EXIT":
                print(f"\nClient {client_address} has closed the connection.")
                break # Hanya keluar dari perulangan client ini, server tetap jalan
            
            print(f"\nFrom Client {client_address}: {message}")
            print("Type a message for the clients: ", end="", flush=True)
        except:
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
                        c.send(message.encode('utf-8'))
                        c.close()
                    except:
                        pass
                break
            
            # Kirim pesan ke SEMUA client yang terhubung
            for c in clients:
                try:
                    c.send(message.encode('utf-8'))
                except:
                    pass
        except:
            break


# Function to run the server
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Tambahan: Mencegah error 'Address already in use' saat server di-restart
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', 444))
    
    # Diubah dari 1 ke 5 agar bisa menampung antrean banyak koneksi
    server_socket.listen(5) 
    
    print("_____________________________________________________")
    print("|                                                   |")
    print("|   Welcome to the Chat Program by Zidane Putra S   |")
    print("|                   Class TI25I                     |")
    print("|___________________________________________________|")
    print("Server is waiting for connections from clients on port 444")

    # Flag to indicate when the program should stop
    stop_flag = [False]
    
    # Pindahkan thread mengirim pesan ke sini agar berjalan sekali untuk semua
    send_thread = threading.Thread(target=send_to_clients, args=(stop_flag,))
    send_thread.start()

    # Tambahan: Gunakan looping while untuk terus menerima client baru
    while not stop_flag[0]:
        try:
            # Set timeout agar loop tidak macet dan bisa mengecek stop_flag secara berkala
            server_socket.settimeout(1.0)
            client_socket, client_address = server_socket.accept()
            
            # Masukkan client baru ke dalam list
            clients.append(client_socket)
            
            # Replace getport() with getpeername() to get the port
            print(f"\nClient has connected {client_address} on port {client_socket.getpeername()[1]}")
            print("Type a message for the clients: ", end="", flush=True)

            # Create thread to receive messages from THIS specific client
            receive_thread = threading.Thread(target=receive_from_client, args=(client_socket, client_address, stop_flag))
            receive_thread.daemon = True # Thread otomatis tertutup jika program mati
            receive_thread.start()
            
        except socket.timeout:
            continue # Lanjutkan perulangan untuk mengecek apakah server masih hidup
        except Exception as e:
            if not stop_flag[0]:
                print(f"Error accepting connections: {e}")
            break

    server_socket.close()
    print("Server is exiting.")
    sys.exit()

if __name__ == "__main__":
    start_server()