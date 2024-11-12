import time

from sqlalchemy import delete, select

from models import Token, sqlite_session


class TokenRepository:
    model = Token

    def get_token(self) -> str:
        """Получить токен из БД"""
        with sqlite_session() as session:
            return session.scalar(select(self.model).limit(1))

    def update_token(self, access_token):
        """Обновляет токен"""
        with sqlite_session() as session:
            session.execute(delete(self.model))
            token = self.model(access_token=access_token, created_at=int(time.time()))
            session.add(token)
            session.commit()
