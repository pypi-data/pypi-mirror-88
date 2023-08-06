"""
Procuret Python
Session Module
author: hugh@blinkybeach.com
"""
from procuret.data.codable import CodingDefinition as CD
from procuret.ancillary.abstract_session import AbstractSession
from procuret.ancillary.session_lifecycle import Lifecycle
from procuret.ancillary.session_perspective import Perspective
from procuret.http.api_request import ApiRequest
from procuret.http.method import HTTPMethod
from typing import TypeVar, Type
from procuret.errors.inconsistent import InconsistentState

T = TypeVar('T', bound='Session')


class Session(AbstractSession):

    PATH = '/session'

    coding_map = {
        'session_id': CD(int),
        'session_key': CD(str),
        'api_key': CD(str),
        'lifecycle': CD(Lifecycle),
        'perspective': CD(Perspective)
    }

    def __init__(
        self,
        session_id: int,
        session_key: str,
        api_key: str,
        lifecycle: Lifecycle,
        perspective: Perspective
    ) -> None:

        self._session_id = session_id
        self._session_key = session_key
        self._api_key = api_key
        self._lifecycle = lifecycle
        self._perspective = perspective

        return

    session_id = property(lambda s: s._session_id)
    session_key = property(lambda s: s._session_key)
    api_key = property(lambda s: s._api_key)
    lifecycle = property(lambda s: s._lifecycle)
    perspective = property(lambda s: s._perspective)

    @classmethod
    def create_with_email(
        cls: Type[T],
        email: str,
        plaintext_secret: str,
        perspective: Perspective,
        lifecycle: Lifecycle = Lifecycle.LONG_LIVED
    ) -> T:

        data = {
            'email': email,
            'secret': plaintext_secret,
            'perspective': perspective.value,
            'lifecycle': lifecycle.value
        }

        result = ApiRequest.make(
            path=cls.PATH,
            method=HTTPMethod.POST,
            data=data,
            session=None,
            query_parameters=None
        )
        if result is None:
            raise InconsistentState

        return cls.decode(result)
