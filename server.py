import socket
import threading

# '0.0.0.0' artinya server siap menerima koneksi dari IP manapun di jaringan
HOST = '0.0.0.0'
PORT = 5000

def handle_client(client_socket, client_address):
    print(f"[KONEKSI BARU] {client_address} terhubung.")
    
    while True:
        try:
            # Menerima pesan dari client (max 1024 byte)
            message = client_socket.recv(1024).decode('utf-8')
            if not message or message == "EXIT":
                print(f"[DISCONNECT] {client_address} terputus.")
                break
            
            print(f"[{client_address}] {message}")
            
            # Balas pesan ke client
            reply = f"Server menerima: {message}"
            client_socket.send(reply.encode('utf-8'))
        except:
            break

    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[BERJALAN] Server mendengarkan di port {PORT}...")

    while True:
        # Menerima koneksi masuk dari client
        client_socket, client_address = server.accept()
        # Jalankan thread baru agar server bisa melayani multiple client
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()

if __name__ == "__main__":
    start_server()