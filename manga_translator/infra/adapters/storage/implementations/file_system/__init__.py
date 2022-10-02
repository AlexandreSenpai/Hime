from io import BytesIO
from manga_translator.infra.adapters.storage.storage_interface import StorageInterface


class FileSystem(StorageInterface):
    def upload(self, image: BytesIO, path: str) -> str:
        with open(path, 'wb') as file:
            file.write(image.getbuffer())
            file.close()
        return path