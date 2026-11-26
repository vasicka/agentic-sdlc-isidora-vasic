def recognise_digit(glyph):
    if glyph == (" _ ", "| |", "|_|"):
        return "0"
    elif glyph == ("   ", "  |", "  |"):
        return "1"
    elif glyph == (" _ ", " _|", "|_ "):
        return "2"
    return "0"
