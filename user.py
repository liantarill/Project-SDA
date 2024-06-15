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

# Fungsi untuk menulis antrean ke file CSV
def write_queue_data(file_name, data):
    fieldnames = ['nama', 'usia', 'id_penerbangan', 'jumlah_tiket']
    with open(file_name, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerows(data)

# Fungsi untuk melakukan pemesanan tiket
def book_ticket(flight_id, num_tickets, nama, usia):
    global flights_data, booking_queue
    for flight in flights_data:
        if int(flight['id']) == flight_id:
            current_capacity = int(flight['kapasitas'])
            if current_capacity >= num_tickets:
                flight['kapasitas'] = str(current_capacity - num_tickets)
                booking_queue.append({'nama': nama, 'usia': usia, 'id_penerbangan': flight_id, 'jumlah_tiket': num_tickets})
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
        nama = entry_nama.get()
        usia = entry_usia.get()
        if not nama or not usia:
            raise ValueError("Name and personal data must be provided.")
        book_ticket(flight_id, num_tickets, nama, usia)
        write_flight_data(file_name, flights_data)  # Menulis kembali data setelah perubahan
        write_queue_data(queue_file_name, booking_queue[-1:])  # Menulis data antrean baru
    except ValueError as e:
        messagebox.showerror("Error", str(e))

# Membaca data penerbangan dari file CSV
file_name = 'tiket.csv'
queue_file_name = 'antrean.csv'
flights_data = read_flight_data(file_name)
booking_queue = []

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

# Label dan Entry untuk Nama
label_nama = tk.Label(root, text="Nama:")
label_nama.pack()
entry_nama = tk.Entry(root)
entry_nama.pack()

# Label dan Entry untuk Data Diri
label_usia = tk.Label(root, text="Usia:")
label_usia.pack()
entry_usia = tk.Entry(root)
entry_usia.pack()

# Label dan Entry untuk ID Penerbangan
label_flight_id = tk.Label(root, text="Flight ID:")
label_flight_id.pack()
entry_flight_id = tk.Entry(root)
entry_flight_id.pack()

# Label dan Entry untuk Jumlah Tiket
label_num_tickets = tk.Label(root, text="Jumlah:")
label_num_tickets.pack()
entry_num_tickets = tk.Entry(root)
entry_num_tickets.pack()

# Tombol untuk Memesan Tiket
button_book_ticket = tk.Button(root, text="Book Ticket", command=handle_book_ticket)
button_book_ticket.pack()

# Menjalankan main loop Tkinter
root.mainloop()
