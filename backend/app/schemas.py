from app.models import Song

from uuid import UUID


class ISongList(Song):
    id: UUID
    name: str
