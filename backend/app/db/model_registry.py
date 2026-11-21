"""Concrete Stage 1 persistence models. Later modules register their own models."""
from datetime import date, datetime, timezone
from decimal import Decimal
from uuid import UUID, uuid4
from sqlalchemy import (BigInteger, text, Boolean, CheckConstraint, Date, DateTime, ForeignKey, ForeignKeyConstraint,
                        Index, Integer, JSON, Numeric, String, UniqueConstraint)
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


def now():
    return datetime.now(timezone.utc)


class Entity:
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class Business(Entity, Base):
    __tablename__ = 'businesses'
    slug: Mapped[str] = mapped_column(String(80), unique=True)
    name: Mapped[str] = mapped_column(String(160))
    active: Mapped[bool] = mapped_column(Boolean, default=True)


class BusinessSettings(Base):
    __tablename__ = 'business_settings'
    business_id: Mapped[UUID] = mapped_column(ForeignKey('businesses.id'), primary_key=True)
    currency: Mapped[str] = mapped_column(String(3), default='PKR')
    timezone: Mapped[str] = mapped_column(String(64), default='Asia/Karachi')
    version: Mapped[int] = mapped_column(Integer, default=1)
    __table_args__ = (CheckConstraint('version > 0', name='version_positive'),)


class User(Entity, Base):
    __tablename__ = 'users'
    business_id: Mapped[UUID] = mapped_column(ForeignKey('businesses.id'), index=True)
    email: Mapped[str] = mapped_column(String(254))
    name: Mapped[str] = mapped_column(String(160))
    password_hash: Mapped[str] = mapped_column(String(512))
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    version: Mapped[int] = mapped_column(Integer, default=1)
    __table_args__ = (UniqueConstraint('business_id', 'email'), UniqueConstraint('business_id', 'id'),
                      CheckConstraint('email = lower(email)', name='email_normalized'),
                      CheckConstraint('version > 0', name='version_positive'))


class Role(Entity, Base):
    __tablename__ = 'roles'
    business_id: Mapped[UUID] = mapped_column(ForeignKey('businesses.id'), index=True)
    name: Mapped[str] = mapped_column(String(80))
    system: Mapped[bool] = mapped_column(Boolean, default=False)
    version: Mapped[int] = mapped_column(Integer, default=1)
    __table_args__ = (UniqueConstraint('business_id', 'name'), UniqueConstraint('business_id', 'id'),)


class Permission(Base):
    __tablename__ = 'permissions'
    code: Mapped[str] = mapped_column(String(100), primary_key=True)


class UserRole(Base):
    __tablename__ = 'user_roles'
    business_id: Mapped[UUID] = mapped_column(primary_key=True)
    user_id: Mapped[UUID] = mapped_column(primary_key=True)
    role_id: Mapped[UUID] = mapped_column(primary_key=True)
    __table_args__ = (
        ForeignKeyConstraint(['business_id', 'user_id'], ['users.business_id', 'users.id']),
        ForeignKeyConstraint(['business_id', 'role_id'], ['roles.business_id', 'roles.id']),
        Index('ix_user_roles_role', 'business_id', 'role_id'))


class RolePermission(Base):
    __tablename__ = 'role_permissions'
    role_id: Mapped[UUID] = mapped_column(ForeignKey('roles.id'), primary_key=True)
    permission_code: Mapped[str] = mapped_column(ForeignKey('permissions.code'), primary_key=True)


class AuthSession(Entity, Base):
    __tablename__ = 'auth_sessions'
    business_id: Mapped[UUID] = mapped_column()
    user_id: Mapped[UUID] = mapped_column(index=True)
    refresh_hash: Mapped[str] = mapped_column(String(64), unique=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    __table_args__ = (ForeignKeyConstraint(['business_id', 'user_id'], ['users.business_id', 'users.id']),)


class AuditLog(Entity, Base):
    __tablename__ = 'audit_logs'
    business_id: Mapped[UUID] = mapped_column(ForeignKey('businesses.id'))
    actor_id: Mapped[UUID | None] = mapped_column()
    action: Mapped[str] = mapped_column(String(100))
    resource_id: Mapped[str] = mapped_column(String(100))
    request_id: Mapped[str | None] = mapped_column(String(36))
    __table_args__ = (ForeignKeyConstraint(['business_id', 'actor_id'], ['users.business_id', 'users.id']),
                      Index('ix_audit_business_created', 'business_id', 'created_at'))


class DocumentSequence(Base):
    __tablename__ = 'document_sequences'
    business_id: Mapped[UUID] = mapped_column(ForeignKey('businesses.id'), primary_key=True)
    document_type: Mapped[str] = mapped_column(String(50), primary_key=True)
    year: Mapped[int] = mapped_column(Integer, primary_key=True)
    next_value: Mapped[int] = mapped_column(Integer, default=1)
    __table_args__ = (CheckConstraint('next_value > 0', name='next_positive'),)


class IdempotencyRecord(Entity, Base):
    __tablename__ = 'idempotency_records'
    business_id: Mapped[UUID] = mapped_column(ForeignKey('businesses.id'))
    operation: Mapped[str] = mapped_column(String(100))
    key: Mapped[str] = mapped_column(String(128))
    request_hash: Mapped[str] = mapped_column(String(64))
    result_id: Mapped[UUID] = mapped_column()
    __table_args__ = (UniqueConstraint('business_id', 'operation', 'key'),)


class Account(Entity, Base):
    __tablename__ = 'accounts'
    business_id: Mapped[UUID] = mapped_column(ForeignKey('businesses.id'))
    code: Mapped[str] = mapped_column(String(40))
    name: Mapped[str] = mapped_column(String(160))
    kind: Mapped[str] = mapped_column(String(20))
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    __table_args__ = (UniqueConstraint('business_id', 'code'), UniqueConstraint('business_id', 'id'),
                      CheckConstraint("kind IN ('asset','liability','equity','income','expense')", name='account_kind'))


class JournalEntry(Entity, Base):
    __tablename__ = 'journal_entries'
    transaction_id: Mapped[int] = mapped_column(BigInteger, server_default=text('txid_current()'))
    business_id: Mapped[UUID] = mapped_column(ForeignKey('businesses.id'))
    source_type: Mapped[str] = mapped_column(String(60))
    source_id: Mapped[str] = mapped_column(String(100))
    event: Mapped[str] = mapped_column(String(60))
    accounting_date: Mapped[date] = mapped_column(Date)
    currency: Mapped[str] = mapped_column(String(3))
    actor_id: Mapped[UUID] = mapped_column()
    __table_args__ = (UniqueConstraint('business_id', 'source_type', 'source_id', 'event'),
                      UniqueConstraint('business_id', 'id'),
                      ForeignKeyConstraint(['business_id', 'actor_id'], ['users.business_id', 'users.id']),
                      Index('ix_journal_business_date', 'business_id', 'accounting_date'))


class JournalEntryLine(Entity, Base):
    __tablename__ = 'journal_entry_lines'
    business_id: Mapped[UUID] = mapped_column()
    entry_id: Mapped[UUID] = mapped_column(index=True)
    account_id: Mapped[UUID] = mapped_column(index=True)
    debit: Mapped[Decimal] = mapped_column(Numeric(20, 6))
    credit: Mapped[Decimal] = mapped_column(Numeric(20, 6))
    __table_args__ = (
        ForeignKeyConstraint(['business_id', 'entry_id'], ['journal_entries.business_id', 'journal_entries.id']),
        ForeignKeyConstraint(['business_id', 'account_id'], ['accounts.business_id', 'accounts.id']),
        CheckConstraint('(debit > 0 AND credit = 0) OR (credit > 0 AND debit = 0)', name='one_positive_side'),
        CheckConstraint("debit < 100000000000000 AND credit < 100000000000000", name='finite_amount'))
