import abc

from rest_framework.response import Response


class BaseExceptionToResponse(Exception, abc.ABC):
    content_type = 'application/json'

    def __init__(self, param: str):
        self.param = param

    @property
    @abc.abstractmethod
    def status(self) -> int:
        pass

    @property
    @abc.abstractmethod
    def data(self) -> dict:
        pass

    @property
    def response(self) -> Response:
        return Response(status=self.status, data=self.data, content_type=self.content_type)