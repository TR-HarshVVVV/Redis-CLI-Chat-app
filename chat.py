import redis

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Function to verify login
def login(username, password):
    stored_password = r.hget(f'user:{username}', 'password')
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
