import socket
def connection():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(('127.0.0.1', 1100))
        print("Połączono z serwerem.")  
        return client_socket
    except socket.error as e:
        print(f"Błąd połączenia: {e}")
        exit() 
def send_logindata(client_socket,message):
    if client_socket:
        
        client_socket.send(message.encode())  
        print("Wiadomość wysłana.")

