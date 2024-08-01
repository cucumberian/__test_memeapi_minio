from pydantic import BaseModel


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
