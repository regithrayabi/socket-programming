import socket # Mengimpor modul socket yang diperlukan

def start_client():
    # Membuat objek socket dan menghubungkannya ke alamat IP dan port server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))

    # Memungkinkan pengguna untuk memasukkan pesan teks dan mengirimkannya ke server dalam sebuah loop
    while True:
        # Meminta input pengguna dan mengirimkan pesan teks tersebut ke server
        message = input("Masukkan pesan (atau ketik 'keluar' untuk berhenti): ")
        client_socket.sendall(message.encode('utf-8'))
        
        if message.lower() == 'keluar':
            break

        # Menerima dan menampilkan respons dari server di terminal
        response = client_socket.recv(1024).decode('utf-8')
        print(f"Server response: {response}")

    # Menangani penutupan koneksi dengan benar
    client_socket.close()

if __name__ == "__main__":
    start_client()