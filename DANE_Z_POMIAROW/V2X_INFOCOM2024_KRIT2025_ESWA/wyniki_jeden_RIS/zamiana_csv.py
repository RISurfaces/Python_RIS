import os
import re

# =========================
# CONFIG
# =========================
folder = "jeden_ris_wyniki"
N = 26

# =========================
# STEP 1: MAPOWANIE
# =========================
files = os.listdir(folder)

pattern = re.compile(r"^(.*_)(\d+)\.csv$")

rename_map = {}

for fname in files:
    match = pattern.match(fname)
    if not match:
        continue

    prefix, num = match.groups()
    num = int(num)

    if 1 <= num <= N:
        new_num = N - num + 1
        new_name = f"{prefix}{new_num}.csv"
        rename_map[fname] = new_name

# =========================
# STEP 2: RENAME → TEMP
# =========================
for old, new in rename_map.items():
    temp_name = old + ".tmp"
    os.rename(
        os.path.join(folder, old),
        os.path.join(folder, temp_name)
    )

# =========================
# STEP 3: TEMP → FINAL
# =========================
for old, new in rename_map.items():
    temp_name = old + ".tmp"
    os.rename(
        os.path.join(folder, temp_name),
        os.path.join(folder, new)
    )

print("✅ Zakończono: numeracja plików została odwrócona (1↔26, 2↔25, ...).")
