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


def test_parsing_be_001_1_s001_given_five_glyph_when_recognised_then_returns_five():
    from src.parser import recognise_digit

    # GIVEN
    glyph = (" _ ", "|_ ", " _|")

    # WHEN
    result = recognise_digit(glyph)

    # THEN
    assert result == "5"


def test_parsing_be_001_1_s001_given_six_glyph_when_recognised_then_returns_six():
    from src.parser import recognise_digit

    # GIVEN
    glyph = (" _ ", "|_ ", "|_|")

    # WHEN
    result = recognise_digit(glyph)

    # THEN
    assert result == "6"


def test_parsing_be_001_1_s001_given_seven_glyph_when_recognised_then_returns_seven():
    from src.parser import recognise_digit

    # GIVEN
    glyph = (" _ ", "  |", "  |")

    # WHEN
    result = recognise_digit(glyph)

    # THEN
    assert result == "7"


def test_parsing_be_001_1_s001_given_eight_glyph_when_recognised_then_returns_eight():
    from src.parser import recognise_digit

    # GIVEN
    glyph = (" _ ", "|_|", "|_|")

    # WHEN
    result = recognise_digit(glyph)

    # THEN
    assert result == "8"


def test_parsing_be_001_1_s001_given_nine_glyph_when_recognised_then_returns_nine():
    from src.parser import recognise_digit

    # GIVEN
    glyph = (" _ ", "|_|", " _|")

    # WHEN
    result = recognise_digit(glyph)

    # THEN
    assert result == "9"


def test_parsing_be_001_1_s002_given_complete_entry_with_nine_zeros():
    from src.parser import parse_entry

    # GIVEN
    # A four-line entry with nine zeros
    entry = (
        " _  _  _  _  _  _  _  _  _ ",
        "| || || || || || || || || |",
        "|_||_||_||_||_||_||_||_||_|",
        "",
    )

    # WHEN
    result = parse_entry(entry)

    # THEN
    assert result == "000000000"


def test_parsing_be_001_1_s002_given_complete_entry_with_123456789():
    from src.parser import parse_entry

    # GIVEN
    # A four-line entry with digits 123456789
    # Based on BankOCR kata examples
    entry = (
        "    _  _     _  _  _  _  _ ",
        "  | _| _||_||_ |_   ||_||_|",
        "  ||_  _|  | _||_|  ||_| _|",
        "",
    )

    # WHEN
    result = parse_entry(entry)

    # THEN
    assert result == "123456789"
