from abc import ABC, abstractmethod
from dataclasses import dataclass, fields
from enum import Enum, Flag, auto
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from requests import Request


class Season(Enum):
    """A enum of seasons to filter by

    Attributes:
        SPRING:
        SUMMER:
        FALL:
        WINTER:
    """

    SPRING = auto()
    SUMMER = auto()
    FALL = auto()
    WINTER = auto()


class Status(Enum):
    """A enum of anime states to filter by

    Attributes:
        UPCOMING:
        ONGOING:
        COMPLETED:
    """

    UPCOMING = auto()
    ONGOING = auto()
    COMPLETED = auto()


class MediaType(Enum):
    """A enum of mediatypes to filter by

    Attributes:
        TV:
        MOVIE:
        OVA:
        ONA:
        SPECIAL:
        MUSIC:
    """

    TV = auto()
    MOVIE = auto()
    OVA = auto()
    ONA = auto()
    SPECIAL = auto()
    MUSIC = auto()


@dataclass
class Filters:
    """A flter class that acts as a filter collection

    Attributes:
        year: The year to filter by
        season: The season to filter by
        status: The status to filter by
        media_type: The media type to filter by
    """

    year: Optional[List[int]] = None
    season: Optional[List[Season]] = None
    status: Optional[List[Status]] = None
    media_type: Optional[List[MediaType]] = None


class FilterCapabilities(Flag):
    """A Flag class that describes the filter capabilities of a provider. Look [here](https://docs.python.org/3/library/enum.html#enum.Flag) to learn how to use this.

    Attributes:
        YEAR:
        SEASON:
        STATUS:
        MEDIA_TYPE:
        ALL:
    """

    YEAR = auto()
    SEASON = auto()
    STATUS = auto()
    MEDIA_TYPE = auto()
    ALL = YEAR | SEASON | STATUS | MEDIA_TYPE


class BaseFilter(ABC):
    def __init__(self, request: "Request"):
        self._request = request

    @abstractmethod
    def _apply_query(self, query: str): ...

    @abstractmethod
    def _apply_year(self, year: List[int]): ...

    @abstractmethod
    def _apply_season(self, season: List[Season]): ...

    @abstractmethod
    def _apply_status(self, status: List[Status]): ...

    @abstractmethod
    def _apply_media_type(self, media_type: List[MediaType]): ...

    @staticmethod
    def _map_enum_members(values, map):
        mapped = []
        for m in values:
            mapped.append(map[m])
        return mapped

    def apply(self, query: str, filters: Filters) -> "Request":
        self._apply_query(query)

        for filter in fields(filters):
            value = getattr(filters, filter.name)
            if not value:
                continue

            func = self.__getattribute__(f"_apply_{filter.name}")
            func(value)

        return self._request
