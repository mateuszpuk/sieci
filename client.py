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