import csv
import tkinter as tk
from tkinter import messagebox

# Membaca list tiket
def read_tickets(by_capacity=False):
    tickets = []
    try:
        with open('tiket.csv', mode='r', newline='') as file:
            reader = csv.DictReader(file)
            tickets = list(reader)
            if by_capacity:
                tickets = merge_sort(tickets, key=lambda x: int(x['kapasitas']))
            else:
                tickets = merge_sort(tickets, key=lambda x: int(x['id']))
    except FileNotFoundError:
        with open('tiket.csv', mode='w', newline='') as file:
            fieldnames = ['id', 'destinasi', 'maskapai', 'kapasitas', 'tanggal', 'waktu']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
    return tickets

# Membaca antrean
def read_queue():
    queue = []
    try:
        with open('antrean.csv', mode='r', newline='') as file:
            reader = csv.DictReader(file)
            queue = list(reader)
    except FileNotFoundError:
        with open('antrean.csv', mode='w', newline='') as file:
            fieldnames = ['nama', 'usia', 'id_penerbangan', 'jumlah_tiket']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
    return queue

# Menambahkan jadwal baru
def add_ticket(data):
    fieldnames = ['id', 'destinasi', 'maskapai', 'kapasitas', 'tanggal', 'waktu']
    next_id = get_next_ticket_id()
    data['id'] = str(next_id)
    with open('tiket.csv', mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow(data)

# Update penerbangan
def update_ticket(id, new_data):
    tickets = read_tickets()
    for ticket in tickets:
        if ticket['id'] == str(id):
            ticket.update(new_data)
            break
    _save_all_tickets(tickets)

# Untuk menghapus jadwal penerbangan
def delete_ticket(id):
    tickets = read_tickets()
    tickets = [ticket for ticket in tickets if ticket['id'] != str(id)]
    _save_all_tickets(tickets)

# Fungsi untuk menghapus antrean
def delete_queue(index):
    queue = read_queue()
    if 0 <= index < len(queue):
        del queue[index]
    _save_all_queue(queue)

# Untuk menyimpan data penerbangan
def _save_all_tickets(tickets):
    fieldnames = ['id', 'destinasi', 'maskapai', 'kapasitas', 'tanggal', 'waktu']
    with open('tiket.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(tickets)

# Untuk menyimpan antrean
def _save_all_queue(queue):
    fieldnames = ['nama', 'usia', 'id_penerbangan', 'jumlah_tiket']
    with open('antrean.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(queue)

# Fungsi untuk mendapatkan id berikutnya
def get_next_ticket_id():
    tickets = read_tickets()
    if not tickets:
        return 1
    else:
        return max(int(ticket['id']) for ticket in tickets) + 1

# Binary search
def binary_search(tickets, id_to_find):
    low = 0
    high = len(tickets) - 1
    while low <= high:
        mid = (low + high) // 2
        if int(tickets[mid]['id']) == id_to_find:
            return tickets[mid]
        elif int(tickets[mid]['id']) < id_to_find:
            low = mid + 1
        else:
            high = mid - 1
    return None

# Merge Sort
def merge_sort(data, key=lambda x: x):
    if len(data) <= 1:
        return data
    mid = len(data) // 2
    left = merge_sort(data[:mid], key=key)
    right = merge_sort(data[mid:], key=key)
    return merge(left, right, key=key)

def merge(left, right, key=lambda x: x):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

class TicketManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Manajemen Tiket")
        self.root.geometry("700x700")
        self.root.configure(bg='lightblue')
        self.root.resizable(False, False)

        self.create_widgets()
        self.refresh_list()

    def create_widgets(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=10, pady=10)

        self.label_destinasi = tk.Label(self.frame, text="Destinasi")
        self.label_destinasi.grid(row=0, column=0)
        self.destinasi_entry = tk.Entry(self.frame)
        self.destinasi_entry.grid(row=0, column=1)

        self.label_maskapai = tk.Label(self.frame, text="Maskapai")
        self.label_maskapai.grid(row=1, column=0)
        self.maskapai_entry = tk.Entry(self.frame)
        self.maskapai_entry.grid(row=1, column=1)

        self.label_kapasitas = tk.Label(self.frame, text="Kapasitas")
        self.label_kapasitas.grid(row=2, column=0)
        self.kapasitas_entry = tk.Entry(self.frame)
        self.kapasitas_entry.grid(row=2, column=1)

        self.label_tanggal = tk.Label(self.frame, text="Tanggal")
        self.label_tanggal.grid(row=3, column=0)
        self.tanggal_entry = tk.Entry(self.frame)
        self.tanggal_entry.grid(row=3, column=1)

        self.label_waktu = tk.Label(self.frame, text="Waktu")
        self.label_waktu.grid(row=4, column=0)
        self.waktu_entry = tk.Entry(self.frame)
        self.waktu_entry.grid(row=4, column=1)

        button_padx = 10
        button_pady = 10

        self.add_button = tk.Button(self.frame, text="Tambah", command=self.add_ticket)
        self.add_button.grid(row=5, column=0, padx=button_padx, pady=button_pady, sticky="ew")

        self.update_button = tk.Button(self.frame, text="Update", command=self.update_ticket_data)
        self.update_button.grid(row=5, column=1, padx=button_padx, pady=button_pady, sticky="ew")

        self.delete_button = tk.Button(self.frame, text="Hapus", command=self.delete_ticket_data)
        self.delete_button.grid(row=5, column=2, padx=button_padx, pady=button_pady, sticky="ew")

        self.sort_by_id_button = tk.Button(self.frame, text="Urutkan berdasarkan ID", command=self.sort_tickets_by_id)
        self.sort_by_id_button.grid(row=6, column=0, columnspan=3, padx=button_padx, pady=button_pady, sticky="ew")

        self.sort_by_kapasitas_button = tk.Button(self.frame, text="Urutkan berdasarkan Kapasitas", command=self.sort_tickets_by_kapasitas)
        self.sort_by_kapasitas_button.grid(row=7, column=0, columnspan=3, padx=button_padx, pady=button_pady, sticky="ew")

        self.listbox = tk.Listbox(self.frame, width=80, height=10)
        self.listbox.grid(row=8, column=0, columnspan=3, pady=10)
        self.listbox.bind("<<ListboxSelect>>", self.on_listbox_select)

        self.queue_label = tk.Label(self.frame, text="Antrean Pemesanan:")
        self.queue_label.grid(row=9, column=0, columnspan=3)

        self.queue_listbox = tk.Listbox(self.frame, width=80, height=5)
        self.queue_listbox.grid(row=10, column=0, columnspan=3, pady=10)
        self.queue_listbox.bind("<<ListboxSelect>>", self.on_queue_listbox_select)

        self.process_queue_button = tk.Button(self.frame, text="Proses Antrean", command=self.process_queue)
        self.process_queue_button.grid(row=11, column=0, padx=button_padx, pady=button_pady, sticky="ew")

        self.delete_queue_button = tk.Button(self.frame, text="Hapus Antrean", command=self.delete_queue_data)
        self.delete_queue_button.grid(row=11, column=1, padx=button_padx, pady=button_pady, sticky="ew")

        # Add search entry and button for queue
        self.search_label = tk.Label(self.frame, text="Cari Nama:")
        self.search_label.grid(row=12, column=0)
        self.search_entry = tk.Entry(self.frame)
        self.search_entry.grid(row=12, column=1)

        self.search_button = tk.Button(self.frame, text="Cari", command=self.search_queue_by_name)
        self.search_button.grid(row=12, column=2, padx=button_padx, pady=button_pady, sticky="ew")

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        tickets = read_tickets()
        for ticket in tickets:
            self.listbox.insert(tk.END, f"{ticket['id']}: {ticket['destinasi']} - {ticket['maskapai']} - {ticket['kapasitas']} - {ticket['tanggal']} - {ticket['waktu']}")
        self.refresh_queue()

    def refresh_queue(self):
        self.queue_listbox.delete(0, tk.END)
        queue = read_queue()
        for idx, item in enumerate(queue):
            self.queue_listbox.insert(tk.END, f"{idx+1}. {item['nama']} - {item['usia']} - {item['id_penerbangan']} - {item['jumlah_tiket']}")

    def on_listbox_select(self, event):
        if not self.listbox.curselection():
            return
        index = self.listbox.curselection()[0]
        selected = self.listbox.get(index)
        id = selected.split(":")[0]
        ticket = next((t for t in read_tickets() if t['id'] == id), None)
        if ticket:
            self.destinasi_entry.delete(0, tk.END)
            self.destinasi_entry.insert(0, ticket['destinasi'])
            self.maskapai_entry.delete(0, tk.END)
            self.maskapai_entry.insert(0, ticket['maskapai'])
            self.kapasitas_entry.delete(0, tk.END)
            self.kapasitas_entry.insert(0, ticket['kapasitas'])
            self.tanggal_entry.delete(0, tk.END)
            self.tanggal_entry.insert(0, ticket['tanggal'])
            self.waktu_entry.delete(0, tk.END)
            self.waktu_entry.insert(0, ticket['waktu'])

    def on_queue_listbox_select(self, event):
        pass

    def add_ticket(self):
        destinasi = self.destinasi_entry.get()
        maskapai = self.maskapai_entry.get()
        kapasitas = self.kapasitas_entry.get()
        tanggal = self.tanggal_entry.get()
        waktu = self.waktu_entry.get()
        if not (destinasi and maskapai and kapasitas and tanggal and waktu):
            messagebox.showwarning("Peringatan", "Semua kolom harus diisi")
            return

        new_ticket = {
            'destinasi': destinasi,
            'maskapai': maskapai,
            'kapasitas': kapasitas,
            'tanggal': tanggal,
            'waktu': waktu
        }
        add_ticket(new_ticket)
        self.refresh_list()
        self.clear_entries()

    def update_ticket_data(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih tiket yang akan diupdate")
            return
        id = self.listbox.get(selected[0]).split(":")[0]
        destinasi = self.destinasi_entry.get()
        maskapai = self.maskapai_entry.get()
        kapasitas = self.kapasitas_entry.get()
        tanggal = self.tanggal_entry.get()
        waktu = self.waktu_entry.get()
        if destinasi and maskapai and kapasitas and tanggal and waktu:
            update_ticket(id, {'destinasi': destinasi, 'maskapai': maskapai, 'kapasitas': kapasitas, 'tanggal': tanggal, 'waktu': waktu})
            self.refresh_list()
            self.clear_entries()
        else:
            messagebox.showwarning("Peringatan", "Semua kolom harus diisi")

    def delete_ticket_data(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih tiket yang akan dihapus")
            return
        id = self.listbox.get(selected[0]).split(":")[0]
        delete_ticket(id)
        self.refresh_list()
        self.clear_entries()

    def sort_tickets_by_id(self):
        self.listbox.delete(0, tk.END)
        tickets = merge_sort(read_tickets(), key=lambda x: int(x['id']))
        for ticket in tickets:
            self.listbox.insert(tk.END, f"{ticket['id']}: {ticket['destinasi']} - {ticket['maskapai']} - {ticket['kapasitas']} - {ticket['tanggal']} - {ticket['waktu']}")

    def sort_tickets_by_kapasitas(self):
        self.listbox.delete(0, tk.END)
        tickets = merge_sort(read_tickets(by_capacity=True), key=lambda x: int(x['kapasitas']))
        for ticket in tickets:
            self.listbox.insert(tk.END, f"{ticket['id']}: {ticket['destinasi']} - {ticket['maskapai']} - {ticket['kapasitas']} - {ticket['tanggal']} - {ticket['waktu']}")

    def process_queue(self):
        selected = self.queue_listbox.curselection()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih antrean yang akan diproses")
            return
        index = selected[0]
        queue = read_queue()
        if 0 <= index < len(queue):
            item = queue[index]
            ticket_id = item['id_penerbangan']
            ticket = binary_search(read_tickets(), int(ticket_id))
            if ticket:
                kapasitas_baru = int(ticket['kapasitas']) - int(item['jumlah_tiket'])
                if kapasitas_baru >= 0:
                    update_ticket(ticket_id, {'kapasitas': str(kapasitas_baru)})
                    delete_queue(index)
                    self.refresh_list()
                    messagebox.showinfo("Sukses", "Antrean telah diproses")
                else:
                    messagebox.showwarning("Gagal", "Kapasitas tiket tidak mencukupi")
            else:
                messagebox.showwarning("Gagal", "Tiket tidak ditemukan")

    def delete_queue_data(self):
        selected = self.queue_listbox.curselection()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih antrean yang akan dihapus")
            return
        index = selected[0]
        delete_queue(index)
        self.refresh_queue()

    def search_queue_by_name(self):
        search_name = self.search_entry.get()
        if not search_name:
            messagebox.showwarning("Peringatan", "Masukkan nama untuk mencari")
            return

        queue = read_queue()
        search_results = [f"{idx+1}. {item['nama']} - {item['usia']} - {item['id_penerbangan']} - {item['jumlah_tiket']}"
                          for idx, item in enumerate(queue) if search_name.lower() in item['nama'].lower()]

        self.queue_listbox.delete(0, tk.END)
        if search_results:
            for result in search_results:
                self.queue_listbox.insert(tk.END, result)
        else:
            self.queue_listbox.insert(tk.END, "Tidak ditemukan antrean dengan nama tersebut")

    def clear_entries(self):
        self.destinasi_entry.delete(0, tk.END)
        self.maskapai_entry.delete(0, tk.END)
        self.kapasitas_entry.delete(0, tk.END)
        self.tanggal_entry.delete(0, tk.END)
        self.waktu_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = TicketManager(root)
    root.mainloop()
