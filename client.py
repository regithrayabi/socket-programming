import socket

# Ganti dengan IP IPv4 laptop server (hasil 'ipconfig' di laptop temanmu)
SERVER_IP = '192.168.x.x' 
PORT = 5000

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Menghubungkan ke IP dan Port server
        client.connect((SERVER_IP, PORT))
        print(f"[TERHUBUNG] Berhasil terhubung ke server {SERVER_IP}:{PORT}")
        print("Ketik pesan lalu tekan Enter (ketik 'EXIT' untuk keluar):")

        while True:
            message = input("> ")
            client.send(message.encode('utf-8'))
            
            if message == "EXIT":
                break

            # Menerima balasan dari server
            response = client.recv(1024).decode('utf-8')
            print(f"[SERVER]: {response}")

    except Exception as e:
        print(f"[ERROR] Gagal terhubung ke server: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    start_client()