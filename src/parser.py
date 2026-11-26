def recognise_digit(glyph):
    if glyph == (" _ ", "| |", "|_|"):
        return "0"
    elif glyph == ("   ", "  |", "  |"):
        return "1"
    return "0"
