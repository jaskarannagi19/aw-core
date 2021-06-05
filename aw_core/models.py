import json
import logging
import numbers
from os import name
import typing
from datetime import datetime, timedelta, timezone
from typing import Any, List, Dict, Union, Optional

import iso8601

logger = logging.getLogger(__name__)


Number = Union[int, float]
Id = Optional[Union[int, str]]
ConvertableTimestamp = Union[datetime, str]
Duration = Union[timedelta, Number]
Data = Dict[str, Any]

name=Union[str, str]
email=Union[str, str]
age=Union[int, int]
userfrom=Union[str, str]
timeskills=Union[str, str]
unproductive_websites=Union[str, str]
productive_websites=Union[str, str]

def _timestamp_parse(ts_in: ConvertableTimestamp) -> datetime:
    """
    Takes something representing a timestamp and
    returns a timestamp in the representation we want.
    """
    ts = iso8601.parse_date(ts_in) if isinstance(ts_in, str) else ts_in
    # Set resolution to milliseconds instead of microseconds
    # (Fixes incompability with software based on unix time, for example mongodb)
    ts = ts.replace(microsecond=int(ts.microsecond / 1000) * 1000)
    # Add timezone if not set
    if not ts.tzinfo:
        # Needed? All timestamps should be iso8601 so ought to always contain timezone.
        # Yes, because it is optional in iso8601
        logger.warning("timestamp without timezone found, using UTC: {}".format(ts))
        ts = ts.replace(tzinfo=timezone.utc)
    return ts

class UserInfo(dict):
    def __init__(
        self,
        id: Id = None,
        name: name=None,
        email: email=None,
        age: age=0,
        userfrom: userfrom=None,
        timeskills:timeskills=None,
        unproductive_websites:unproductive_websites=None,
        productive_websites:productive_websites=None
    ) -> None:
        self.id 
        self.email = email
        self.age=age  
        self.userfrom=userfrom
        self.timeskills=timeskills
        self.unproductive_websites=unproductive_websites
        self.productive_websites=productive_websites
        self.name = name


    def __eq__(self, other: object) -> bool:
        if isinstance(other, UserInfo):
            return (
                self.email == other.email
                and self.age == other.age
                and self.name == other.name
            )
        else:
            raise TypeError(
                "operator not supported between instances of '{}' and '{}'".format(
                    type(self), type(other)
                )
            )

    def __lt__(self, other: object) -> bool:
        if isinstance(other, UserInfo):
            return self.email 
        else:
            raise TypeError(
                "operator not supported between instances of '{}' and '{}'".format(
                    type(self), type(other)
                )
            )

    def to_json_dict(self) -> dict:
        """Useful when sending data over the wire.
        Any mongodb interop should not use do this as it accepts datetimes."""
        json_data = self.copy()
        return json_data

    def to_json_str(self) -> str:
        data = self.to_json_dict()
        return json.dumps(data)

    def _hasprop(self, propname: str) -> bool:
        """Badly named, but basically checks if the underlying
        dict has a prop, and if it is a non-empty list"""
        return propname in self and self[propname] is not None

    @property
    def id(self) -> Id:
        return self["id"] if self._hasprop("id") else None

    @id.setter
    def id(self, id: Id) -> None:
        self["id"] = id


    @property
    def name(self) -> name:
        return self["name"] if self._hasprop("name") else None

    @name.setter
    def name(self, name: name) -> None:
        self["name"] = name

    @property
    def email(self) -> email:
        return self["email"] if self._hasprop("email") else None

    @email.setter
    def email(self, email: email) -> None:
        self["email"] = email

    @property
    def age(self) -> age:
        return self["age"] if self._hasprop("age") else None

    @age.setter
    def age(self, age: age) -> None:
        self["age"] = age

    @property
    def userfrom(self) -> userfrom:
        return self["userfrom"] if self._hasprop("userfrom") else None

    @age.setter
    def userfrom(self, userfrom: userfrom) -> None:
        self["userfrom"] = userfrom

    @property
    def timeskills(self) -> timeskills:
        return self["timeskills"] if self._hasprop("timeskills") else None

    @age.setter
    def timeskills(self, timeskills: timeskills) -> None:
        self["timeskills"] = timeskills

    @property
    def unproductive_websites(self) -> unproductive_websites:
        return self["unproductive_websites"] if self._hasprop("unproductive_websites") else None

    @age.setter
    def unproductive_websites(self, unproductive_websites: unproductive_websites) -> None:
        self["unproductive_websites"] = unproductive_websites


    @property
    def productive_websites(self) -> productive_websites:
        return self["productive_websites"] if self._hasprop("productive_websites") else None

    @age.setter
    def productive_websites(self, productive_websites: productive_websites) -> None:
        self["productive_websites"] = productive_websites

  

    # @property
    # def data(self) -> dict:
    #     return self["data"] if self._hasprop("data") else {}

    # @data.setter
    # def data(self, data: dict) -> None:
    #     self["data"] = data

    # @property
    # def timestamp(self) -> datetime:
    #     return self["timestamp"]

    # @timestamp.setter
    # def timestamp(self, timestamp: ConvertableTimestamp) -> None:
    #     self["timestamp"] = _timestamp_parse(timestamp).astimezone(timezone.utc)

    # @property
    # def duration(self) -> timedelta:
    #     return self["duration"] if self._hasprop("duration") else timedelta(0)

    # @duration.setter
    # def duration(self, duration: Duration) -> None:
    #     if isinstance(duration, timedelta):
    #         self["duration"] = duration
    #     elif isinstance(duration, numbers.Real):
    #         self["duration"] = timedelta(seconds=duration)  # type: ignore
    #     else:
    #         raise TypeError(
    #             "Couldn't parse duration of invalid type {}".format(type(duration))
    #         )
















class Event(dict):
    """
    Used to represents an event.
    """

    def __init__(
        self,
        id: Id = None,
        timestamp: ConvertableTimestamp = None,
        duration: Duration = 0,
        data: Data = dict(),
    ) -> None:
        self.id = id
        if timestamp is None:
            logger.warning(
                "Event initializer did not receive a timestamp argument, using now as timestamp"
            )
            # FIXME: The typing.cast here was required for mypy to shut up, weird...
            self.timestamp = datetime.now(typing.cast(timezone, timezone.utc))
        else:
            # The conversion needs to be explicit here for mypy to pick it up (lacks support for properties)
            self.timestamp = _timestamp_parse(timestamp)
        self.duration = duration  # type: ignore
        self.data = data

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Event):
            return (
                self.timestamp == other.timestamp
                and self.duration == other.duration
                and self.data == other.data
            )
        else:
            raise TypeError(
                "operator not supported between instances of '{}' and '{}'".format(
                    type(self), type(other)
                )
            )

    def __lt__(self, other: object) -> bool:
        if isinstance(other, Event):
            return self.timestamp < other.timestamp
        else:
            raise TypeError(
                "operator not supported between instances of '{}' and '{}'".format(
                    type(self), type(other)
                )
            )

    def to_json_dict(self) -> dict:
        """Useful when sending data over the wire.
        Any mongodb interop should not use do this as it accepts datetimes."""
        json_data = self.copy()
        json_data["timestamp"] = self.timestamp.astimezone(timezone.utc).isoformat()
        json_data["duration"] = self.duration.total_seconds()
        return json_data

    def to_json_str(self) -> str:
        data = self.to_json_dict()
        return json.dumps(data)

    def _hasprop(self, propname: str) -> bool:
        """Badly named, but basically checks if the underlying
        dict has a prop, and if it is a non-empty list"""
        return propname in self and self[propname] is not None

    @property
    def id(self) -> Id:
        return self["id"] if self._hasprop("id") else None

    @id.setter
    def id(self, id: Id) -> None:
        self["id"] = id

    @property
    def data(self) -> dict:
        return self["data"] if self._hasprop("data") else {}

    @data.setter
    def data(self, data: dict) -> None:
        self["data"] = data

    @property
    def timestamp(self) -> datetime:
        return self["timestamp"]

    @timestamp.setter
    def timestamp(self, timestamp: ConvertableTimestamp) -> None:
        self["timestamp"] = _timestamp_parse(timestamp).astimezone(timezone.utc)

    @property
    def duration(self) -> timedelta:
        return self["duration"] if self._hasprop("duration") else timedelta(0)

    @duration.setter
    def duration(self, duration: Duration) -> None:
        if isinstance(duration, timedelta):
            self["duration"] = duration
        elif isinstance(duration, numbers.Real):
            self["duration"] = timedelta(seconds=duration)  # type: ignore
        else:
            raise TypeError(
                "Couldn't parse duration of invalid type {}".format(type(duration))
            )
