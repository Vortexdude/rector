from app.api.models import User, Role, Group, Permission
from .schema import UserRegisterSchema, RoleCreate, GroupCreate, PermissionCreate
from sqlalchemy.orm import Session
import bcrypt


class UserResource(object):
    def __init__(self, session: Session):
        self.db = session

    def insert(self, user: UserRegisterSchema) -> User | None:
        if self.find_by_email(user.email):
            return
        password_hash = get_password_hash(user.password)
        user = User(
            username=user.username,
            password_hash=password_hash,
            email=user.email,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def find_by_email(self, email: str) -> User:
        user = self.db.query(User).filter_by(email=email).first()
        return user if user else {}

    def find_by_id(self, user_id: str) -> User:
        user = self.db.query(User).filter_by(id=user_id).first()
        return user if user else {}


class RoleResource(object):

    def __init__(self, session: Session):
        self.db = session

    def insert(self, role_data: RoleCreate) -> Role | None:
        role = Role(**role_data.model_dump())
        self.db.add(role)
        self.db.commit()
        self.db.refresh(role)
        return role


class GroupResource(object):

    def __init__(self, session: Session):
        self.db = session

    def insert(self, group_data: GroupCreate) -> Role | None:
        group = Group(**group_data.model_dump())
        self.db.add(group)
        self.db.commit()
        self.db.refresh(group)
        return group


class PermissionResource(object):

    def __init__(self, session: Session):
        self.db = session

    def insert(self, perm_data: PermissionCreate) -> Role | None:
        permission = Permission(**perm_data.model_dump())
        self.db.add(permission)
        self.db.commit()
        self.db.refresh(permission)
        return permission


def get_password_hash(password: str):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def create_admin_user(data, db):
    group_data = {"name": "admin-gp"}
    permission_data = {"name": "admin-perm", "details": "all"}
    role_data = {"name": "admin"}
    password_hash = get_password_hash(data.password)
    user = User(
        username=data.username,
        password_hash=password_hash,
        email=data.email,
        groups=[Group(**group_data)],
        roles=[Role(**role_data)],
        permissions=[Permission(**permission_data)]
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
