from sqlalchemy import Column, Integer, String, ForeignKey, Table, TIMESTAMP
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.sql import func
from app.core.db import Base
from uuid import uuid4


class SurrogatePK(Base):
    __abstract__ = True

    id: Mapped[str] = mapped_column(String, default=lambda: str(uuid4()), primary_key=True, nullable=False)


user_roles = Table(
    'user_roles', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('role_id', Integer, ForeignKey('roles.id'))
)

role_permissions = Table(
    'role_permissions', Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.id')),
    Column('permission_id', Integer, ForeignKey('permissions.id'))
)

user_permissions = Table(
    'user_permissions', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('permission_id', Integer, ForeignKey('permissions.id'))
)

user_groups = Table(
    'user_groups', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('group_id', Integer, ForeignKey('groups.id'))
)


class User(SurrogatePK):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    roles = relationship('Role', secondary=user_roles, back_populates='users')
    permissions = relationship('Permission', secondary=user_permissions, back_populates='users')
    groups = relationship('Group', secondary=user_groups, back_populates='users')

    def __str__(self):
        return f"<User email {self.email}>"


class Role(SurrogatePK):
    __tablename__ = 'roles'

    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    users = relationship('User', secondary=user_roles, back_populates="roles")
    permissions = relationship('Permission', secondary=role_permissions, back_populates="roles")


class Permission(SurrogatePK):
    __tablename__ = 'permissions'

    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    details: Mapped[str] = mapped_column(String(255), nullable=False)
    roles = relationship('Role', secondary=role_permissions, back_populates='permissions')
    users = relationship('User', secondary=user_permissions, back_populates='permissions')


class Group(SurrogatePK):
    __tablename__ = 'groups'

    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    users = relationship('User', secondary=user_groups, back_populates='groups')


class AuditLog(SurrogatePK):
    __tablename__ = 'audit_logs'

    user_id = mapped_column(ForeignKey('users.id'))
    change_type: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    change_details = mapped_column(String(50))
    changed_at = mapped_column(TIMESTAMP, server_default=func.now())
    user = relationship('User')
