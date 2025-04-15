from sqlalchemy.orm import Session


class BaseRepository:
    def __init__(self, db: Session):
        self._db: Session = db

    @property
    def db(self):
        return self._db
