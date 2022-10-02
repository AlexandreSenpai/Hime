from dataclasses import dataclass, field
import datetime
from dataclasses import dataclass

from hime.application.core.entities.entity import Entity


@dataclass
class Language:
    source: str = field(default='')
    target: str = field(default='')

@dataclass
class Translation(Entity):
    
    language: Language = Language()
    text: str = ""
    original: str = ""

    def __init__(self,
                 entity_id: str = None,
                 created_at: datetime.datetime = None,
                 updated_at: datetime.datetime = None,
                 language: Language = None,
                 text: str = None,
                 original: str = None):
        super().__init__(entity_id=entity_id,
                         created_at=created_at,
                         updated_at=updated_at)

        self.language = language if language is not None else Language()
        self.text = text if text is not None else ""
        self.original = original if original is not None else ""