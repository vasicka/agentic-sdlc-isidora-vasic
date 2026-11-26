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
    return "0"
