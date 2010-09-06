# -*- coding: utf-8 -*-

import string


def valida_ISBN10(isbn):
    """
    Validar codigo ISBN 10. Devuelve el ISBN ó False si no es válido.
    """
    #TODO: deberia validar el ISBN con la cuenta
    # No entiendo este TODO
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

def valida_ISBN13(isbn):
    """
    Validar codigo ISBN 13. Devuelve el ISBN ó False si no es válido.
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

def valida_ISBN(isbn):
    """
    Validar codigo ISBN 10 o 13. Devuelve el ISBN ó False si no es válido.
    """
    return valida_ISBN10(isbn) or valida_ISBN13(isbn)
