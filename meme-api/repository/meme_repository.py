from sqlalchemy import select
from sqlalchemy import insert
from sqlalchemy import delete
from sqlalchemy import update

from db.db import DatabaseManager
from db.models import MemeOrm

from schema.meme_schema import MemeDb
from schema.meme_schema import MemeDbAdd
from schema.meme_schema import MemeDbModify


class MemeRepo:
    def __init__(self, session_manager: "DatabaseManager"):
        self.session_manager = session_manager
        self.create_table()

    def create_table(self):
        MemeOrm.metadata.create_all(bind=self.session_manager.engine)

    def clear_table(self):
        with self.session_manager.session() as session:
            session.query(MemeOrm).delete()
            session.commit()

    def get_all_memes(self) -> list[MemeDb]:
        with self.session_manager.session() as session:
            query = select(MemeOrm).select_from(MemeOrm)
            cursor = session.execute(query)
            memes_orm = cursor.scalars().all()
            meme_db = [
                MemeDb.model_validate(m, from_attributes=True)
                for m in memes_orm
            ]
            return meme_db

    def get_meme_by_id(self, meme_id: int):
        with self.session_manager.session() as session:
            query = (
                select(MemeOrm)
                .select_from(MemeOrm)
                .where(MemeOrm.id == meme_id)
            )
            cursor = session.execute(query)
            meme_orm = cursor.scalar_one_or_none()
            if meme_orm is None:
                return None
            meme_db = MemeDb.model_validate(obj=meme_orm, from_attributes=True)
            return meme_db

    def add_meme(self, meme: MemeDbAdd) -> MemeDb | None:
        query = (
            insert(MemeOrm)
            .values(meme.model_dump(exclude_none=True))
            .returning(MemeOrm)
        )
        with self.session_manager.session() as session:
            cursor = session.execute(query)
            session.commit()
            meme_orm = cursor.scalar_one_or_none()
            if meme_orm is None:
                return None
            meme_db = MemeDb.model_validate(obj=meme_orm, from_attributes=True)
            return meme_db

    def delete_meme(self, meme_id: int) -> MemeDb | None:
        query = delete(MemeOrm).where(MemeOrm.id == meme_id).returning(MemeOrm)
        with self.session_manager.session() as session:
            cursor = session.execute(query)
            meme_orm = cursor.scalar_one_or_none()
            if meme_orm is None:
                return None

            meme_db = MemeDb.model_validate(obj=meme_orm, from_attributes=True)
            session.commit()
            return meme_db

    def modify_meme(self, meme: MemeDbModify):
        query = (
            update(MemeOrm)
            .where(MemeOrm.id == meme.id)
            .values(meme.model_dump(exclude_none=True, exclude={"id"}))
            .returning(MemeOrm)
        )
        with self.session_manager.session() as session:
            cursor = session.execute(query)
            meme_orm = cursor.scalar_one_or_none()
            if meme_orm is None:
                return None
            meme_db = MemeDb.model_validate(obj=meme_orm, from_attributes=True)
            session.commit()
            return meme_db
