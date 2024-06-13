
def ris_pattern_negation(ris_pattern : str) -> str:
    ris_pattern = int(ris_pattern,16)
    ris_pattern = ~ris_pattern & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
    ris_pattern = hex(ris_pattern)
    ris_pattern = str(ris_pattern)
    no_of_zero_to_add = 66 - len(ris_pattern)
    for i in range(no_of_zero_to_add):
        ris_pattern = ris_pattern[:2] + '0' + ris_pattern [2:]
    return ris_pattern

ris_pattern = '0xFF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00FF00'
ris_pattern_neg = ris_pattern_negation(ris_pattern)
print(ris_pattern_neg)