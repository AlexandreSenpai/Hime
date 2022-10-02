"""This module handles the generic entity definition.
"""

from dataclasses import asdict, dataclass
import datetime
from typing import Dict
import uuid

@dataclass
class Entity:
    """This class its a generic entity class.
    """
    _id: str = None
    _created_at: datetime.datetime = None
    _updated_at: datetime.datetime = None

    def __init__(self,
                 entity_id: str,
                 created_at: datetime.datetime,
                 updated_at: datetime.datetime):

        self._id = entity_id if entity_id is not None else str(uuid.uuid4())
        self._created_at = created_at if created_at is not None else datetime.datetime.now()
        self._updated_at = updated_at if updated_at is not None else datetime.datetime.now()


    @property
    def id(self) -> str:
        """This method returns the entity id.

        Returns:
            str: current entity id
        """
        return self._id

    @property
    def created_at(self) -> datetime.datetime:
        """This method returns the entity creation date.

        Returns:
            datetime.datetime: current entity creation date.
        """
        return self._created_at

    @property
    def updated_at(self) -> datetime.datetime:
        """This method returns the entity update date.

        Returns:
            datetime.datetime: current entity updated date
        """
        return self._updated_at
    
    @property
    def data(self) -> Dict[str, any]:
        return asdict(self)