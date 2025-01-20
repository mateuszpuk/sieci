import socket
import json
def connection():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(('127.0.0.1', 1100))
        print("Połączono z serwerem.")  
        return client_socket
    except socket.error as e:
        print(f"Błąd połączenia: {e}")
        exit()

def send_logindata(client_socket, user, pwd):
    if client_socket:
        message = f"LOG;{user};{pwd}\n"  
        client_socket.send(message.encode())  
        print("Wiadomość wysłana.")
def send_signupdata(client_socket, user, pwd):
    if client_socket:
        message = f"SIGN;{user};{pwd}\n"  
        client_socket.send(message.encode())  
        print("Wiadomość wysłana.")
def send_friend(client_socket, user, friend):
    if client_socket:
        message = f"NEWF;{user};{friend}\n" 
        client_socket.send(message.encode())  
        print("Wiadomość wysłana znajomy.")

def send_message(client_socket, sender, receiver, message):
    if client_socket:
        # Prepare the message format: "MSG;sender;receiver;message\n"
        formatted_message = f"MSG;{sender};{receiver};{message}\n"
        client_socket.send(formatted_message.encode())  # Send the message
        print(f"Wiadomość wysłana do {receiver}: {message}")


def recvfromserver(client_socket):
    if client_socket:
        message = client_socket.recv(1024).decode('utf-8', errors='ignore')
        print(f"Odebrano wiadomość: {repr(message)}")
        return message.strip()
def receive_friends_list(client_socket):
    if client_socket:
        # listą znajomych w formacie JSON
        json_message = client_socket.recv(2048).decode('utf-8') 
        list=[]
        json_message=json_message.strip()
        print(f"Odebrano JSON: {repr(json_message)}")
        json_message = json_message.replace('\x00', '')  # Usuwamy znak NULL
        json_message = json_message.replace('\n', '')    # Usuwamy nowe linie
        json_message = json_message.replace('\t', '')
        # friends_data = json.loads(json_message.strip())
        # print(friends_data)
        print(f"Odebrano JSON: {repr(json_message)}")
        try:
            
            friends_data = json.loads(json_message)
            if 'friends' in friends_data:
                friends_list = friends_data['friends']
                print("Lista znajomych:")
                for friend in friends_list:
                    print(friend)
                    list.append(friend)
                print(list)
                return list
            else:
                print("Brak znajomych w odpowiedzi.")
                return None
        except json.JSONDecodeError:
            print("Błąd dekodowania JSON.")
def receive_previous_messages(client_socket, username, friend_username):
    
    # Sending the GET_MESSAGES request to the server
    request = f"GET_MESSAGES;{username};{friend_username}\n"
    client_socket.send(request.encode())

    # Receive the response from the server
    response = client_socket.recv(1024).decode()

    if response.startswith("Brak historii wiadomości"):
        print(response)
    else:
        try:
            # Try to parse the JSON response
            message_history = json.loads(response)
            print(f"Message history between {username} and {friend_username}:")

            # Extract messages from the JSON object
            messages = message_history.get("message_history", [])
            return messages
        except json.JSONDecodeError:
            print("Błąd dekodowania odpowiedzi od serwera.")
            print(response)

def get_message_history(client_socket, username, target):
    messages = receive_previous_messages(client_socket, username, target)
    return messages if messages else []
def get_group_message_history(client_socket, group_name):
    messages = receive_group_messages(client_socket, group_name)
    return messages if messages else []

def get_message_history(client_socket, username, target):
    messages = receive_previous_messages(client_socket, username, target)
    return messages if messages else []

def receive_previous_messages(client_socket, username, friend_username):
    request = f"GET_MESSAGES;{username};{friend_username}\n"
    client_socket.send(request.encode())
    response = client_socket.recv(1024).decode()

    if response.startswith("Brak historii wiadomości"):
        print(response)
    else:
        try:
            message_history = json.loads(response)
            print(f"Message history between {username} and {friend_username}:")

            messages = message_history.get("message_history", [])
            return messages
        except json.JSONDecodeError:
            print("Błąd dekodowania odpowiedzi od serwera.")
            print(response)
def create_group(client_socket, group_name):
    if client_socket:
        message = f"CREATE_GROUP;{group_name}\n"
        client_socket.send(message.encode())
        print(f"Grupa {group_name} została utworzona.")

def add_to_group(client_socket, user, group_name, friend):
    if client_socket:
        message = f"ADD_TO_GROUP;{user};{group_name};{friend}\n"
        client_socket.send(message.encode())
        print(f"Użytkownik {friend} dodany do grupy {group_name}.")

def send_group_message(client_socket, sender, group_name, message):
    if client_socket:
        formatted_message = f"GMSG;{sender};{group_name};{message}\n"
        client_socket.send(formatted_message.encode())  
        print(f"Wiadomość wysłana do grupy {group_name}: {message}")

def receive_group_messages(client_socket, group_name):
    if client_socket:
        message = f"GET_GROUP_MESSAGES;{group_name}\n"
        client_socket.send(message.encode())
        
        response = client_socket.recv(1024).decode()
        print(response)
        if response.startswith("Brak historii wiadomości"):
            print(response)
        else:
            try:
                message_history = json.loads(response)
                print(f"Wiadomości w grupie {group_name}:")
                
                messages = message_history.get("message_history", [])
                for msg in messages:
                    print(msg)
                return messages
            except json.JSONDecodeError:
                print("Błąd dekodowania odpowiedzi od serwera.")
                print(response)

def get_group_message_history(client_socket, group_name):
    messages = receive_group_messages(client_socket, group_name)
    return messages if messages else []

if __name__ == '__main__':
    clients = connection()
    print(get_group_message_history(clients, 'Group 1'))
