import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFont, ImageTk
import json
from datetime import datetime
import os


def get_hex_pattern_by_id(pattern_id):
    json_file = "RIS_patterns.json"  # Nazwa pliku JSON
    with open(json_file, "r") as f:
        data = json.load(f)

    for pattern in data["PATTERNS"]:
        if pattern["ID"] == pattern_id:
            return pattern["HEX"]

    return None  # return None if pattern_id not found


def get_id_pattern_by_hex(hex_pattern):
    json_file = "RIS_patterns.json"  # Nazwa pliku JSON
    with open(json_file, "r") as f:
        data = json.load(f)

    for pattern in data["PATTERNS"]:
        if pattern["HEX"] == hex_pattern:
            return pattern["ID"]

    return None  # return None if hex_pattern not found


def hex_to_bin(hex_string):
    # Usuwamy prefix 0x
    hex_string = hex_string.replace("0x", "")
    # Konwersja hex na binarną z usunięciem prefixu binarnego '0b' i dopełnieniem zerami
    bin_string = "".join(format(int(c, 16), "04b") for c in hex_string)
    return bin_string


def save_image(image):
    # Otwórz okno dialogowe do wyboru miejsca zapisu
    file_path = filedialog.asksaveasfilename(
        defaultextension=".png", filetypes=[("PNG files", "*.png")]
    )
    if file_path:
        image.save(file_path)
        print(f"Obraz zapisano jako: {file_path}")


# Funkcja rysująca GUI na podstawie 4 ciągów binarnych i zapisująca obraz
def generate_image(binary_strings):
    grid_size = 16
    cell_size = 30
    outer_margin = 20
    inner_margin = 4
    pattern_spacing = 30  # Odstęp między patternami
    title_height = 60  # Wysokość dla tytułu nad każdym patternem
    legend_height = 120  # Wysokość dla legendy na dole
    legend_spacing = 40  # Odstęp między patternami a legendą

    # Rozmiar pojedynczego patternu
    single_pattern_width = grid_size * cell_size * 2 + 2 * inner_margin
    single_pattern_height = grid_size * cell_size + 2 * inner_margin

    # Tworzenie obrazu dla 4 patternów w układzie 2x2 z tytułami i legendą
    img_size = (
        2 * single_pattern_width + 3 * outer_margin + pattern_spacing,
        2 * (single_pattern_height + title_height)
        + 3 * outer_margin
        + pattern_spacing
        + legend_spacing
        + legend_height,
    )
    image = Image.new("RGB", img_size, "white")
    draw = ImageDraw.Draw(image)

    # Próba załadowania czcionki
    try:
        title_font = ImageFont.truetype("arial.ttf", 96)  # Większa czcionka dla tytułu
        legend_font = ImageFont.truetype("arial.ttf", 80)
    except:
        title_font = ImageFont.load_default()
        legend_font = ImageFont.load_default()

    # Pozycje dla 4 patternów (2x2) - z uwzględnieniem tytułów
    positions = [
        (outer_margin, outer_margin + title_height),  # Lewy górny
        (
            outer_margin + single_pattern_width + pattern_spacing,
            outer_margin + title_height,
        ),  # Prawy górny
        (
            outer_margin,
            outer_margin
            + title_height
            + single_pattern_height
            + title_height
            + pattern_spacing,
        ),  # Lewy dolny
        (
            outer_margin + single_pattern_width + pattern_spacing,
            outer_margin
            + title_height
            + single_pattern_height
            + title_height
            + pattern_spacing,
        ),  # Prawy dolny
    ]

    # Rysowanie każdego z 4 patternów
    for pattern_idx, binary_string in enumerate(binary_strings):
        if binary_string is None:
            continue

        offset_x, offset_y = positions[pattern_idx]

        # Rysowanie tytułu nad patternem
        title_text = f"Pattern {pattern_idx + 1}"
        # Obliczanie pozycji tytułu (wyśrodkowanie)
        bbox = draw.textbbox((0, 0), title_text, font=title_font)
        text_width = bbox[2] - bbox[0]
        title_x = offset_x + (single_pattern_width + 2 * inner_margin - text_width) // 2
        title_y = offset_y - title_height + 10
        draw.text((title_x, title_y), title_text, fill="black", font=title_font)

        # Rysowanie czarnej otoczki dla patternu
        black_rect_start = (offset_x, offset_y)
        black_rect_end = (
            offset_x + single_pattern_width + 2 * inner_margin,
            offset_y + single_pattern_height + 2 * inner_margin,
        )
        draw.rectangle([black_rect_start, black_rect_end], fill="black")

        # Rysowanie siatki na białym tle
        grid_start_x = offset_x + inner_margin
        grid_start_y = offset_y + inner_margin

        for i in range(256):
            row = i // grid_size
            col = i % grid_size
            color = "blue" if binary_string[i] == "1" else "lightblue"

            # Współrzędne komórki w obrazie
            x1 = grid_start_x + col * cell_size * 2
            y1 = grid_start_y + row * cell_size
            x2 = x1 + cell_size * 2
            y2 = y1 + cell_size
            draw.rectangle([x1, y1, x2, y2], fill=color, outline="black")

    # Rysowanie legendy na dole (poniżej wszystkich patternów)
    # Pozycja Y legendy: dolne patterny + spacing + margines
    legend_y = (outer_margin + title_height + single_pattern_height + title_height + 
                pattern_spacing + single_pattern_height + 2 * inner_margin + legend_spacing)
    legend_x_center = img_size[0] // 2

    # Tytuł legendy
    legend_title = "Legend"
    bbox = draw.textbbox((0, 0), legend_title, font=title_font)
    text_width = bbox[2] - bbox[0]
    draw.text(
        (legend_x_center - text_width // 2, legend_y),
        legend_title,
        fill="black",
        font=title_font,
    )

    # Elementy legendy
    legend_item_y = legend_y + 45
    square_width = 60  # Szerokość prostokąta (2:1 jak w patternach)
    square_height = 30
    spacing = 150

    # ON (niebieski)
    on_x = legend_x_center - spacing
    draw.rectangle(
        [
            on_x - square_width - 10,
            legend_item_y,
            on_x - 10,
            legend_item_y + square_height,
        ],
        fill="blue",
        outline="black",
        width=2,
    )
    draw.text((on_x + 5, legend_item_y + 5), "ON", fill="black", font=legend_font)

    # OFF (jasnoniebieski)
    off_x = legend_x_center + spacing
    draw.rectangle(
        [
            off_x - square_width - 10,
            legend_item_y,
            off_x - 10,
            legend_item_y + square_height,
        ],
        fill="lightblue",
        outline="black",
        width=2,
    )
    draw.text((off_x + 5, legend_item_y + 5), "OFF", fill="black", font=legend_font)

    # Tworzenie okna GUI
    window = tk.Tk()
    window.title("4 Patterns Combined View")

    # Funkcja automatycznego zapisu przy zamknięciu
    def on_closing():
        # Generuj nazwę pliku z timestampem
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"4patterns_{timestamp}.png"

        # Zapisz w bieżącym katalogu
        image.save(filename)
        print(f"Obraz automatycznie zapisano jako: {filename}")

        # Zamknij okno
        window.destroy()

    # Ustaw funkcję wywoływaną przy zamknięciu okna
    window.protocol("WM_DELETE_WINDOW", on_closing)

    outer_frame = tk.Frame(window, bg="white", padx=outer_margin, pady=outer_margin)
    outer_frame.pack()

    # Kontener dla 4 patternów
    patterns_container = tk.Frame(outer_frame, bg="white")
    patterns_container.pack()

    # Rysowanie każdego z 4 patternów w GUI z tytułami
    for pattern_idx, binary_string in enumerate(binary_strings):
        if binary_string is None:
            continue

        pattern_row = pattern_idx // 2
        pattern_col = pattern_idx % 2

        # Kontener dla patternu z tytułem
        pattern_container = tk.Frame(patterns_container, bg="white")
        pattern_container.grid(
            row=pattern_row,
            column=pattern_col,
            padx=pattern_spacing // 2,
            pady=pattern_spacing // 2,
        )

        # Tytuł
        title_label = tk.Label(
            pattern_container,
            text=f"Pattern {pattern_idx + 1}",
            font=("Arial", 42, "bold"),
            bg="white",
        )
        title_label.pack(pady=(0, 5))

        # Ramka z patternem
        inner_frame = tk.Frame(
            pattern_container, bg="black", padx=inner_margin, pady=inner_margin
        )
        inner_frame.pack()

        for i in range(256):
            row = i // grid_size
            col = i % grid_size
            color = "blue" if binary_string[i] == "1" else "lightblue"

            # Rysowanie w GUI
            cell = tk.Frame(
                inner_frame,
                width=cell_size * 2,
                height=cell_size,
                bg=color,
                bd=1,
                relief="solid",
            )
            cell.grid(row=row, column=col)

    # Legenda
    legend_frame = tk.Frame(outer_frame, bg="white", pady=20)
    legend_frame.pack()

    legend_title = tk.Label(
        legend_frame, text="Legend", font=("Arial", 48, "bold"), bg="white"
    )
    legend_title.pack()

    legend_items = tk.Frame(legend_frame, bg="white")
    legend_items.pack(pady=5)

    # ON
    on_color = tk.Frame(
        legend_items, width=140, height=70, bg="blue", bd=3, relief="solid"
    )
    on_color.pack(side="left", padx=5)
    on_label = tk.Label(legend_items, text="ON", font=("Arial", 42), bg="white")
    on_label.pack(side="left", padx=5)

    # Separator
    separator = tk.Label(legend_items, text="  ", bg="white")
    separator.pack(side="left", padx=20)

    # OFF
    off_color = tk.Frame(
        legend_items, width=140, height=70, bg="lightblue", bd=3, relief="solid"
    )
    off_color.pack(side="left", padx=5)
    off_label = tk.Label(legend_items, text="OFF", font=("Arial", 42), bg="white")
    off_label.pack(side="left", padx=5)

    # Dodanie przycisku zapisu obrazu
    save_button = ttk.Button(
        window, text="Zapisz obraz jako PNG", command=lambda: save_image(image)
    )
    save_button.pack(pady=(10, 10))

    window.mainloop()


def get_binary_from_input(pattern_input):
    """Konwertuje ID lub HEX na ciąg binarny"""
    if not pattern_input or pattern_input.strip() == "":
        return None

    pattern_input = pattern_input.strip()

    if pattern_input.startswith("0x"):  # If the input is HEX
        return hex_to_bin(pattern_input)
    else:  # If the input is ID
        hex_pattern = get_hex_pattern_by_id(pattern_input)
        if hex_pattern:
            return hex_to_bin(hex_pattern)
        else:
            print(f"Pattern o ID '{pattern_input}' nie został znaleziony.")
            return None


def on_convert():
    # Pobierz wartości z 4 pól
    binary_strings = []
    for entry in entries:
        pattern_input = entry.get()
        bin_string = get_binary_from_input(pattern_input)
        binary_strings.append(bin_string)

    # Sprawdź czy przynajmniej jeden pattern został wprowadzony
    if all(bs is None for bs in binary_strings):
        print("Błąd: Wprowadź przynajmniej jeden pattern!")
        return

    # Jeśli jakiś pattern nie został podany, użyj pustego (wszystkie 0)
    for i in range(len(binary_strings)):
        if binary_strings[i] is None:
            binary_strings[i] = "0" * 256

    generate_image(binary_strings)


# Ustawienia GUI
root = tk.Tk()
root.title("4-Pattern View Generator")
root.geometry("400x250")

# Tytuł
title_label = ttk.Label(
    root, text="Generator widoku 4 patternów", font=("Arial", 14, "bold")
)
title_label.pack(pady=(15, 10))

# Ramka na pola wprowadzania
input_frame = ttk.LabelFrame(
    root, text="Wprowadź ID lub HEX dla każdego patternu", padding=10
)
input_frame.pack(pady=10, padx=20, fill="both", expand=True)

# Tworzenie 4 pól wprowadzania z etykietami
entries = []
labels_text = [
    "Pattern 1 (lewy górny):",
    "Pattern 2 (prawy górny):",
    "Pattern 3 (lewy dolny):",
    "Pattern 4 (prawy dolny):",
]

for i, label_text in enumerate(labels_text):
    frame = ttk.Frame(input_frame)
    frame.pack(fill="x", pady=3)

    label = ttk.Label(frame, text=label_text, width=25, anchor="w")
    label.pack(side="left")

    entry = ttk.Entry(frame, width=20)
    entry.pack(side="left", padx=5)
    entries.append(entry)

# Przycisk do konwersji
convert_button = ttk.Button(root, text="Generuj obraz 4 patternów", command=on_convert)
convert_button.pack(pady=(10, 15))

# Instrukcja
info_label = ttk.Label(
    root,
    text="Możesz wprowadzić ID (np. '1') lub HEX (np. '0xFFFF...')",
    font=("Arial", 8),
    foreground="gray",
)
info_label.pack()

root.mainloop()
