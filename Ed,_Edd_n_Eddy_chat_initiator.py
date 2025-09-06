import socket
import json
import base64
import secrets
import sys
from datetime import datetime
from pyDes import triple_des, PAD_PKCS5

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# Diffie-Hellman parameters
P = 19
G = 2
PORT = 6001


def main_menu():
    while True:
        print("\nChat Initiator Menu")
        print("1. Users")
        print("2. Chat")
        print("3. History")
        print("4. Exit")

        choice = input("Select an option: ").strip()
        match choice:
            case "1":
                try:
                    with open("users.json", "r") as f:
                        users = json.load(f)
                    if not users:
                        print("No users are currently online")
                    else:
                        print("Online users:")
                        for idx, (ip, username) in enumerate(users.items(), start=1):
                            print(f"{idx}. {username} ({ip})")
                except FileNotFoundError:
                    print("No user data. Run Peer Discovery first.")

            case "2":
                try:
                    with open("users.json", "r") as f:
                        users = json.load(f)
                    if not users:
                        print("No users are currently online")
                        continue

                    # List IP → username entries correctly
                    ip_list = list(users.items())
                    print("\nSelect a user to chat with:")
                    for idx, (ip, username) in enumerate(ip_list, start=1):
                        print(f"{idx}. {username} ({ip})")

                    sel = input("Select a user by number: ").strip()
                    if not sel.isdigit() or not (1 <= int(sel) <= len(ip_list)):
                        print("Invalid selection")
                        continue

                    selected_ip, selected_username = ip_list[int(sel) - 1]
                    print(f"Starting chat with {selected_username} at {selected_ip}")

                    secure_mode = input("Use secure mode? (Yes/No): ").strip().lower()
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.connect((selected_ip, PORT))
                    print("Connected. Type your message below.")

                    if secure_mode == "no":
                        # Build and send unencrypted payload
                        message = input("You: ").strip()
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        payload = json.dumps({"unencrypted_message": message})
                        sock.sendall(payload.encode())

                        print(f"You: {message}")
                        with open("history.txt", "a", encoding= "utf-8") as log:
                            log.write(f"[{timestamp}] Sent to {selected_username}: {message}\n")

                        # Receive reply
                        data = sock.recv(4096)
                        if not data:
                            print("No response from peer.")
                        else:
                            try:
                                peer = json.loads(data.decode())
                                reply = peer.get("unencrypted_message", "")
                                print(f"{selected_username}: {reply}")
                                with open("history.txt", "a", encoding= "utf-8") as log:
                                    log.write(f"[{timestamp}] Received from {selected_username}: {reply}\n")
                            except json.JSONDecodeError:
                                print("Received invalid response from peer.")
                        sock.close()

                    elif secure_mode == "yes":
                        # Diffie-Hellman handshake
                        a = secrets.randbelow(P - 2) + 2  # random in [2, P-1)
                        print(f"Generated random private key a = {a}")

                        A = pow(G, a, P)
                        sock.sendall(json.dumps({"key": str(A)}).encode())

                        resp = sock.recv(1024)
                        B = int(json.loads(resp.decode()).get("key"))
                        shared = pow(B, a, P)
                        print(f"Shared secret: {shared}")

                        # Encrypt and send
                        des_key = str(shared).ljust(24).encode()[:24]
                        cipher = triple_des(des_key, padmode=PAD_PKCS5)
                        message = input("You: ").strip()
                        encrypted = cipher.encrypt(message.encode())
                        b64 = base64.b64encode(encrypted).decode()
                        
                        sock.sendall(json.dumps({"encrypted_message": b64}).encode())
                        print("Encrypted message sent.")
                        with open("history.txt", "a", encoding= "utf-8") as log:
                            log.write(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] (Secure) Sent to {selected_username}: {message}\n")
                        sock.close()

                    else:
                        print("Invalid mode. Canceling chat.")
                        sock.close()

                except FileNotFoundError:
                    print("User list missing. Run Peer Discovery.")
                except ConnectionRefusedError:
                    print("Connection failed—responder not running?")
                except Exception as e:
                    print(f"Error: {e}")

            case "3":
                print("\nChat History:")
                logs = []
                try:
                    with open("history.txt", "r", encoding= "utf-8") as sent_log:
                        for line in sent_log:
                            logs.append(line.strip())
                except FileNotFoundError:
                    print("No history yet. Send some messages!")

                try:
                    with open("chatlog.txt", "r", encoding= "utf-8") as recv_log:
                        for line in recv_log:
                            logs.append(line.strip())

                except FileNotFoundError:
                    print("No received message history available.")

                logs.sort(key=lambda line: datetime.strptime(line[1:20], "%Y-%m-%d %H:%M:%S"))

                print("\n--- Full Chat History ---")
                for entry in logs:
                    print(entry)

            case "4":
                print("Goodbye!")
                break

            case _:
                print("Invalid choice!")

if __name__ == "__main__":
    main_menu()
