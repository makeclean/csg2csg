from csg2csg.MCNPCellCard import MCNPCellCard, mcnp_line_formatter


# TODO definitely add some more robust testing of the position of the
# logical operations - Very Important


def test_simple_cell():
    card_string = "1 1 -1.0 -4 5 -6 7"
    card = MCNPCellCard(card_string)
    assert card.text_string == card_string
    assert card.cell_id == 1
    assert card.cell_density == -1.0


def test_more_complex_cell():
    card_string = "2 3 -14.0 (-4 5 -6 7):(9 12 13)"
    card = MCNPCellCard(card_string)
    assert card.text_string == card_string
    assert card.cell_id == 2
    assert card.cell_material_number == 3
    assert card.cell_density == -14.0


def test_mcnp_detect_keywords_all():
    string = "2 3 -14.0 1 imp:n=1 imp:p=1 u=3 fill=12 vol=150"
    cell_card = MCNPCellCard(string)
    new_string = cell_card._MCNPCellCard__detect_keywords(
        ["imp", "u", "fill", "vol"], string
    )
    assert new_string == "2 3 -14.0 1 "


def test_mcnp_detect_keywords_imp():
    string = "2 3 -14.0 1 imp:n=1 imp:p=1 "
    cell_card = MCNPCellCard(string)
    new_string = cell_card._MCNPCellCard__detect_keywords(["imp"], string)
    assert new_string == "2 3 -14.0 1 "


def test_mcnp_detect_keywords_uni():
    string = "2 3 -14.0 1 u=1 "
    cell_card = MCNPCellCard(string)
    new_string = cell_card._MCNPCellCard__detect_keywords(["u"], string)
    assert new_string == "2 3 -14.0 1 "


def test_mcnp_detect_keywords_fill():
    string = "2 3 -14.0 1 fill=3"
    cell_card = MCNPCellCard(string)
    new_string = cell_card._MCNPCellCard__detect_keywords(["fill"], string)
    assert new_string == "2 3 -14.0 1 "


def test_mcnp_detect_keywords_vol():
    string = "2 3 -14.0 1 vol=300"
    cell_card = MCNPCellCard(string)
    new_string = cell_card._MCNPCellCard__detect_keywords(["vol"], string)
    assert new_string == "2 3 -14.0 1 "


def test_mcnp_detect_keywords_tmp():
    string = "2 3 -14.0 1 tmp=300"
    cell_card = MCNPCellCard(string)
    new_string = cell_card._MCNPCellCard__detect_keywords(["tmp"], string)
    assert new_string == "2 3 -14.0 1 "


def test_mcnp_line_format():
    string = "1 0 (-1 3 4 5 6 8 9 ( 12 13 15))"
    mcnp_string = mcnp_line_formatter(string)
    assert string == mcnp_string
    # note these horrendously long lines - is actually what im trying to test and furthermore
    # all of the standard techniques to break the string across multuple lines like
    # https://stackoverflow.com/questions/5437619/python-style-line-continuation-with-strings
    # dont actually work
    string = "1 0 (-1 3 4 5 6 8 9 ( 12 13 15) ( 12 13 15) ( 12 13 15) ( 12 13 15) ( 12 13 15))"
    result = mcnp_line_formatter(string)
    assert result == (
        "1 0 (-1 3 4 5 6 8 9 ( 12 13 15) ( 12 13 15) ( 12 13 15) ( 12 13 15) (\n      12 13 15))"
    )
