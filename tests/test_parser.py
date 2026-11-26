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


def test_parsing_be_001_1_s001_given_two_glyph_when_recognised_then_returns_two():
    from src.parser import recognise_digit

    # GIVEN
    glyph = (" _ ", " _|", "|_ ")

    # WHEN
    result = recognise_digit(glyph)

    # THEN
    assert result == "2"


def test_parsing_be_001_1_s001_given_three_glyph_when_recognised_then_returns_three():
    from src.parser import recognise_digit

    # GIVEN
    glyph = (" _ ", " _|", " _|")

    # WHEN
    result = recognise_digit(glyph)

    # THEN
    assert result == "3"


def test_parsing_be_001_1_s001_given_four_glyph_when_recognised_then_returns_four():
    from src.parser import recognise_digit

    # GIVEN
    glyph = ("   ", "|_|", "  |")

    # WHEN
    result = recognise_digit(glyph)

    # THEN
    assert result == "4"
