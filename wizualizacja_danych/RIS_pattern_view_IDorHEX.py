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
    
    for i in range(256):
        row = i // grid_size
        col = i % grid_size
        color = "green" if binary_string[i] == '1' else "white"
        canvas = tk.Canvas(window, width=cell_size*2, height=cell_size , highlightthickness=0)
        canvas.create_rectangle(1, 1, cell_size*2, cell_size, fill=color, outline=color)
        canvas.grid(row=row, column=col, padx=(0.1), pady=(0.1))
        
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
label.pack()
entry = ttk.Entry(root)
entry.pack()

# Przycisk do konwersji
convert_button = ttk.Button(root, text="Konwertuj i pokaż obraz", command=on_convert)
convert_button.pack()

root.mainloop()
