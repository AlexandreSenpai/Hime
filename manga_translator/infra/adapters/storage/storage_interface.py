from io import BytesIO


class StorageInterface:
    def upload(self, image: BytesIO, path: str) -> str: ...