# Redis-Based Chat Application (Pub/Sub)

## **📌 System Description**

This project is a **simple chat application** using **Redis Pub/Sub**, where users can log in, join a chat room, and exchange messages. The system stores user credentials in Redis and enables real-time communication between users in the same chat room.

### **🔹 Key Features**

- **User authentication** using Redis Hashes.
- **Chat rooms** where multiple users can communicate.
- **Two ways to run the application**:
  1. **Manually using Redis CLI (tmux recommended).**
  2. **Automatically using a Python script.**
- **Real-time messaging** using Redis' `PUBLISH` and `SUBSCRIBE` commands.

---

## **📌 Step-by-Step Setup Guide**

### **1️⃣ Start Redis Server**

1. Open **WSL terminal**.
2. Start the Redis server:
   ```sh
   redis-server
   ```
3. Open Redis CLI:
   ```sh
   redis-cli
   ```

---

### **2️⃣ Create Users in Redis**

Store users and their passwords:

```sh
HSET users:harsh password "harsh123"
HSET users:aditya password "aditya123"
```

✅ **Verify user data**:

```sh
HGETALL users:harsh
```

---

### **3️⃣ Create a Chat Room**

1. Create a chat room (`room1`) and add users:
   ```sh
   SADD room:room1 harsh aditya
   ```
2. **Check room members**:
   ```sh
   SMEMBERS room:room1
   ```

---

## **📌 Two Ways to Run the Chat Application**

### **🔹 Method 1: Using Redis CLI (Manual Mode)**

#### **For Harsh**

1. Open **tmux**:
   ```sh
   tmux
   ```
2. Start Redis CLI and subscribe to `room1`:
   ```sh
   redis-cli
   SUBSCRIBE room1
   ```
3. **Split tmux window**:
   - Press `Ctrl + B`, then `%` to split vertically.
4. In the new pane, open Redis CLI and **send messages**:
   ```sh
   redis-cli
   PUBLISH room1 "Harsh: Hello Aditya!"
   ```

#### **For Aditya**

- Repeat the same steps in another WSL terminal.
- Subscribe and send messages in `room1` using Redis CLI.

---

### **🔹 Method 2: Using a Python Script**

#### **1️⃣ Install Dependencies**

```sh
pip3 install redis
```

#### **2️⃣ Run `chat.py` in CMD**

- **For Harsh** (Terminal 1 – CMD):
  ```sh
  python chat.py
  ```
- **For Aditya** (Terminal 2 – CMD):
  ```sh
  python chat.py
  ```

#### **3️⃣ Subscribe to Chat Room in WSL**

```sh
redis-cli
SUBSCRIBE room1
```

---

## **📌 Explanation of `chat.py` Code**

```python
import redis

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Function to verify login
def login(username, password):
    stored_password = r.hget(f'users:{username}', 'password')
    if stored_password and stored_password == password:
        print(f"✅ Login successful! Welcome, {username}")
        return True
    else:
        print("❌ Invalid username or password.")
        return False

# Function to subscribe to a chat room
def subscribe_to_room(room):
    pubsub = r.pubsub()
    pubsub.subscribe(room)
    print(f"📢 Listening for messages in {room}...")

    for message in pubsub.listen():
        if message["type"] == "message":
            print(message["data"])

# Function to send a message
def send_message(room, username, msg):
    r.publish(room, f"{username}: {msg}")

if __name__ == "__main__":
    # Force user to log in
    user = input("Enter username: ")
    pwd = input("Enter password: ")

    if not login(user, pwd):
        exit()  # Exit if login fails

    # Proceed to chat
    room = input("Enter chat room (e.g., room1): ")
    print("Type your message and press Enter to send.")
    print("Type 'exit' to leave the chat.")

    while True:
        msg = input(f"{user}: ")
        if msg.lower() == "exit":
            break
        send_message(room, user, msg)
```

### **🔹 How It Works**

1. **Login System**: Users enter their username and password.
2. **Authentication**: Checks Redis for the stored password.
3. **Join Chat Room**: If login is successful, the user selects a chat room.
4. **Messaging**:
   - Messages are published to Redis using `PUBLISH room1 "message"`.
   - Subscribers receive messages instantly in real-time.

---

## **📌 Expected Workflow**

1. **Start Redis server in WSL**
2. **Use either Redis CLI (Tmux) OR `chat.py` (Python) to chat**
3. **Messages get published in `room1`, and all subscribers receive them**

---

## **📌 Conclusion**

- **Redis Pub/Sub** enables real-time chat functionality.
- **Two execution methods**:
  - **Manual via Redis CLI & tmux**
  - **Automated via Python Script**
- **Requires only two terminals**:
  - **1 WSL (Redis CLI, tmux for Pub/Sub)**
  - **1 CMD (Python Script for login & messaging)**

🚀 **This project effectively demonstrates Redis' Pub/Sub messaging for real-time communication.**
