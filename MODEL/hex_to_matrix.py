import csv

def hex_to_bin(pattern: str, rows: int, columns: int) -> str:
    pattern = pattern.removeprefix("0x")
    bin_str = str(bin(int(pattern, 16)))
    bin_str = bin_str.removeprefix("0b")
    no_zeros_to_add = (rows * columns) - len(bin_str)
    for i in range(no_zeros_to_add):
        bin_str = "0" + bin_str
    return bin_str

def create_matrix(bin_str: str, rows: int, columns: int) -> list:
    ris_matrix = []
    i = 0
    for row in range(rows):
        a = []
        for column in range(columns):
            a.append(int(bin_str[i]))
            i += 1
        ris_matrix.append(a)
    return ris_matrix

def save_matrix_to_csv(matrix: list, filename: str) -> None:
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(matrix)

def A_coeff(bin_str: str, A_coeff_min: float, A_coeff_max: float, rows: int, columns: int) -> float:
    no_of_all_elemnts = rows * columns
    no_of_turn_on_elemnts = bin_str.count("1")
    A_treshold = A_coeff_max - A_coeff_min
    print(no_of_turn_on_elemnts)
    return A_coeff_min + (no_of_turn_on_elemnts / no_of_all_elemnts) * A_treshold

if __name__ == '__main__':
    bin_str = hex_to_bin(
        "0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF", 16, 16
    )
    print("HEX przekonwertowany na BIN: ", bin_str)
    ris_matrix = create_matrix(bin_str, 16, 16)
    print("HEX przekonwertowany na macierz: ", ris_matrix)
    save_matrix_to_csv(ris_matrix, "matrix.csv")
    print("Macierz została zapisana do pliku 'matrix.csv'")
    a_coeff = A_coeff(bin_str, -5, -1.9, 16, 16)  # for 5.5Ghz
    print("Współczynnik a: ", a_coeff)
