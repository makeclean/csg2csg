from csg2csg.MCNPFormatter import get_fortran_formatted_number


def test_fortran_format():
    string = "-1.0-1"
    number = get_fortran_formatted_number(string)
    assert number == -1.0e-1

    string = "-1.0+1"
    number = get_fortran_formatted_number(string)
    assert number == -1.0e1

    string = "1.0+1"
    number = get_fortran_formatted_number(string)
    assert number == 1.0e1

    string = "15.0-100"
    number = get_fortran_formatted_number(string)
    assert number == 1.5e-99

    string = "-15.0+39"
    number = get_fortran_formatted_number(string)
    assert number == -1.5e40

    string = "-15.0+309"
    number = get_fortran_formatted_number(string)
    assert number == -1.5e310

    string = "6.1000"
    number = get_fortran_formatted_number(string)
    assert number == 6.1000

    string = "-6.1000"
    number = get_fortran_formatted_number(string)
    assert number == -6.1000
