import socket
import threading
import time
import datetime

HOST = '0.0.0.0'
PORT = 12345

CLIENT_TIMEOUT_SECONDS = 15
HEARTBEAT_INTERVAL_CLIENT = 5


active_clients = {}
clients_lock = threading.Lock()

def handle_client(client_socket, addr):
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Server: New connection from {addr}")

    with clients_lock:
        active_clients[addr] = time.time()

    try:
        client_socket.settimeout(1.0)

        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    print(
                        f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Server: Client {addr} disconnected gracefully.")
                    break

                message = data.decode('utf-8').strip()
                print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Server: Received from {addr}: '{message}'")

                if message == "HEARTBEAT":
                    with clients_lock:
                        active_clients[addr] = time.time()

            except socket.timeout:
                pass
            except ConnectionResetError:
                print(
                    f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Server: Client {addr} forcibly disconnected (connection reset by peer).")
                break
            except Exception as e:
                print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Server: Error handling client {addr}: {e}")
                break

    finally:
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Server: Closing connection for {addr}.")
        client_socket.close()
        with clients_lock:
            if addr in active_clients:
                del active_clients[addr]


def monitor_clients():
    while True:
        time.sleep(2)
        current_time = time.time()

        clients_to_remove = []
        with clients_lock:
            for addr, last_heartbeat_time in active_clients.items():
                if current_time - last_heartbeat_time > CLIENT_TIMEOUT_SECONDS:
                    print(
                        f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Server: Client {addr} timed out. Last heartbeat: {datetime.datetime.fromtimestamp(last_heartbeat_time).strftime('%H:%M:%S')}")
                    clients_to_remove.append(addr)

            for addr in clients_to_remove:
                if addr in active_clients:
                    del active_clients[addr]
                print(
                    f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Server: Removed timed-out client {addr} from active list.")


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Server: Listening on {HOST}:{PORT}")

        monitor_thread = threading.Thread(target=monitor_clients, daemon=True)
        monitor_thread.start()

        while True:
            conn, addr = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            client_thread.start()

    except Exception as e:
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Server: Server error: {e}")
    finally:
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Server: Shutting down.")
        server_socket.close()


if __name__ == "__main__":
    start_server()