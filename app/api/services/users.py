from sqlalchemy.orm import Session
from app.api.models.users import User
from app.common.security.jwt import get_password_hash, verify_password
from app.common.security.jwt import create_access_token


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def register_user(self, data):
        user = User(
            name=data.name,
            email=data.email,
            hashed_password=get_password_hash(data.password)
        )
        try:
            self.db.add(user)
            self.db.commit()
            self.db.flush(user)
            return {"status": "done"}
        except Exception as e:
            print(e)
            return {"error": "Exception with the database later will change"}

    def _get_user(self, data):
        args = {}
        if data.email:
            args['email'] = data.email

        user = self.db.query(User).filter_by(**args).first()
        if not user:
            return {}
        return user

    def login(self, data):
        user = self._get_user(data)

        if not user:
            return {"message": "User not found"}
        if not verify_password(data.password, user.hashed_password):
            return {"message": "email or password not matched."}
        if not isinstance(user, User):
            return {"Message": "Error with the database"}

        token, expire = create_access_token(sub=user.email)
        return {
            "access_token": token,
            "time": str(expire)
        }

