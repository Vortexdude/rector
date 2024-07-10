import bcrypt
from app.api.models import User, Role, Group, Permission
from .schema import UserRegisterSchema, RoleCreate, GroupCreate, PermissionCreate
from app.core.db import ModelMixing


class UserResource(ModelMixing):

    def insert(self, user: UserRegisterSchema) -> User | dict:
        if self.find_by_email(user.email):
            return {"message": "Username already registered"}

        password_hash = get_password_hash(user.password)
        user = User(
            username=user.username,
            password_hash=password_hash,
            email=user.email,
        )
        self.add_to_db(user)
        return user

    def find_by_email(self, email: str) -> User | dict:
        user = self.db.query(User).filter_by(email=email).first()
        return user if user else {}

    def find_by_username(self, user_name: str) -> User | dict:
        user = self.db.query(User).filter_by(username=user_name).first()
        return user if user else {}


class RoleResource(ModelMixing):

    def insert(self, role_data: RoleCreate) -> Role | dict:
        if self.find_by_name(Role, role_data.name):
            return {"message": "Role already exist"}
        role = Role(**role_data.model_dump())
        self.add_to_db(role)
        return role


class GroupResource(ModelMixing):

    def insert(self, group_data: GroupCreate) -> Role | dict:
        if self.find_by_name(Group, group_data.name):
            return {"message": "Group already exist"}
        group = Group(**group_data.model_dump())
        self.add_to_db(group)
        return group


class PermissionResource(ModelMixing):

    def insert(self, perm_data: PermissionCreate) -> Role | dict:
        if self.find_by_name(Permission, perm_data.name):
            return {"message": "Permission already exist"}

        permission = Permission(**perm_data.model_dump())
        self.add_to_db(permission)
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
