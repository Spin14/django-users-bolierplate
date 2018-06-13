from rest_framework import status

from .base import BaseExceptionToResponse


class NotFound404Exception(BaseExceptionToResponse):
    @property
    def status(self) -> int:
        return status.HTTP_404_NOT_FOUND

    @property
    def data(self) -> dict:
        return {'detail': 'not found [{}]'.format(self.param)}


class MissingParameter400Exception(BaseExceptionToResponse):
    @property
    def status(self) -> int:
        return status.HTTP_400_BAD_REQUEST

    @property
    def data(self) -> dict:
        return {'detail': 'missing parameter [{}]'.format(self.param)}


class InvalidParameter400Exception(BaseExceptionToResponse):
    @property
    def status(self) -> int:
        return status.HTTP_400_BAD_REQUEST

    @property
    def data(self) -> dict:
        return {'detail': 'invalid parameter [{}]'.format(self.param)}
