import tkinter as tk
from tkinter import ttk, messagebox
import requests

# URL base da API
API_URL = "http://localhost:5000/api"

def create_user():
    name = entry_name.get()
    address = entry_address.get()
    phone = entry_phone.get()
    email = entry_email.get()
    
    response = requests.post(f"{API_URL}/users", json={
        "name": name,
        "address": address,
        "phone": phone,
        "email": email
    })
    
    if response.status_code == 201:
        messagebox.showinfo("Success", response.json()["message"])
    else:
        messagebox.showerror("Error", "Failed to create user.")

def get_subjects():
    response = requests.get(f"{API_URL}/subjects")

    if response.status_code == 200:
        subjects = response.json()
        
        # Remove all widgets (buttons) from the tab_display frame
        for widget in tab_display.winfo_children():
            if isinstance(widget, tk.Button):
                widget.destroy()

        display_text = ""
        for subject in subjects:
            display_text += f"Titulo: {subject[2]}, Data: {subject[4]}, Assunto: {subject[3]}\n"
            button = tk.Button(tab_display, text=f"Resolve Subject {subject[0]}", command=lambda s_id=subject[0]: resolve_subject(s_id))
            button.pack(pady=5)
        
        text_display.config(state=tk.NORMAL)
        text_display.delete(1.0, tk.END)
        text_display.insert(tk.END, display_text)
        text_display.config(state=tk.DISABLED)
    else:
        messagebox.showerror("Error", "Failed to fetch subjects")

def create_subject():
    user_id = entry_user_id.get()
    title = entry_subject_title.get()
    description = entry_subject_description.get()
    date = entry_subject_date.get()
    resolved = var_resolved.get()
    
    response = requests.post(f"{API_URL}/subject", json={
        "user_id": user_id,
        "title": title,
        "description": description,
        "date": date,
        "resolved": resolved
    })
    
    if response.status_code == 201:
        messagebox.showinfo("Success", response.json()["message"])
    else:
        messagebox.showerror("Error", "Failed to create subject.")

def resolve_subject(subject_id=None):
    if subject_id is None:
        subject_id = entry_subject_id_resolve.get()
    
    resolve = var_resolved_resolve.get()
    
    response = requests.put(f"{API_URL}/resolve-subject", json={
        "subject_id": subject_id,
        "resolve": resolve
    })
    
    if response.status_code == 200:
        messagebox.showinfo("Success", response.json()["message"])
    else:
        messagebox.showerror("Error", response.json()["message"])

def on_tab_selected(event):
    # Verifica se a aba "Subject Display" está ativa
    current_tab_index = notebook.index("current")
    if current_tab_index == notebook.index(tab_display):
        get_subjects()

# Criar a janela principal
app = tk.Tk()
app.title("API GUI")

# Criar o Notebook (abas)
notebook = ttk.Notebook(app)
notebook.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Aba de Criação de Usuário
tab_user = ttk.Frame(notebook)
notebook.add(tab_user, text="Create User")

tk.Label(tab_user, text="Name").grid(row=0, column=0, padx=5, pady=5)
entry_name = tk.Entry(tab_user)
entry_name.grid(row=0, column=1, padx=5, pady=5)

tk.Label(tab_user, text="Address").grid(row=1, column=0, padx=5, pady=5)
entry_address = tk.Entry(tab_user)
entry_address.grid(row=1, column=1, padx=5, pady=5)

tk.Label(tab_user, text="Phone").grid(row=2, column=0, padx=5, pady=5)
entry_phone = tk.Entry(tab_user)
entry_phone.grid(row=2, column=1, padx=5, pady=5)

tk.Label(tab_user, text="Email").grid(row=3, column=0, padx=5, pady=5)
entry_email = tk.Entry(tab_user)
entry_email.grid(row=3, column=1, padx=5, pady=5)

tk.Button(tab_user, text="Create User", command=create_user).grid(row=4, column=0, columnspan=2, pady=10)

# Aba de visualização de assuntos
tab_display = ttk.Frame(notebook)
notebook.add(tab_display, text="Subject Display")
text_display = tk.Text(tab_display, height=10)
text_display.pack(padx=10, pady=10, side="left", fill="both", expand=True)
text_display.config(state=tk.DISABLED)

# Aba de Criação de Assunto
tab_subject = ttk.Frame(notebook)
notebook.add(tab_subject, text="Create Subject")

tk.Label(tab_subject, text="User ID").grid(row=0, column=0, padx=5, pady=5)
entry_user_id = tk.Entry(tab_subject)
entry_user_id.grid(row=0, column=1, padx=5, pady=5)

tk.Label(tab_subject, text="Title").grid(row=1, column=0, padx=5, pady=5)
entry_subject_title = tk.Entry(tab_subject)
entry_subject_title.grid(row=1, column=1, padx=5, pady=5)

tk.Label(tab_subject, text="Description").grid(row=2, column=0, padx=5, pady=5)
entry_subject_description = tk.Entry(tab_subject)
entry_subject_description.grid(row=2, column=1, padx=5, pady=5)

tk.Label(tab_subject, text="Date").grid(row=3, column=0, padx=5, pady=5)
entry_subject_date = tk.Entry(tab_subject)
entry_subject_date.grid(row=3, column=1, padx=5, pady=5)

var_resolved = tk.BooleanVar()
tk.Checkbutton(tab_subject, text="Resolved", variable=var_resolved).grid(row=4, column=0, columnspan=2, padx=5, pady=5)

tk.Button(tab_subject, text="Create Subject", command=create_subject).grid(row=5, column=0, columnspan=2, pady=10)

# Aba de Resolução de Assunto
tab_resolve = ttk.Frame(notebook)
notebook.add(tab_resolve, text="Resolve Subject")

tk.Label(tab_resolve, text="Subject ID").grid(row=0, column=0, padx=5, pady=5)
entry_subject_id_resolve = tk.Entry(tab_resolve)
entry_subject_id_resolve.grid(row=0, column=1, padx=5, pady=5)

tk.Label(tab_resolve, text="Resolve").grid(row=1, column=0, padx=5, pady=5)
var_resolved_resolve = tk.BooleanVar()
tk.Checkbutton(tab_resolve, variable=var_resolved_resolve).grid(row=1, column=1, padx=5, pady=5)

tk.Button(tab_resolve, text="Resolve Subject", command=resolve_subject).grid(row=2, column=0, columnspan=2, pady=10)

# Vincula o evento de seleção de aba à função
notebook.bind("<<NotebookTabChanged>>", on_tab_selected)

# Iniciar o loop principal da interface
app.mainloop()