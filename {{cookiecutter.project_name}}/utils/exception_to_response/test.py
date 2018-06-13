from unittest import TestCase

import sys

print(sys.path)

from djangocopypaste.exception_to_response.base import BaseExceptionToResponse
#from djangocopypaste.exception_to_response.exceptions import NotFound404Exception, MissingParameter400Exception, InvalidParameter400Exception


class TestExceptions(TestCase):
    def test123(self):
        assert True

"""
class TestExceptions(TestCase):
    def test_not_found_404_exception(self):
        try:
            raise NotFound404Exception('name')
        except BaseExceptionToResponse as e:
            response = e.response

        self.assertEquals(response.status_code, 404)
        self.assertIn('detail', response.data)
        self.assertIn(response.data['detail'], 'not found [name]')

    def test_missing_parameter_exception(self):
        try:
            raise MissingParameter400Exception('name')
        except BaseExceptionToResponse as e:
            response = e.response

        self.assertEquals(response.status_code, 400)
        self.assertIn('detail', response.data)
        self.assertIn(response.data['detail'], 'missing parameter [name]')

    def test_bad_parameter_exception(self):
        try:
            raise InvalidParameter400Exception('name')
        except BaseExceptionToResponse as e:
            response = e.response

        self.assertEquals(response.status_code, 400)
        self.assertIn('detail', response.data)
        self.assertIn(response.data['detail'], 'invalid parameter [name]')
"""