from pydantic import BaseModel


class MemeMinio(BaseModel):
    file_bytes: bytes
    s3_file_object: str


class MemeDbAdd(BaseModel):
    text: str
    file_name: str
    s3_file_object: str


class MemeDb(MemeDbAdd):
    id: int


class MemeDbModify(BaseModel):
    id: int
    text: str | None = None
    file_name: str | None = None
    s3_file_object: str | None = None


class MemeDTOAdd(BaseModel):
    text: str
    file_name: str
    file_bytes: bytes


class MemeDTO(MemeDTOAdd):
    id: int
    s3_file_name: str


class MemeDTOUpdate(BaseModel):
    id: int
    text: str | None = None
    file_name: str | None = None
    s3_file_object: str | None = None
    file_bytes: bytes | None = None
