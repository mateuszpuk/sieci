import tkinter as tk
from tkinter import messagebox
import client

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

def signin(clients):
    si_window = tk.Toplevel()
    si_window.title("Logowanie")
    si_window.configure(bg="white")
    center_window(si_window, 400, 300)

    frame = tk.Frame(si_window, bg="white", padx=20, pady=20)
    frame.pack(fill=tk.BOTH, expand=True)

    label_username = tk.Label(frame, text="Wprowadź nazwę użytkownika:", font=("Arial", 12), bg="white")
    label_username.pack(pady=10)
    username = tk.Entry(frame, font=("Arial", 12))
    username.pack(pady=5, ipadx=10)

    label_pass = tk.Label(frame, text="Wprowadź hasło:", font=("Arial", 12), bg="white")
    label_pass.pack(pady=10)
    password = tk.Entry(frame, show="*", font=("Arial", 12))
    password.pack(pady=5, ipadx=10)

    def handle_signin():
        user = username.get()
        pwd = password.get()
        if not user or not pwd:
            messagebox.showerror("Błąd", "Proszę wprowadzić nazwę użytkownika i hasło.",parent=si_window)
            return
        
        #wysylanie do serwera by sprawdzic czy taki uzytkownik istnieje 
        client.send_logindata(clients, user,pwd)
        msg=client.recvfromserver(clients)
        if (msg[:2]=='ok'):
            si_window.destroy() 
            chat(user)  
        else:
            messagebox.showerror("Błąd", "Nieprawidłowe dane logowania. Spróbuj ponownie.",parent=si_window)
        
        

    button_ok = tk.Button(frame, text="Zaloguj się", font=("Arial", 12), bg="#0078D7", fg="white",command=handle_signin)
    button_ok.pack(pady=15, ipadx=20, ipady=5)
    

def signup():
    su_window = tk.Toplevel()
    su_window.title("Rejestracja")
    su_window.configure(bg="white")
    center_window(su_window, 400, 400)

    frame = tk.Frame(su_window, bg="white", padx=20, pady=20)
    frame.pack(fill=tk.BOTH, expand=True)

    label_username = tk.Label(frame, text="Wprowadź nazwę użytkownika:", font=("Arial", 12), bg="white")
    label_username.pack(pady=10)
    username = tk.Entry(frame, font=("Arial", 12))
    username.pack(pady=5, ipadx=10)

    label_pass = tk.Label(frame, text="Wprowadź hasło:", font=("Arial", 12), bg="white")
    label_pass.pack(pady=10)
    password = tk.Entry(frame, show="*", font=("Arial", 12))
    password.pack(pady=5, ipadx=10)

    label_pass1 = tk.Label(frame, text="Potwierdź hasło:", font=("Arial", 12), bg="white")
    label_pass1.pack(pady=10)
    password1 = tk.Entry(frame, show="*", font=("Arial", 12))
    password1.pack(pady=5, ipadx=10)

    def handle_signup():
        user=username.get()
        pwd = password.get()
        pwd1 = password1.get()
        
        if pwd != pwd1:
            messagebox.showerror("Błąd", "Hasła nie są zgodne. Spróbuj ponownie.",parent=su_window)
            return
        if not username.get() or not pwd:
            messagebox.showerror("Błąd", "Proszę wypełnić wszystkie pola.",parent=su_window)
            return
        client.send_signupdata(clients,user,pwd)
        msg=client.recvfromserver(clients)
        if (msg[:2]!='ok'):
            messagebox.showerror("Błąd", "Nazwa użytkownika zajęta.",parent=su_window)
            return
        su_window.destroy()
        messagebox.showinfo("Sukces", "Zarejestrowano pomyślnie!")
        

    button_ok = tk.Button(frame, text="Zarejestruj się", font=("Arial", 12), bg="#0078D7", fg="white",command=handle_signup)
    button_ok.pack(pady=15, ipadx=20, ipady=5)

def chat(user):
    chat_window = tk.Toplevel()
    chat_window.title("Główne okno")
    chat_window.configure(bg="white")
    center_window(chat_window, 800, 600)

    main_frame = tk.Frame(chat_window, bg="white")
    main_frame.pack(fill=tk.BOTH, expand=True)

    friends_frame = tk.Frame(main_frame, bg="#f0f0f0", width=200)
    friends_frame.pack(side=tk.LEFT, fill=tk.Y)

    button_frame = tk.Frame(friends_frame, bg="#f0f0f0")
    button_frame.pack(fill=tk.X, pady=5)

    add_friend_button = tk.Button(
        button_frame, text="Dodaj znajomego", font=("Arial", 12), bg="#0078D7", 
        fg="white", command=lambda: add_friend(friends_listbox))
    add_friend_button.pack(fill=tk.X, padx=10, pady=5)

    tk.Label(friends_frame, text="Znajomi", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=10)
    friends_listbox = tk.Listbox(friends_frame, font=("Arial", 12), bg="white")
    friends_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    tk.Label(friends_frame, text="Grupy", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=10)
    groups_listbox = tk.Listbox(friends_frame, font=("Arial", 12), bg="white")
    groups_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    logout_button = tk.Button(friends_frame, text="Wyloguj się", font=("Arial", 12), bg="#0078D7", fg="white",
                              command=lambda: chat_window.destroy())
    logout_button.pack(side=tk.BOTTOM, pady=10)

    chat_frame = tk.Frame(main_frame, bg="white")
    chat_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    chat_label = tk.Label(chat_frame, text="Chat", font=("Arial", 14, "bold"), bg="white")
    chat_label.pack(pady=10)

    chat_history = tk.Text(chat_frame, font=("Arial", 12), bg="#f9f9f9", state=tk.DISABLED, height=20)
    chat_history.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    chat_entry = tk.Entry(chat_frame, font=("Arial", 12))
    chat_entry.pack(fill=tk.X, padx=10, pady=5)

    send_button = tk.Button(chat_frame, text="Wyślij", font=("Arial", 12), bg="#0078D7", fg="white", command=lambda: send_message_or_group())
    send_button.pack(pady=5)

    # Select a friend from the list and load the chat history
    def select_friend(event):
        try:
            selected_friend = friends_listbox.get(friends_listbox.curselection())
            chat_label.config(text=f"Chat z: {selected_friend}")
            chat_history.config(state=tk.NORMAL)
            chat_history.delete(1.0, tk.END)
            messages = client.get_message_history(clients, user, selected_friend)
            if messages:
                for message in messages:
                    chat_history.insert(tk.END, f"{message['sender']}: {message['message']}\n")
            else:
                chat_history.insert(tk.END, "Brak historii wiadomości.\n")
            chat_history.config(state=tk.DISABLED)
        except tk.TclError:
            print("No friend selected")

    # Select a group and load the group chat history
    def select_group(event):
        try:
            selected_group = groups_listbox.get(groups_listbox.curselection())
            chat_label.config(text=f"Grupa: {selected_group}")
            chat_history.config(state=tk.NORMAL)
            chat_history.delete(1.0, tk.END)

            messages = client.get_group_message_history(clients, selected_group)
            if messages:
                for message in messages:
                    chat_history.insert(tk.END, f"{message['sender']}: {message['message']}\n")
            else:
                chat_history.insert(tk.END, "Brak historii wiadomości w grupie.\n")

            chat_history.config(state=tk.DISABLED)
        except tk.TclError:
            print("No group selected")

    # Handle sending messages to either a friend or a group
    def send_message_or_group():
        message = chat_entry.get()
        if not message:
            return

        # Check if a friend or group is selected
        selected_friend = friends_listbox.curselection()
        selected_group = groups_listbox.curselection()

        if selected_friend:
            recipient = friends_listbox.get(selected_friend)
            chat_history.config(state=tk.NORMAL)
            chat_history.insert(tk.END, f"Ty: {message}\n")
            chat_history.config(state=tk.DISABLED)
            chat_entry.delete(0, tk.END)
            client.send_message(clients, user, recipient, message)
        
        elif selected_group:
            group_name = groups_listbox.get(selected_group)
            chat_history.config(state=tk.NORMAL)
            chat_history.insert(tk.END, f"Ty (grupa {group_name}): {message}\n")
            chat_history.config(state=tk.DISABLED)
            chat_entry.delete(0, tk.END)
            client.send_group_message(clients, user, group_name, message)
        else:
            print("Nie wybrano odbiorcy ani grupy.")

    friends_listbox.bind("<<ListboxSelect>>", select_friend)
    groups_listbox.bind("<<ListboxSelect>>", select_group)

    # Fetch and display the list of friends
    friends_data = client.receive_friends_list(clients)
    for friend in friends_data:
        friends_listbox.insert(tk.END, friend)

    # Fetch and display the list of groups
    groups_data = client.get_user_groups(clients, user)
    if groups_data:
        for group in groups_data:
            groups_listbox.insert(tk.END, group)

    def add_friend(friends_listbox):
        def handle_add():
            new_friend = friend_entry.get()
            if new_friend:
                client.send_friend(clients, user, new_friend)
                msg = client.recvfromserver(clients)
                if msg == "dodano":
                    friends_listbox.insert(tk.END, new_friend)
                    add_window.destroy()
                elif msg == "Nie możesz dodać siebie do znajomych.":
                    messagebox.showerror("Błąd", "Nie możesz dodać siebie do znajomych.", parent=add_window)
                elif msg == "Nie ma takiego użytkownika":
                    messagebox.showerror("Błąd", "Nie ma takiego użytkownika.", parent=add_window)
                else:
                    messagebox.showerror("Błąd", "Już jesteście znajomymi", parent=add_window)

        add_window = tk.Toplevel(chat_window)
        add_window.title("Dodaj znajomego")
        center_window(add_window, 300, 150)

        tk.Label(add_window, text="Nazwa znajomego:", font=("Arial", 12)).pack(pady=10)
        friend_entry = tk.Entry(add_window, font=("Arial", 12))
        friend_entry.pack(pady=5)

        tk.Button(
            add_window, text="Dodaj", font=("Arial", 12), bg="#0078D7", fg="white", relief="flat", command=handle_add
        ).pack(pady=10)

    
def main():
    window = tk.Tk()
    window.title("Komunikator")
    window.configure(bg="white")
    center_window(window, 400, 300)

    frame = tk.Frame(window, bg="white", padx=20, pady=20)
    frame.pack(fill=tk.BOTH, expand=True)

    title_label = tk.Label(frame, text="Komunikator", font=("Arial", 16, "bold"), bg="white")
    title_label.pack(pady=20)

    button_signin = tk.Button(
        frame, text="Loguj", font=("Arial", 12), bg="#0078D7", fg="white",
        width=15, command=lambda: signin(clients))
    button_signup = tk.Button(
        frame, text="Zarejestruj się", font=("Arial", 12), bg="#0078D7", fg="white",
        width=15 ,command=signup)

    button_signin.pack(pady=10)
    button_signup.pack(pady=10)

    window.mainloop()




if __name__=="__main__":
    clients = client.connection()
    main()