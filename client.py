import socket
import threading
import time
import datetime

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345

HEARTBEAT_INTERVAL_CLIENT = 5
RECONNECT_DELAY = 10

client_socket = None
connected = False
heartbeat_thread_running = False


def send_heartbeats():
    global connected
    global heartbeat_thread_running

    heartbeat_thread_running = True
    while connected:
        try:
            if client_socket:
                message = "HEARTBEAT"
                client_socket.sendall(message.encode('utf-8'))
                print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Client: Sent heartbeat.")
            time.sleep(HEARTBEAT_INTERVAL_CLIENT)
        except Exception as e:
            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Client: Error sending heartbeat: {e}")
            connected = False
            break
    heartbeat_thread_running = False


def connect_to_server():
    """Manages connection and re-connection to the server."""
    global client_socket, connected, heartbeat_thread_running

    while True:
        if not connected:
            print(
                f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Client: Attempting to connect to server at {SERVER_HOST}:{SERVER_PORT}...")
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((SERVER_HOST, SERVER_PORT))
                client_socket.settimeout(1.0)
                connected = True
                print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Client: Connected to server.")

                if not heartbeat_thread_running:
                    heartbeat_thread = threading.Thread(target=send_heartbeats, daemon=True)
                    heartbeat_thread.start()

                while connected:
                    try:
                        data = client_socket.recv(4096)
                        if data:
                            print(
                                f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Client: Received data from server: {data.decode('utf-8')}")
                        else:
                            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Client: Server closed connection.")
                            connected = False
                    except socket.timeout:
                         pass
                    except ConnectionResetError:
                        print(
                            f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Client: Server forcibly disconnected (connection reset).")
                        connected = False
                    except Exception as e:
                        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Client: Error during receive: {e}")
                        connected = False

            except ConnectionRefusedError:
                print(
                    f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Client: Connection refused. Server might not be running or is busy.")
            except Exception as e:
                print(
                    f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Client: An error occurred during connection: {e}")
            finally:
                if client_socket and not connected:
                    client_socket.close()
                    client_socket = None

            if not connected:
                print(
                    f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Client: Retrying connection in {RECONNECT_DELAY} seconds...")
                time.sleep(RECONNECT_DELAY)
        else:
            time.sleep(1)


if __name__ == "__main__":
    connect_to_server()