# -*- coding: utf-8 -*-

import string

def validate_ISBN10(isbn):
    """
    Validate ISBN10 code. Returns the ISBN or False if is not valid.
    """
    isbn = isbn.replace("-", "").replace(" ", "")

    if len(isbn) == 10 and not [x for x in isbn if x not in (
            string.digits + "X")]:

        total = 0
        for i in range(9):
            total += int(isbn[i]) * (10 - i)
        z = (11 - (total % 11)) % 11
        if (z == 10 and isbn[-1] == 'X') or ("%d" % z == isbn[-1]):
            return isbn
        else:
            return False

def validate_ISBN13(isbn):
    """
    Validate ISBN13 code. Returns the ISBN or False if is not valid.
    """
    #El chequeo para ISBN de 13 digitos sale de:
    #ref: http://en.wikipedia.org/wiki/International_Standard_Book_Number#ISBN-13

    isbn = isbn.replace("-", "").replace(" ", "")

    if len(isbn) == 13 and not [x for x in isbn if x not in string.digits]:
        i = 1
        total = 0
        for n in isbn[:-1]:
            total = total + i * int(n)
            if i == 1: i = 3
            else: i = 1
        check = 10 - ( total % 10 )
        if check == int(isbn[-1]):
            return isbn
        else:
            return False

def validate_ISBN(isbn):
    """
    Validate ISBN13 or ISBN10 code. Returns the ISBN or False if any is valid.
    """
    return validate_ISBN10(isbn) or validate_ISBN13(isbn)
    