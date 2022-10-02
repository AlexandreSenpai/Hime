from typing import Protocol
from hime.application.core.entities.translation import Language, Translation


class TranslatorInterface(Protocol):
    def translate(self, text: str, language: Language) -> Translation: ...