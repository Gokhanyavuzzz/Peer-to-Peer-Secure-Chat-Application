import socket
import json
import time 

BROADCAST_IP = "192.168.1.255" # Broadcast address for the local network
BROADCAST_PORT = 6000 # We will send the broadcast message to this port
INTERVAL = 8 # seconds

def broadcast_message():
    
    #Function to broadcast a message to the network.

    # Get the username from the user
    username = input("Enter your username: ").strip()  
    
    # store locally
    with open("username.txt", "w") as f:
        f.write(username)

    # Changing the format of the username to JSON
    message = json.dumps({"username": username})

    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    
    # Set the socket option to allow broadcasting
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
    # Set the socket option to allow address reuse
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Set a timeout for the socket
    sock.settimeout(0.24)

    # Send the message every INTERVAL seconds
    print(f"Broadcasting message: {message} to {BROADCAST_IP}:{BROADCAST_PORT} every {INTERVAL} seconds.")
    
    # Loop to send the message at regular intervals
    while True:
        # Send the message to the broadcast address
        try:
            sock.sendto(message.encode(), (BROADCAST_IP, BROADCAST_PORT))
            print(f"Message sent: {message}")
        except socket.timeout:
            print("Timeout: Broadcast response not received.")
        except socket.gaierror:
            print("Invalid address or hostname.")
        except OSError as e:
            print(f"OS error occurred: {e}")
        except Exception as e:
            print(f"General error: {e}")
            break 

        
        # Wait for the specified interval before sending the next message
        time.sleep(INTERVAL)
    
if __name__ == "__main__": 
    broadcast_message()

