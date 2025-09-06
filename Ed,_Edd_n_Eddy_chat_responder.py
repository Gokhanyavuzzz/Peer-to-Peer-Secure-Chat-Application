import socket
import json
from pyDes import triple_des, PAD_PKCS5
import base64
from datetime import datetime


P = 19
G = 2  

PORT = 6001

def start_server():
    # Set up a TCP socket to listen for incoming chat messages
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', PORT))
    # Allow the socket to listen for only one connection at a time
    server_socket.listen(1)
    
    print(f"Waiting for incoming chat connections on port {PORT}...")

    while True:
        # Accept a connection from a client
        conn, addr = server_socket.accept()
        print(f"\nConnected by {addr}")

        try:
            # Receive data from the client
            data = conn.recv(1024)

            if not data:
                print("No data received. Closing connection.")
                conn.close()
                continue

            try:
                payload = json.loads(data.decode())
            except json.JSONDecodeError:
                print("Invalid JSON received.")
                conn.close()
                continue

            if "key" in payload:
                print(f"Received key for secure exchange: {payload['key']}")

                b = 6 
                B = pow(G, b, P)

                A = int(payload['key'])
                shared_secret = pow(A, b, P)
                print(f"Shared secret: {shared_secret}")
                                
                des_key = str(shared_secret).ljust(24).encode()[:24]
                cipher = triple_des(des_key, padmode=PAD_PKCS5)

                response = json.dumps({"key": str(B)}) 
                conn.send(response.encode())

                encrypted_data = conn.recv(2048)
                message_json = json.loads(encrypted_data.decode())

                cipher_text = base64.b64decode(message_json['encrypted_message'])
                decrypted_message = cipher.decrypt(cipher_text).decode()
                                
                print(f"{addr[0]} says (secure): {decrypted_message}")
                
                with open("chatlog.txt", "a") as log:
                    log.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Received from {addr[0]} (secure): {decrypted_message}\n")

            # Check if data is received
            elif "unencrypted_message" in payload:
                    # If the message is unencrypted, print it
                    print(f"{addr[0]} says: {payload['unencrypted_message']}")
                    with open("chatlog.txt", "a") as log:
                        # Log the unencrypted message to a file")
                        log.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Received from {addr[0]}: {payload['unencrypted_message']}\n")

                    ack = json.dumps({"unencrypted_message": "Message received ✔️"})
                    conn.send(ack.encode())          

            else:
                print("Unknown message format received.")      

        except Exception as e:
            print(f"Error receiving message: {e}")

        finally:
            conn.close()
            print("Connection closed.")

if __name__ == "__main__":
    start_server()
