import tkinter as tk
from tkinter import messagebox
import csv

# Fungsi untuk membaca data dari file CSV
def read_flight_data(file_name):
    with open(file_name, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        data = list(reader)
    return data

# Fungsi untuk menulis data kembali ke file CSV
def write_flight_data(file_name, data):
    fieldnames = ['id', 'destinasi', 'maskapai', 'kapasitas', 'tanggal', 'waktu']
    with open(file_name, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

# Fungsi untuk melakukan pemesanan tiket
def book_ticket(flight_id, num_tickets):
    global flights_data
    for flight in flights_data:
        if int(flight['id']) == flight_id:
            current_capacity = int(flight['kapasitas'])
            if current_capacity >= num_tickets:
                flight['kapasitas'] = str(current_capacity - num_tickets)
                messagebox.showinfo("Booking Success", f"Booking successful for {num_tickets} tickets on Flight ID {flight_id}")
            else:
                messagebox.showwarning("Booking Failed", f"Not enough capacity on Flight ID {flight_id}. Please try again later.")
            break
    else:
        messagebox.showerror("Flight Not Found", f"Flight with ID {flight_id} not found.")

    update_available_tickets_label()  # Memperbarui label informasi tiket yang tersedia setelah pemesanan

# Fungsi untuk memperbarui label informasi tiket yang tersedia
def update_available_tickets_label():
    available_tickets_text.set(get_available_tickets_info())

# Fungsi untuk mendapatkan informasi tiket yang tersedia sebagai teks
def get_available_tickets_info():
    info = "Available Tickets:\n"
    for flight in flights_data:
        info += f"Flight ID {flight['id']}: {flight['kapasitas']} tickets\n"
    return info

# Fungsi untuk menangani tombol "Pesan Tiket"
def handle_book_ticket():
    try:
        flight_id = int(entry_flight_id.get())
        num_tickets = int(entry_num_tickets.get())
        book_ticket(flight_id, num_tickets)
        write_flight_data(file_name, flights_data)  # Menulis kembali data setelah perubahan
    except ValueError:
        messagebox.showerror("Error", "Please enter valid flight ID and number of tickets.")

# Membaca data penerbangan dari file CSV
file_name = 'tiket.csv'
flights_data = read_flight_data(file_name)

# Membuat GUI menggunakan Tkinter
root = tk.Tk()
root.title("Flight Ticket Booking")
root.geometry("800x600")

# Label untuk informasi tiket yang tersedia
available_tickets_text = tk.StringVar()
available_tickets_label = tk.Label(root, textvariable=available_tickets_text, justify=tk.LEFT)
available_tickets_label.pack()

# Memperbarui label informasi tiket yang tersedia
update_available_tickets_label()

# Garis pemisah
tk.Label(root, text="").pack()

# Label dan Entry untuk ID Penerbangan
label_flight_id = tk.Label(root, text="Flight ID:")
label_flight_id.pack()
entry_flight_id = tk.Entry(root)
entry_flight_id.pack()

# Label dan Entry untuk Jumlah Tiket
label_num_tickets = tk.Label(root, text="Number of Tickets:")
label_num_tickets.pack()
entry_num_tickets = tk.Entry(root)
entry_num_tickets.pack()

# Tombol untuk Memesan Tiket
button_book_ticket = tk.Button(root, text="Book Ticket", command=handle_book_ticket)
button_book_ticket.pack()

# Menjalankan main loop Tkinter
root.mainloop()
