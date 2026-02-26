from sqlalchemy import MetaData, Integer, String, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func


class BaseModel(DeclarativeBase):
    """
    Base class for SQLAlchemy models with explicit naming convention.
    """
    metadata = MetaData(naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    })

    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), onupdate=func.now())


class LLModel(BaseModel):
    __tablename__ = "llmodels"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))
    size: Mapped[int] = mapped_column(Integer)
    format: Mapped[str] = mapped_column(String(64))
    parameters: Mapped[str] = mapped_column(String(64))
    quantization_level: Mapped[str] = mapped_column(String(64))

    def __repr__(self):
        return f'Model({self.id}, "{self.name}")'
