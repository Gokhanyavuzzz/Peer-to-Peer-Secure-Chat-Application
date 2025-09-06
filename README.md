# CMP2204Project
Computer Networks Python Project
# 🔐 Peer-to-Peer Secure Chat Application

This project is a peer-to-peer chat application developed for the CMP2204 course. It supports both secure (DES-encrypted) and unsecure text messaging between users on the same network.

## 📦 Project Structure

```
.
├── chat_initiator.py         # User interface to send messages
├── chat_responder.py         # Receives and decrypts messages
├── service_announcer.py      # Broadcasts username across network
├── peer_discovery.py         # Listens for users on the network
├── users.json                # Stores discovered users
├── history.txt               # Stores sent messages
├── chatlog.txt               # Stores received messages
├── images/                   # Wireshark screenshots and execution proofs
└── README.md                 # Project documentation
```

## ⚙️ Requirements

- Python 3.10+
- `pyDes` library  
  Install via:
  ```bash
  pip install -r requirements.txt
  ```

## 🧠 Features

- ✅ Peer discovery using UDP broadcast
- ✅ Chat with selected peers using TCP
- ✅ Diffie-Hellman key exchange for secure chats
- ✅ DES encryption with base64 encoding
- ✅ Message logging (history & received logs)
- ✅ Supports both secure and unsecure messaging
- ✅ Wireshark validated secure message exchange

## 🚀 How to Run

**Step 1: Start these on both machines**
```bash
python service_announcer.py
python peer_discovery.py
```

**Step 2: On the receiver machine**
```bash
python chat_responder.py
```

**Step 3: On the sender machine**
```bash
python chat_initiator.py
```
## ⚙️ Functional Overview

### 1. `service_announcer.py`
- Broadcasts the user's presence to the local network via UDP.
- Sends the username in JSON format every 8 seconds.

### 2. `peer_discovery.py`
- Listens for broadcast messages and maintains a list of online peers.
- Updates a local `users.json` file.

### 3. `chat_initiator.py`
- Provides a CLI menu to:
  - List online users
  - Start a secure or unsecure chat
  - View chat history
- If secure chat is selected, performs:
  - Diffie-Hellman key exchange
  - DES encryption using the shared secret
  - Base64 encoding of encrypted messages

### 4. `chat_responder.py`
- Waits for incoming TCP messages.
- If the message is encrypted:
  - Performs key exchange
  - Decrypts the message using the DES key derived from shared secret
- Logs all messages (secure and unsecure) to `chatlog.txt`.

---
## 🔐 Security Mechanisms

- **Diffie-Hellman Key Exchange**: Establishes a shared secret key over insecure channels.
- **DES Encryption**: Encrypts messages using the shared secret, formatted to 8-byte blocks.
- **Base64 Encoding**: Ensures encrypted binary messages can be transmitted over text-based protocols.
- 
## 👤 Kullanıcı Senaryoları

### Senaryo 1: Ahmet sends secure message to Zeynep
1. Both launch announcer and discovery.
2. Zeynep runs chat_responder.py
3. Ahmet selects Zeynep from list and chooses secure chat.
4. DH exchange → DES encryption → base64 → sent.
5. Message decrypted and logged.

## 🛠️ Troubleshooting & Common Errors

| Issue | Cause | Solution |
|------|-------|----------|
| Peer not appearing | Broadcast IP mismatch | Check BROADCAST_IP based on subnet |
| Message fails | Antivirus blocking socket | Allow Python in Windows Firewall |
| Decryption fails | Wrong DH key | Ensure same p, g and proper key input |

---

## 🧪 Wireshark Analysis

The following images show captured packets using Wireshark during secure and unsecure message exchanges:

| Secure Sent | Secure Received |
|-------------|------------------|
| ![Secure Sent 1](images/secure_sent1.0.jpg) | ![Secure Received 1](images/received_secure2.0.jpg) |
| ![Secure Sent 2](images/secure_sent1.1.jpg) | ![Secure Received 2](images/received_secure2.1.jpg) |
| — | ![Secure Received 3](images/received_secure_message2.jpg) |

| Unsecure Sent | Unsecure Received |
|---------------|--------------------|
| ![Unsecure Sent](images/unsecure.jpg) | ![Unsecure Received](images/received-unsecure.jpg) |

---

## 📁 Commands Summary

```bash
# Start network services
python service_announcer.py
python peer_discovery.py

# Start chat interfaces
python chat_responder.py
python chat_initiator.py

# Optional: clear logs
del history.txt chatlog.txt users.json
```
---

## 📝 Requirements

- Python 3.8+
- Libraries:
  - `pyDes`
  - `base64`
  - `socket`
  - `json`

Install required packages via pip:
```bash
pip install pyDes
```

---

## 📌 Notes

- Make sure all devices are on the same subnet.
- Broadcasting IP should be modified according to your network (e.g., `192.168.1.255`).
  
## 👥 Team

- [Gökhan Yavuz]
- [Ahmet Erbey]
- [Raouf Alipour]

