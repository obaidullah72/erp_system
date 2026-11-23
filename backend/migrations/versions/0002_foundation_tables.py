"""Foundation tables. Frozen DDL: independent of future ORM edits."""
from alembic import op

revision = '0002_foundation_tables'
down_revision = '0001_foundation'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
CREATE TABLE businesses (
	slug VARCHAR(80) NOT NULL,
	name VARCHAR(160) NOT NULL,
	active BOOLEAN NOT NULL,
	id UUID NOT NULL,
	created_at TIMESTAMP WITH TIME ZONE NOT NULL,
	CONSTRAINT pk_businesses PRIMARY KEY (id),
	CONSTRAINT uq_businesses_slug UNIQUE (slug)
)

""")
    op.execute("""
CREATE TABLE permissions (
	code VARCHAR(100) NOT NULL,
	CONSTRAINT pk_permissions PRIMARY KEY (code)
)

""")
    op.execute("""
CREATE TABLE accounts (
	business_id UUID NOT NULL,
	code VARCHAR(40) NOT NULL,
	name VARCHAR(160) NOT NULL,
	kind VARCHAR(20) NOT NULL,
	active BOOLEAN NOT NULL,
	id UUID NOT NULL,
	created_at TIMESTAMP WITH TIME ZONE NOT NULL,
	CONSTRAINT pk_accounts PRIMARY KEY (id),
	CONSTRAINT uq_accounts_business_id_code UNIQUE (business_id, code),
	CONSTRAINT uq_accounts_business_id_id UNIQUE (business_id, id),
	CONSTRAINT ck_accounts_account_kind CHECK (kind IN ('asset','liability','equity','income','expense')),
	CONSTRAINT fk_accounts_business_id_businesses FOREIGN KEY(business_id) REFERENCES businesses (id)
)

""")
    op.execute("""
CREATE TABLE business_settings (
	business_id UUID NOT NULL,
	currency VARCHAR(3) NOT NULL,
	timezone VARCHAR(64) NOT NULL,
	version INTEGER NOT NULL,
	CONSTRAINT pk_business_settings PRIMARY KEY (business_id),
	CONSTRAINT ck_business_settings_version_positive CHECK (version > 0),
	CONSTRAINT fk_business_settings_business_id_businesses FOREIGN KEY(business_id) REFERENCES businesses (id)
)

""")
    op.execute("""
CREATE TABLE document_sequences (
	business_id UUID NOT NULL,
	document_type VARCHAR(50) NOT NULL,
	year INTEGER NOT NULL,
	next_value INTEGER NOT NULL,
	CONSTRAINT pk_document_sequences PRIMARY KEY (business_id, document_type, year),
	CONSTRAINT ck_document_sequences_next_positive CHECK (next_value > 0),
	CONSTRAINT fk_document_sequences_business_id_businesses FOREIGN KEY(business_id) REFERENCES businesses (id)
)

""")
    op.execute("""
CREATE TABLE idempotency_records (
	business_id UUID NOT NULL,
	operation VARCHAR(100) NOT NULL,
	key VARCHAR(128) NOT NULL,
	request_hash VARCHAR(64) NOT NULL,
	result_id UUID NOT NULL,
	id UUID NOT NULL,
	created_at TIMESTAMP WITH TIME ZONE NOT NULL,
	CONSTRAINT pk_idempotency_records PRIMARY KEY (id),
	CONSTRAINT uq_idempotency_records_business_id_operation_key UNIQUE (business_id, operation, key),
	CONSTRAINT fk_idempotency_records_business_id_businesses FOREIGN KEY(business_id) REFERENCES businesses (id)
)

""")
    op.execute("""
CREATE TABLE roles (
	business_id UUID NOT NULL,
	name VARCHAR(80) NOT NULL,
	system BOOLEAN NOT NULL,
	version INTEGER NOT NULL,
	id UUID NOT NULL,
	created_at TIMESTAMP WITH TIME ZONE NOT NULL,
	CONSTRAINT pk_roles PRIMARY KEY (id),
	CONSTRAINT uq_roles_business_id_name UNIQUE (business_id, name),
	CONSTRAINT uq_roles_business_id_id UNIQUE (business_id, id),
	CONSTRAINT fk_roles_business_id_businesses FOREIGN KEY(business_id) REFERENCES businesses (id)
)

""")
    op.execute("""CREATE INDEX ix_roles_business_id ON roles (business_id)""")
    op.execute("""
CREATE TABLE users (
	business_id UUID NOT NULL,
	email VARCHAR(254) NOT NULL,
	name VARCHAR(160) NOT NULL,
	password_hash VARCHAR(512) NOT NULL,
	active BOOLEAN NOT NULL,
	version INTEGER NOT NULL,
	id UUID NOT NULL,
	created_at TIMESTAMP WITH TIME ZONE NOT NULL,
	CONSTRAINT pk_users PRIMARY KEY (id),
	CONSTRAINT uq_users_business_id_email UNIQUE (business_id, email),
	CONSTRAINT uq_users_business_id_id UNIQUE (business_id, id),
	CONSTRAINT ck_users_email_normalized CHECK (email = lower(email)),
	CONSTRAINT ck_users_version_positive CHECK (version > 0),
	CONSTRAINT fk_users_business_id_businesses FOREIGN KEY(business_id) REFERENCES businesses (id)
)

""")
    op.execute("""CREATE INDEX ix_users_business_id ON users (business_id)""")
    op.execute("""
CREATE TABLE audit_logs (
	business_id UUID NOT NULL,
	actor_id UUID,
	action VARCHAR(100) NOT NULL,
	resource_id VARCHAR(100) NOT NULL,
	request_id VARCHAR(36),
	id UUID NOT NULL,
	created_at TIMESTAMP WITH TIME ZONE NOT NULL,
	CONSTRAINT pk_audit_logs PRIMARY KEY (id),
	CONSTRAINT fk_audit_logs_business_id_users FOREIGN KEY(business_id, actor_id) REFERENCES users (business_id, id),
	CONSTRAINT fk_audit_logs_business_id_businesses FOREIGN KEY(business_id) REFERENCES businesses (id)
)

""")
    op.execute("""CREATE INDEX ix_audit_business_created ON audit_logs (business_id, created_at)""")
    op.execute("""
CREATE TABLE auth_sessions (
	business_id UUID NOT NULL,
	user_id UUID NOT NULL,
	refresh_hash VARCHAR(64) NOT NULL,
	expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
	revoked_at TIMESTAMP WITH TIME ZONE,
	id UUID NOT NULL,
	created_at TIMESTAMP WITH TIME ZONE NOT NULL,
	CONSTRAINT pk_auth_sessions PRIMARY KEY (id),
	CONSTRAINT fk_auth_sessions_business_id_users FOREIGN KEY(business_id, user_id) REFERENCES users (business_id, id),
	CONSTRAINT uq_auth_sessions_refresh_hash UNIQUE (refresh_hash)
)

""")
    op.execute("""CREATE INDEX ix_auth_sessions_expires_at ON auth_sessions (expires_at)""")
    op.execute("""CREATE INDEX ix_auth_sessions_user_id ON auth_sessions (user_id)""")
    op.execute("""
CREATE TABLE journal_entries (
	transaction_id BIGINT DEFAULT txid_current() NOT NULL,
	business_id UUID NOT NULL,
	source_type VARCHAR(60) NOT NULL,
	source_id VARCHAR(100) NOT NULL,
	event VARCHAR(60) NOT NULL,
	accounting_date DATE NOT NULL,
	currency VARCHAR(3) NOT NULL,
	actor_id UUID NOT NULL,
	id UUID NOT NULL,
	created_at TIMESTAMP WITH TIME ZONE NOT NULL,
	CONSTRAINT pk_journal_entries PRIMARY KEY (id),
	CONSTRAINT uq_journal_entries_business_id_source_type_source_id_event UNIQUE (business_id, source_type, source_id, event),
	CONSTRAINT uq_journal_entries_business_id_id UNIQUE (business_id, id),
	CONSTRAINT fk_journal_entries_business_id_users FOREIGN KEY(business_id, actor_id) REFERENCES users (business_id, id),
	CONSTRAINT fk_journal_entries_business_id_businesses FOREIGN KEY(business_id) REFERENCES businesses (id)
)

""")
    op.execute("""CREATE INDEX ix_journal_business_date ON journal_entries (business_id, accounting_date)""")
    op.execute("""
CREATE TABLE role_permissions (
	role_id UUID NOT NULL,
	permission_code VARCHAR(100) NOT NULL,
	CONSTRAINT pk_role_permissions PRIMARY KEY (role_id, permission_code),
	CONSTRAINT fk_role_permissions_role_id_roles FOREIGN KEY(role_id) REFERENCES roles (id),
	CONSTRAINT fk_role_permissions_permission_code_permissions FOREIGN KEY(permission_code) REFERENCES permissions (code)
)

""")
    op.execute("""
CREATE TABLE user_roles (
	business_id UUID NOT NULL,
	user_id UUID NOT NULL,
	role_id UUID NOT NULL,
	CONSTRAINT pk_user_roles PRIMARY KEY (business_id, user_id, role_id),
	CONSTRAINT fk_user_roles_business_id_users FOREIGN KEY(business_id, user_id) REFERENCES users (business_id, id),
	CONSTRAINT fk_user_roles_business_id_roles FOREIGN KEY(business_id, role_id) REFERENCES roles (business_id, id)
)

""")
    op.execute("""CREATE INDEX ix_user_roles_role ON user_roles (business_id, role_id)""")
    op.execute("""
CREATE TABLE journal_entry_lines (
	business_id UUID NOT NULL,
	entry_id UUID NOT NULL,
	account_id UUID NOT NULL,
	debit NUMERIC(20, 6) NOT NULL,
	credit NUMERIC(20, 6) NOT NULL,
	id UUID NOT NULL,
	created_at TIMESTAMP WITH TIME ZONE NOT NULL,
	CONSTRAINT pk_journal_entry_lines PRIMARY KEY (id),
	CONSTRAINT fk_journal_entry_lines_business_id_journal_entries FOREIGN KEY(business_id, entry_id) REFERENCES journal_entries (business_id, id),
	CONSTRAINT fk_journal_entry_lines_business_id_accounts FOREIGN KEY(business_id, account_id) REFERENCES accounts (business_id, id),
	CONSTRAINT ck_journal_entry_lines_one_positive_side CHECK ((debit > 0 AND credit = 0) OR (credit > 0 AND debit = 0)),
	CONSTRAINT ck_journal_entry_lines_finite_amount CHECK (debit < 100000000000000 AND credit < 100000000000000)
)

""")
    op.execute("""CREATE INDEX ix_journal_entry_lines_account_id ON journal_entry_lines (account_id)""")
    op.execute("""CREATE INDEX ix_journal_entry_lines_entry_id ON journal_entry_lines (entry_id)""")
    install_guards()


def downgrade():
    op.drop_table('journal_entry_lines')
    op.drop_table('user_roles')
    op.drop_table('role_permissions')
    op.drop_table('journal_entries')
    op.drop_table('auth_sessions')
    op.drop_table('audit_logs')
    op.drop_table('users')
    op.drop_table('roles')
    op.drop_table('idempotency_records')
    op.drop_table('document_sequences')
    op.drop_table('business_settings')
    op.drop_table('accounts')
    op.drop_table('permissions')
    op.drop_table('businesses')
    op.execute("DROP FUNCTION IF EXISTS erp_check_journal() CASCADE")
    op.execute("DROP FUNCTION IF EXISTS erp_immutable() CASCADE")
    op.execute("DROP FUNCTION IF EXISTS erp_line_insert() CASCADE")


def install_guards():
    op.execute('''CREATE FUNCTION erp_immutable() RETURNS trigger LANGUAGE plpgsql AS $$
        BEGIN RAISE EXCEPTION 'Posted and audit records are immutable' USING ERRCODE = '23514'; END $$''')
    for table in ('journal_entries', 'journal_entry_lines', 'audit_logs'):
        op.execute(f'CREATE TRIGGER immutable_record BEFORE UPDATE OR DELETE ON {table} FOR EACH ROW EXECUTE FUNCTION erp_immutable()')
    op.execute('''CREATE FUNCTION erp_line_insert() RETURNS trigger LANGUAGE plpgsql AS $$
        BEGIN
          IF NOT EXISTS (SELECT 1 FROM journal_entries WHERE id = NEW.entry_id
                         AND transaction_id = txid_current()) THEN
            RAISE EXCEPTION 'Lines must be created with their entry' USING ERRCODE = '23514';
          END IF;
          RETURN NEW;
        END $$''')
    op.execute('CREATE TRIGGER lines_in_entry_transaction BEFORE INSERT ON journal_entry_lines FOR EACH ROW EXECUTE FUNCTION erp_line_insert()')
    op.execute('''CREATE FUNCTION erp_check_journal() RETURNS trigger LANGUAGE plpgsql AS $$
        DECLARE target uuid; n bigint; d numeric; c numeric;
        BEGIN
          IF TG_TABLE_NAME = 'journal_entries' THEN target := NEW.id; ELSE target := NEW.entry_id; END IF;
          SELECT count(*), coalesce(sum(debit),0), coalesce(sum(credit),0) INTO n,d,c
            FROM journal_entry_lines WHERE entry_id = target;
          IF n < 2 OR d <> c THEN
            RAISE EXCEPTION 'Journal must contain balanced lines' USING ERRCODE = '23514';
          END IF;
          RETURN NULL;
        END $$''')
    for table in ('journal_entries', 'journal_entry_lines'):
        op.execute(f'CREATE CONSTRAINT TRIGGER balanced_journal AFTER INSERT ON {table} DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION erp_check_journal()')
