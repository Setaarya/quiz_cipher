import tkinter as tk
from tkinter import filedialog, messagebox
import os

# Vigenere Cipher
def vigenere_cipher(text, key, mode):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    result = ''
    text = text.upper()
    key = key.upper()

    for i in range(len(text)):
        if text[i] in alphabet:
            if mode == 'encrypt':
                index = (alphabet.find(text[i]) + alphabet.find(key[i % len(key)])) % len(alphabet)
            else:
                index = (alphabet.find(text[i]) - alphabet.find(key[i % len(key)])) % len(alphabet)
            result += alphabet[index]
        else:
            result += text[i]
    return result

# Playfair Cipher
def create_playfair_matrix(key):
    alphabet = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'
    matrix = []
    key = ''.join(sorted(set(key), key=key.index))

    for char in key.upper():
        if char not in matrix and char in alphabet:
            matrix.append(char)

    for char in alphabet:
        if char not in matrix:
            matrix.append(char)

    return [matrix[i:i + 5] for i in range(0, 25, 5)]

def find_position(matrix, letter):
    for row in range(5):
        for col in range(5):
            if matrix[row][col] == letter:
                return row, col
    return None

def playfair_cipher(text, key, mode):
    text = text.upper().replace("J", "I")
    key = key.upper()
    text = ''.join([char for char in text if char.isalpha()])

    pairs = []
    i = 0
    while i < len(text):
        a = text[i]
        b = 'X' if i + 1 == len(text) else text[i + 1]

        if a == b:
            pairs.append((a, 'X'))
            i += 1
        else:
            pairs.append((a, b))
            i += 2

    if len(text) % 2 != 0:
        pairs.append((text[-1], 'X'))

    matrix = create_playfair_matrix(key)

    result = ''
    for a, b in pairs:
        row1, col1 = find_position(matrix, a)
        row2, col2 = find_position(matrix, b)

        if row1 == row2:
            if mode == 'encrypt':
                result += matrix[row1][(col1 + 1) % 5]
                result += matrix[row2][(col2 + 1) % 5]
            else:
                result += matrix[row1][(col1 - 1) % 5]
                result += matrix[row2][(col2 - 1) % 5]
        elif col1 == col2:
            if mode == 'encrypt':
                result += matrix[(row1 + 1) % 5][col1]
                result += matrix[(row2 + 1) % 5][col2]
            else:
                result += matrix[(row1 - 1) % 5][col1]
                result += matrix[(row2 - 1) % 5][col2]
        else:
            result += matrix[row1][col2]
            result += matrix[row2][col1]

    return result

# Hill Cipher
def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def matrix_multiply(matrix1, matrix2, size):
    result = [[0] * size for _ in range(size)]

    for i in range(size):
        for j in range(size):
            for k in range(size):
                result[i][j] += matrix1[i][k] * matrix2[k][j]
            result[i][j] %= 26

    return result

def get_determinant(matrix, size):
    if size == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    elif size == 3:
        a, b, c = matrix[0]
        d, e, f = matrix[1]
        g, h, i = matrix[2]
        return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)

def get_matrix_inverse(matrix, size):
    det = get_determinant(matrix, size) % 26
    det_inv = mod_inverse(det, 26)
    if det_inv is None:
        raise ValueError("Tidak ada invers untuk determinan matriks ini.")

    if size == 2:
        a, b = matrix[0]
        c, d = matrix[1]
        inv_matrix = [[d, -b], [-c, a]]
    elif size == 3:
        a, b, c = matrix[0]
        d, e, f = matrix[1]
        g, h, i = matrix[2]
        inv_matrix = [
            [(e * i - f * h), -(b * i - c * h), (b * f - c * e)],
            [-(d * i - f * g), (a * i - c * g), -(a * f - c * d)],
            [(d * h - e * g), -(a * h - b * g), (a * e - b * d)],
        ]

    for i in range(size):
        for j in range(size):
            inv_matrix[i][j] = (inv_matrix[i][j] * det_inv) % 26

    return inv_matrix

def hill_cipher(text, key, mode):
    text = text.upper().replace(" ", "")
    key = key.upper().replace(" ", "")
    text = ''.join([char for char in text if char.isalpha()])
    size = int(len(key) ** 0.5)
    if size * size != len(key):
        raise ValueError("Kunci harus dapat diubah menjadi matriks persegi.")

    key_matrix = [[ord(key[i * size + j]) - ord('A') for j in range(size)] for i in range(size)]
    while len(text) % size != 0:
        text += 'X'

    text_matrix = [[ord(text[i * size + j]) - ord('A') for j in range(size)] for i in range(len(text) // size)]

    if mode == 'decrypt':
        key_matrix = get_matrix_inverse(key_matrix, size)

    result_matrix = []
    for row in text_matrix:
        row_matrix = [[element] for element in row]
        result_row = matrix_multiply([row], key_matrix, size)
        result_matrix.append(result_row[0])

    result = ''.join([chr(result_matrix[i][j] + ord('A')) for i in range(len(result_matrix)) for j in range(size)])
    return result

# GUI 
def create_gui():
    root = tk.Tk()
    root.title("Encryption Program")
    
    # Mengatur layar penuh dan background
    root.attributes("-fullscreen", True)
    root.configure(bg="#2B2B2B")  # Warna background

    # Mengubah warna teks
    fg_color = "#FFFFFF"
    btn_bg_color = "#007BFF"
    entry_bg_color = "#4C4C4C"
    
    def step_1():
        for widget in root.winfo_children():
            widget.pack_forget()

        method_label = tk.Label(root, text="Pilih Metode:", font=("Arial", 14), bg="#2B2B2B", fg=fg_color)
        method_label.pack(pady=20)

        global method_var
        method_var = tk.StringVar(value="vigenere")
        vigenere_radio = tk.Radiobutton(root, text="Vigenere Cipher", variable=method_var, value="vigenere", bg="#2B2B2B", fg=fg_color, selectcolor="#4C4C4C", font=("Arial", 12))
        playfair_radio = tk.Radiobutton(root, text="Playfair Cipher", variable=method_var, value="playfair", bg="#2B2B2B", fg=fg_color, selectcolor="#4C4C4C", font=("Arial", 12))
        hill_radio = tk.Radiobutton(root, text="Hill Cipher", variable=method_var, value="hill", bg="#2B2B2B", fg=fg_color, selectcolor="#4C4C4C", font=("Arial", 12))
        vigenere_radio.pack(pady=5)
        playfair_radio.pack(pady=5)
        hill_radio.pack(pady=5)

        next_button = tk.Button(root, text="Selanjutnya", command=step_2, bg=btn_bg_color, fg=fg_color, font=("Arial", 12), width=20)
        next_button.pack(pady=20)

    def step_2():
        for widget in root.winfo_children():
            widget.pack_forget()

        key_label = tk.Label(root, text="Masukkan Kunci:", font=("Arial", 14), bg="#2B2B2B", fg=fg_color)
        key_label.pack(pady=20)

        global key_entry
        key_entry = tk.Entry(root, width=40, bg=entry_bg_color, fg=fg_color, font=("Arial", 12))
        key_entry.pack(pady=10)

        next_button = tk.Button(root, text="Selanjutnya", command=step_3, bg=btn_bg_color, fg=fg_color, font=("Arial", 12), width=20)
        next_button.pack(pady=20)

    def step_3():
        for widget in root.winfo_children():
            widget.pack_forget()

        input_label = tk.Label(root, text="Pilih Metode Input:", font=("Arial", 14), bg="#2B2B2B", fg=fg_color)
        input_label.pack(pady=20)

        global text_var
        text_var = tk.StringVar(value="manual")
        manual_radio = tk.Radiobutton(root, text="Input Manual", variable=text_var, value="manual", bg="#2B2B2B", fg=fg_color, selectcolor="#4C4C4C", font=("Arial", 12))
        file_radio = tk.Radiobutton(root, text="Input dari File .txt", variable=text_var, value="file", bg="#2B2B2B", fg=fg_color, selectcolor="#4C4C4C", font=("Arial", 12))
        manual_radio.pack(pady=5)
        file_radio.pack(pady=5)

        global input_entry, file_label
        input_entry = tk.Entry(root, width=60, bg=entry_bg_color, fg=fg_color, font=("Arial", 12))
        input_entry.pack(pady=10)

        file_label = tk.Label(root, text="File belum dipilih.", font=("Arial", 12), bg="#2B2B2B", fg=fg_color)

        text_var.trace_add('write', lambda *args: toggle_input_mode())

        next_button = tk.Button(root, text="Selanjutnya", command=step_4, bg=btn_bg_color, fg=fg_color, font=("Arial", 12), width=20)
        next_button.pack(pady=20)

    def toggle_input_mode():
        if text_var.get() == "manual":
            input_entry.pack()
            file_label.pack_forget()
        else:
            input_entry.pack_forget()
            file_label.pack()

            filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
            if filename:
                with open(filename, 'r') as file:
                    global input_text
                    input_text = file.read()
                file_label.config(text=f"File Terpilih: {os.path.basename(filename)}")

    def step_4():
        for widget in root.winfo_children():
            widget.pack_forget()

        mode_label = tk.Label(root, text="Pilih Mode:", font=("Arial", 14), bg="#2B2B2B", fg=fg_color)
        mode_label.pack(pady=20)

        global mode_var
        mode_var = tk.StringVar(value="encrypt")
        encrypt_radio = tk.Radiobutton(root, text="Enkripsi", variable=mode_var, value="encrypt", bg="#2B2B2B", fg=fg_color, selectcolor="#4C4C4C", font=("Arial", 12))
        decrypt_radio = tk.Radiobutton(root, text="Dekripsi", variable=mode_var, value="decrypt", bg="#2B2B2B", fg=fg_color, selectcolor="#4C4C4C", font=("Arial", 12))
        encrypt_radio.pack(pady=5)
        decrypt_radio.pack(pady=5)

        next_button = tk.Button(root, text="Selanjutnya", command=step_5, bg=btn_bg_color, fg=fg_color, font=("Arial", 12), width=20)
        next_button.pack(pady=20)

    def step_5():
        for widget in root.winfo_children():
            widget.pack_forget()

        key = key_entry.get()
        text = input_entry.get() if text_var.get() == "manual" else input_text
        mode = mode_var.get()
        method = method_var.get()

        try:
            if method == "vigenere":
                result = vigenere_cipher(text, key, mode)
            elif method == "playfair":
                result = playfair_cipher(text, key, mode)
            elif method == "hill":
                result = hill_cipher(text, key, mode)
            else:
                result = "Metode tidak dikenal."
        except Exception as e:
            result = f"Error: {str(e)}"

        result_label = tk.Label(root, text="Hasil:", font=("Arial", 14), bg="#2B2B2B", fg=fg_color)
        result_label.pack(pady=20)

        result_text = tk.Text(root, height=10, width=50, bg=entry_bg_color, fg=fg_color, font=("Arial", 12))
        result_text.pack(pady=10)
        result_text.insert(tk.END, result)

        close_button = tk.Button(root, text="Tutup", command=root.quit, bg=btn_bg_color, fg=fg_color, font=("Arial", 12), width=20)
        close_button.pack(pady=20)

    step_1()
    root.mainloop()

if __name__ == "__main__":
    create_gui()
