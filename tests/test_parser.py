def test_parsing_be_001_1_s001_recognise_zero():
    from src.parser import recognise_digit

    # GIVEN
    glyph = (" _ ", "| |", "|_|")

    # WHEN
    result = recognise_digit(glyph)

    # THEN
    assert result == "0"


def test_parsing_be_001_1_s001_given_one_glyph_when_recognised_then_returns_one():
    from src.parser import recognise_digit

    # GIVEN
    glyph = ("   ", "  |", "  |")

    # WHEN
    result = recognise_digit(glyph)

    # THEN
    assert result == "1"
