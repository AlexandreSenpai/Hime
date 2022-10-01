from dataclasses import asdict, dataclass, field
import datetime

from hime.application.core.entities.entity import Entity

@dataclass
class Dimensions:
    width: int = field(default=0)
    height: int = field(default=0)

@dataclass
class ImageProps:
    dimensions: Dimensions = field(default_factory=Dimensions)
    
    def as_dict(self):
        return asdict(self)

@dataclass
class Image(Entity):
    def __init__(self,
                 entity_id: str = None,
                 created_at: datetime.datetime = None,
                 updated_at: datetime.datetime = None,
                 props: ImageProps = ImageProps()):
        super().__init__(entity_id=entity_id,
                         created_at=created_at,
                         updated_at=updated_at,
                         props=props)
    
    def hello_world(self) -> str:
        return 'Hello World.'