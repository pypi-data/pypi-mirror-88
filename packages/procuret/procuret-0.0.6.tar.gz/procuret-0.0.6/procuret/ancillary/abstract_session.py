"""
Procuret Python
Abstract Session Module
author: hugh@blinkybeach.com
"""
from procuret.ancillary.session_lifecycle import Lifecycle
from procuret.ancillary.session_perspective import Perspective
from procuret.data.codable import Codable


class AbstractSession(Codable):

    session_id: int
    session_key: str
    api_key: str
    lifecycle: Lifecycle
    perspective: Perspective
