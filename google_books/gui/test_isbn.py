# -*- coding: utf-8 -*-

import unittest

from utils import valida_ISBN, valida_ISBN10, valida_ISBN13

GOOD_ISBN10 = '0-596-10046-9'
GOOD_ISBN10_EXPECTED = '0596100469'
BAD_ISBN10 = '0-596-10046'
ISBN10X = '84-205-3014-X'
ISBN10X_EXPECTED = '842053014X'
GOOD_ISBN13 = '978-05-961-0046-9'
GOOD_ISBN13_EXPECTED = '9780596100469'
BAD_ISBN13 = '978-05-961-0046'


class TestISBN(unittest.TestCase):

    def test_any_isbn_ok(self):
        isbn = valida_ISBN(GOOD_ISBN10)
        expected_isbn = GOOD_ISBN10_EXPECTED
        self.assertEqual(expected_isbn, isbn)

        isbn = valida_ISBN(ISBN10X)
        expected_isbn = ISBN10X_EXPECTED
        self.assertEqual(expected_isbn, isbn)

        isbn = valida_ISBN(GOOD_ISBN13)
        expected_isbn = GOOD_ISBN13_EXPECTED
        self.assertEqual(expected_isbn, isbn)

    def test_any_isbn_ibad(self):
        self.fail()

    def test_any_isbn_none(self):
        isbn = valida_ISBN(BAD_ISBN10)
        self.assertEqual(isbn, None)

        isbn = valida_ISBN(BAD_ISBN13)
        self.assertEqual(isbn, None)

    def test_isbn13_ok(self):
        isbn = valida_ISBN(GOOD_ISBN13)
        expected_isbn = GOOD_ISBN13_EXPECTED
        self.assertEqual(expected_isbn, isbn)

    def test_isbn13_bad(self):
        self.fail()

    def test_isbn13_none(self):
        isbn = valida_ISBN13(BAD_ISBN13)
        self.assertEqual(isbn, None)

    def test_isbn10_ok(self):
        isbn = valida_ISBN(GOOD_ISBN10)
        expected_isbn = GOOD_ISBN10_EXPECTED
        self.assertEqual(expected_isbn, isbn)

        isbn = valida_ISBN(ISBN10X)
        expected_isbn = ISBN10X_EXPECTED
        self.assertEqual(expected_isbn, isbn)

    def test_isbn10_bad(self):
        self.fail()

    def test_isbn10_none(self):
        isbn = valida_ISBN(BAD_ISBN10)
        self.assertEqual(isbn, None)


if __name__ == '__main__':
    unittest.main()
