"""Run from backend: python -m scripts.bootstrap_admin --business demo --name 'Demo business' --email admin@example.com"""
import argparse
import getpass
from sqlalchemy import select, text
from app.core.security import hash_password, signing_key
from app.db.session import SessionLocal
from app.db.model_registry import Business, BusinessSettings, User, UserRole
from app.db.seed import seed_roles
from app.modules.audit_logs.service import audit
from app.modules.users.schemas import UserCreate


def bootstrap(db, business, name, email, password):
    import re
    if not re.fullmatch(r'[a-z0-9-]{1,80}', business) or not 1 <= len(name) <= 160:
        raise ValueError('Invalid business slug or name')
    validated = UserCreate(email=email, name='First administrator', password=password, role_ids=[])
    # Serializes first-admin creation even when two CLI processes race.
    db.execute(text('SELECT pg_advisory_xact_lock(47001001)'))
    if db.scalar(select(User.id).limit(1)) or db.scalar(select(Business.id).limit(1)):
        raise ValueError('Bootstrap refused: installation already initialized')
    company = Business(slug=business, name=name)
    db.add(company)
    db.flush()
    db.add(BusinessSettings(business_id=company.id))
    roles = seed_roles(db, company.id)
    user = User(business_id=company.id, email=validated.email, name=validated.name,
                password_hash=hash_password(password))
    db.add(user)
    db.flush()
    db.add(UserRole(business_id=company.id, user_id=user.id, role_id=roles['Super Admin'].id))
    audit(db, company.id, user.id, 'installation.bootstrap', company.id)
    return user


def main():
    parser = argparse.ArgumentParser(description='One-time first administrator bootstrap; no default password')
    parser.add_argument('--business', required=True)
    parser.add_argument('--name', required=True)
    parser.add_argument('--email', required=True)
    args = parser.parse_args()
    signing_key()
    password = getpass.getpass('Password (12–256 characters): ')
    if password != getpass.getpass('Confirm password: '):
        raise SystemExit('Passwords do not match')
    with SessionLocal.begin() as db:
        bootstrap(db, args.business, args.name, args.email, password)
    print('Business and first administrator created.')


if __name__ == '__main__':
    main()
