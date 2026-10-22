import socket
import time # Modul tambahan yang diminta pada langkah implementasi

def start_server():
    # Membuat objek socket dan melakukan bind ke IP serta port
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    
    # Mendengarkan koneksi masuk dari klien
    server_socket.listen(5)
    print("Server is listening on port 12345...")

    # Memastikan server dapat menangani beberapa klien secara berurutan
    while True:
        # Menerima koneksi klien
        client_socket, client_address = server_socket.accept()
        print(f"Connected by {client_address}")

        while True:
            # Menerima pesan dari klien dan menampilkannya di terminal
            message = client_socket.recv(1024).decode('utf-8')
            
            # Jika tidak ada pesan atau klien mengetik 'keluar', hentikan loop untuk klien ini
            if not message or message.lower() == 'keluar':
                break
                
            print(f"Received message: {message}")
            
            # Mengirimkan respons konfirmasi kembali ke klien untuk mengakui penerimaan pesan
            time.sleep(0.1) # Pemanfaatan modul time 
            response = "Message received" # Pesan konfirmasi yang dikirim kembali ke klien
            client_socket.sendall(response.encode('utf-8'))
        
        # Menangani penutupan koneksi dengan benar setelah komunikasi selesai
        client_socket.close()
        print(f"Connection with {client_address} closed.")

if __name__ == "__main__":
    start_server()