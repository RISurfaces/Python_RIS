import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageDraw
import json

def get_hex_pattern_by_id(pattern_id):
    json_file = "RIS_patterns.json"  # Nazwa pliku JSON
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    for pattern in data["PATTERNS"]:
        if pattern["ID"] == pattern_id:
            return pattern["HEX"]
    
    return None  # return None if pattern_id not found

def get_id_pattern_by_hex(hex_pattern):
    json_file = "RIS_patterns.json"  # Nazwa pliku JSON
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    for pattern in data["PATTERNS"]:
        if pattern["HEX"] == hex_pattern:
            return pattern["ID"]
    
    return None  # return None if hex_pattern not found

def hex_to_bin(hex_string):
    # Usuwamy prefix 0x
    hex_string = hex_string.replace("0x", "") 
    # Konwersja hex na binarną z usunięciem prefixu binarnego '0b' i dopełnieniem zerami
    bin_string = ''.join(format(int(c, 16),'04b') for c in hex_string)
    return bin_string

# Funkcja rysująca GUI na podstawie ciągu binarnego
def generate_image(binary_string):
    window = tk.Tk()
    window.title("Hex to Binary Grid")

    grid_size = 16
    cell_size = 30
    outer_margin = 10
    inner_margin = 4
    
    outer_frame = tk.Frame(window, bg="white", padx=outer_margin, pady=outer_margin)  # Zewnętrzna ramka z czarnym tłem i marginesami
    outer_frame.pack()

    inner_frame = tk.Frame(outer_frame, bg="black", padx=inner_margin, pady=inner_margin)  # Wewnętrzna ramka
    inner_frame.pack()

    for i in range(256):
        row = i // grid_size
        col = i % grid_size
        color = "green" if binary_string[i] == '1' else "#C0F6C7"
        cell = tk.Frame(inner_frame, width=cell_size*2, height=cell_size, bg=color, highlightbackground="black", highlightthickness=1)
        cell.grid(row=row, column=col)
    
    window.mainloop()

def on_convert():
    pattern_id_or_hex = entry.get()
    if pattern_id_or_hex.startswith("0x"): # If the input is HEX
        bin_string = hex_to_bin(pattern_id_or_hex)
        generate_image(bin_string)
    else: # If the input is ID
        hex_pattern = get_hex_pattern_by_id(pattern_id_or_hex)
        if hex_pattern:
            bin_string = hex_to_bin(hex_pattern)
            generate_image(bin_string)
        else:
            print("Pattern o podanym ID nie został znaleziony.")

# Ustawienia GUI
root = tk.Tk()
root.title("Hex to Bin Image Converter")

# Etykieta i pole wprowadzania
label = ttk.Label(root, text="Podaj ID patternu lub HEX:")
label.pack(pady=(10, 5))  # Zwiększone pady na górze i dołu
entry = ttk.Entry(root)
entry.pack(pady=(0, 5))  # Zwiększony pady na dole

# Przycisk do konwersji
convert_button = ttk.Button(root, text="Konwertuj i pokaż obraz", command=on_convert)
convert_button.pack(pady=(0, 10))  # Zwiększony pady na dole

root.mainloop()
