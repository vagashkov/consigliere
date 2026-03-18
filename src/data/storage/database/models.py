from sqlalchemy import (
    MetaData, Integer, String, Enum, DateTime, ForeignKey, CheckConstraint
)
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import (
    DeclarativeBase, Mapped, mapped_column, declared_attr
)
from sqlalchemy.sql import func

from src.constants import UserRole


class BaseModel(AsyncAttrs, DeclarativeBase):
    """
    Base class for SQLAlchemy models:
     - explicit __abstract__ flag to prevent table creation
     - supports async models via AsyncAttrs
     - uses explicit naming convention via metadata
     - contains ID, created_at and updated_at standard fields
    """

    __abstract__ = True

    metadata = MetaData(naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    })

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, index=True
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """
        Creates table name based on pluralized class name
        :return:
        """
        return f"{cls.__name__.lower()}s"


class User(BaseModel):
    """
    Model for user authentication
    """

    email: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(128))
    is_active: Mapped[bool] = mapped_column(default=True)
    role: Mapped[str] = mapped_column(
        Enum(UserRole),
        nullable=False,
        default=UserRole.USER
    )


class UserProfile(BaseModel):
    """
    Model for user profile data
    """

    user: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    first_name: Mapped[str] = mapped_column(String(64))
    last_name: Mapped[str] = mapped_column(String(64))


class LLMProvider(BaseModel):
    """
    Model for LLM provider settings
    """
    name: Mapped[str] = mapped_column(String(64))
    url: Mapped[str] = mapped_column(String(256))
    port: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint(
            "port > 0",
            name="min_port_check")
    )
    description: Mapped[str | None] = mapped_column(String(256), nullable=True)

    def __repr__(self):
        return f"{self.name} ({self.url}:{self.port})"


class LLModel(BaseModel):
    """
    Model for LLM model settings
    """

    name: Mapped[str] = mapped_column(String(64))
    size: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint(
            "size > 0",
            name="min_llm_size_check")
    )
    format: Mapped[str] = mapped_column(String(64))
    parameters: Mapped[str] = mapped_column(String(64))
    quantization_level: Mapped[str] = mapped_column(String(64))

    def __repr__(self):
        return f"{self.name} model"
