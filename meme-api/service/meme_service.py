from io import BytesIO
import uuid

from minio_s3.minio_s3 import MinioS3
from repository.meme_repository import MemeRepo

from schema.meme_schema import MemeDTO
from schema.meme_schema import MemeDTOAdd
from schema.meme_schema import MemeDTOUpdate

from schema.meme_schema import MemeDbAdd
from schema.meme_schema import MemeDb


fake_meme_add = MemeDTOAdd(
    text="fake meme text",
    file_name="fake_meme.jpg",
    file_bytes="fake meme bytes".encode(),
)

fake_meme = MemeDTO(
    id=1,
    text="fake meme text",
    file_name="fake_meme.jpg",
    file_bytes="fake meme bytes".encode(),
    s3_file_name="unique-s3-file-name",
)


class MemeService:
    def __init__(self, meme_repo: "MemeRepo", minio: "MinioS3"):
        self.repo = meme_repo
        self.minio = minio

    def add_meme(self, meme: MemeDTOAdd) -> MemeDTO | None:
        s3_object = self.minio.upload_file(
            name=uuid.uuid4().hex,
            binary_io=BytesIO(meme.file_bytes),
            length=len(meme.file_bytes),
        )
        s3_object_name = s3_object.object_name

        meme_add_db = MemeDbAdd(
            text=meme.text,
            file_name=meme.file_name,
            s3_file_object=s3_object_name,
        )
        meme_db = self.repo.add_meme(meme=meme_add_db)
        if meme_db is None:
            return None
        
        meme = MemeDTO(
            id=meme_db.id,
            text=meme_db.text,
            file_name=meme_db.file_name,
            file_bytes=meme.file_bytes,
            s3_file_name=s3_object_name,
        )

        return meme

    def get_meme(self, meme_id: int) -> MemeDTO | None:
        return fake_meme

    def get_all_memes(self) -> list[MemeDTO]:
        return [fake_meme]

    def update_meme(self, meme: MemeDTOUpdate) -> MemeDTO:
        return fake_meme

    def delete_meme(self, meme_id: int) -> MemeDTO | None:
        return fake_meme
