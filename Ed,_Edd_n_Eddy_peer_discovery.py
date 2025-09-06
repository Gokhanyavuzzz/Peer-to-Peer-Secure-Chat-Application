import time
import json
import ipaddress
import socket

PORT = 6000  
users = {}  

# Function to discover peers on the network using UDP broadcast.
def discover_peers():

    # Create a socket for UDP communication
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
    # Set the socket option to allow address reuse
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Listen for incoming broadcast messages on 6000 port
    sock.bind(('', PORT))

    #Set a timepick for the socket
    sock.settimeout(0.2)  

    print(f"Listening for broadcasts on port {PORT}...")
       
    while True:
        try:

            # Listen for incoming broadcast messages
            data, addr = sock.recvfrom(1024)

            # Decode the received data
            payload = json.loads(data.decode())
            
            # Check if the payload contains a username
            username = payload.get("username")
            
            # Check if the payload contains an IP address
            ipaddress = addr[0]
            
            # Check timestamp which is the time when the message was received
            timestamp = time.time()

            if ipaddress not in users:
                # Print the new peer information
                print(f"New peer discovered: {username} at {ipaddress} with timestamp {timestamp}")
                # Add the new peer to the users dictionary
            
            users[ipaddress] = {
                "username": username,
                "timestamp": timestamp
            }

        except socket.timeout:
            pass

        except Exception as e:
            print(f"Error receiving message: {e}")
                         
        # Print the online users
        print_online_users()
        time.sleep(3.5)

def print_online_users():

    #Create a dictionary to store online users
    online_users = {}

    #Calculate current time
    now = time.time()

    # Print the online users
    print("Online users:")
    
    # Create a list to store online users
    for ip, info in users.items():
        elapsed = now - info["timestamp"]
        status = "Online" if elapsed < 10 else "Offline"
        print(f"{info['username']} ({ip}) - {status}")
        
        # If the user is online, add them to the online_users dictionary
        if status == "Online":
            online_users[ip] = info["username"]

    # Save the online users to a JSON file
    with open("users.json", "w") as f:
        json.dump(online_users, f)



if __name__ == "__main__":
    discover_peers()
