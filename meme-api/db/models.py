from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped

from db.db import Base


class MemeOrm(Base):
    __tablename__ = "memes"
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    file_name: Mapped[str]
    s3_file_object: Mapped[str]
