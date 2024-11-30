import tkinter as tk
import client
def close_window(name):
    name.destroy()
def signin(clients):
    si_window=tk.Toplevel()
    si_window.geometry("500x500")

    label_username = tk.Label(si_window, text="Wprowadź nazwę użytkownika:")
    label_username.pack(pady=5)
    username=tk.Entry(si_window)
    username.pack(pady=5)
    
    label_pass= tk.Label(si_window, text="Wprowadź hasło:")
    label_pass.pack(pady=5) 
    password=tk.Entry(si_window, show="*") 
    password.pack(pady=5)
 
        
    def handle_sigin(clients):
        user=username.get()
        pwd=password.get()
        print(f"{user} i {pwd}")
        message = f"LOG;{user};{pwd}" 
        client.send_logindata(clients,message)
    utton_ok=tk.Button(si_window, text="Ok", command=lambda: handle_sigin(clients))
    utton_ok.pack(pady=5)

def singup():
    su_window =tk.Toplevel()
    su_window.geometry("300x300")

    label_username = tk.Label(su_window, text="Wprowadź nazwę użytkownika:")
    label_username.pack(pady=5)
    username=tk.Entry(su_window)
    username.pack(pady=5)
    
    label_pass= tk.Label(su_window, text="Wprowadź hasło:")
    label_pass.pack(pady=5) 
    password=tk.Entry(su_window)
    password1=tk.Entry(su_window)
    password.pack(pady=5)
    label_pass1= tk.Label(su_window, text="Potwierdź hasło:")
    label_pass1.pack(pady=5) 
    password1.pack(pady=5)
    #dodac sprawdzanie hasel czy sa zgodne
    button_ok=tk.Button(su_window, text="Ok", command=lambda: close_window(su_window))
    button_ok.pack(pady=5)

clients= client.connection()

window=tk.Tk()
button_signin = tk.Button(window, text="Loguj", command=lambda: signin(clients))
button_signup = tk.Button(window, text="Zarejestruj się", command=singup)

button_signin.pack(pady=5)
button_signup.pack(pady=5)

window.mainloop() 