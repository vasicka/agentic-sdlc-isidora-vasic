def recognise_digit(glyph):
    if glyph == (" _ ", "| |", "|_|"):
        return "0"
    elif glyph == ("   ", "  |", "  |"):
        return "1"
    elif glyph == (" _ ", " _|", "|_ "):
        return "2"
    elif glyph == (" _ ", " _|", " _|"):
        return "3"
    elif glyph == ("   ", "|_|", "  |"):
        return "4"
    elif glyph == (" _ ", "|_ ", " _|"):
        return "5"
    elif glyph == (" _ ", "|_ ", "|_|"):
        return "6"
    elif glyph == (" _ ", "  |", "  |"):
        return "7"
    elif glyph == (" _ ", "|_|", "|_|"):
        return "8"
    elif glyph == (" _ ", "|_|", " _|"):
        return "9"
    return "0"


def parse_entry(entry):
    # Extract the three glyph rows (ignore the blank line)
    row1, row2, row3, _ = entry

    result = ""
    for i in range(9):
        # Extract 3-character segments from each row
        start = i * 3
        end = start + 3
        glyph = (row1[start:end], row2[start:end], row3[start:end])
        result += recognise_digit(glyph)

    return result
