"""Foundation tables. Frozen DDL: independent of future ORM edits."""
from alembic import op

revision = '0002_foundation_tables'
down_revision = '0001_foundation'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('\nCREATE TABLE businesses (\n\tslug VARCHAR(80) NOT NULL, \n\tname VARCHAR(160) NOT NULL, \n\tactive BOOLEAN NOT NULL, \n\tid UUID NOT NULL, \n\tcreated_at TIMESTAMP WITH TIME ZONE NOT NULL, \n\tCONSTRAINT pk_businesses PRIMARY KEY (id), \n\tCONSTRAINT uq_businesses_slug UNIQUE (slug)\n)\n\n')
    op.execute('\nCREATE TABLE permissions (\n\tcode VARCHAR(100) NOT NULL, \n\tCONSTRAINT pk_permissions PRIMARY KEY (code)\n)\n\n')
    op.execute("\nCREATE TABLE accounts (\n\tbusiness_id UUID NOT NULL, \n\tcode VARCHAR(40) NOT NULL, \n\tname VARCHAR(160) NOT NULL, \n\tkind VARCHAR(20) NOT NULL, \n\tactive BOOLEAN NOT NULL, \n\tid UUID NOT NULL, \n\tcreated_at TIMESTAMP WITH TIME ZONE NOT NULL, \n\tCONSTRAINT pk_accounts PRIMARY KEY (id), \n\tCONSTRAINT uq_accounts_business_id_code UNIQUE (business_id, code), \n\tCONSTRAINT uq_accounts_business_id_id UNIQUE (business_id, id), \n\tCONSTRAINT ck_accounts_account_kind CHECK (kind IN ('asset','liability','equity','income','expense')), \n\tCONSTRAINT fk_accounts_business_id_businesses FOREIGN KEY(business_id) REFERENCES businesses (id)\n)\n\n")
    op.execute('\nCREATE TABLE business_settings (\n\tbusiness_id UUID NOT NULL, \n\tcurrency VARCHAR(3) NOT NULL, \n\ttimezone VARCHAR(64) NOT NULL, \n\tversion INTEGER NOT NULL, \n\tCONSTRAINT pk_business_settings PRIMARY KEY (business_id), \n\tCONSTRAINT ck_business_settings_version_positive CHECK (version > 0), \n\tCONSTRAINT fk_business_settings_business_id_businesses FOREIGN KEY(business_id) REFERENCES businesses (id)\n)\n\n')
    op.execute('\nCREATE TABLE document_sequences (\n\tbusiness_id UUID NOT NULL, \n\tdocument_type VARCHAR(50) NOT NULL, \n\tyear INTEGER NOT NULL, \n\tnext_value INTEGER NOT NULL, \n\tCONSTRAINT pk_document_sequences PRIMARY KEY (business_id, document_type, year), \n\tCONSTRAINT ck_document_sequences_next_positive CHECK (next_value > 0), \n\tCONSTRAINT fk_document_sequences_business_id_businesses FOREIGN KEY(business_id) REFERENCES businesses (id)\n)\n\n')
    op.execute('\nCREATE TABLE idempotency_records (\n\tbusiness_id UUID NOT NULL, \n\toperation VARCHAR(100) NOT NULL, \n\tkey VARCHAR(128) NOT NULL, \n\trequest_hash VARCHAR(64) NOT NULL, \n\tresult_id UUID NOT NULL, \n\tid UUID NOT NULL, \n\tcreated_at TIMESTAMP WITH TIME ZONE NOT NULL, \n\tCONSTRAINT pk_idempotency_records PRIMARY KEY (id), \n\tCONSTRAINT uq_idempotency_records_business_id_operation_key UNIQUE (business_id, operation, key), \n\tCONSTRAINT fk_idempotency_records_business_id_businesses FOREIGN KEY(business_id) REFERENCES businesses (id)\n)\n\n')
    op.execute('\nCREATE TABLE roles (\n\tbusiness_id UUID NOT NULL, \n\tname VARCHAR(80) NOT NULL, \n\tsystem BOOLEAN NOT NULL, \n\tversion INTEGER NOT NULL, \n\tid UUID NOT NULL, \n\tcreated_at TIMESTAMP WITH TIME ZONE NOT NULL, \n\tCONSTRAINT pk_roles PRIMARY KEY (id), \n\tCONSTRAINT uq_roles_business_id_name UNIQUE (business_id, name), \n\tCONSTRAINT uq_roles_business_id_id UNIQUE (business_id, id), \n\tCONSTRAINT fk_roles_business_id_businesses FOREIGN KEY(business_id) REFERENCES businesses (id)\n)\n\n')
    op.execute('CREATE INDEX ix_roles_business_id ON roles (business_id)')
    op.execute('\nCREATE TABLE users (\n\tbusiness_id UUID NOT NULL, \n\temail VARCHAR(254) NOT NULL, \n\tname VARCHAR(160) NOT NULL, \n\tpassword_hash VARCHAR(512) NOT NULL, \n\tactive BOOLEAN NOT NULL, \n\tversion INTEGER NOT NULL, \n\tid UUID NOT NULL, \n\tcreated_at TIMESTAMP WITH TIME ZONE NOT NULL, \n\tCONSTRAINT pk_users PRIMARY KEY (id), \n\tCONSTRAINT uq_users_business_id_email UNIQUE (business_id, email), \n\tCONSTRAINT uq_users_business_id_id UNIQUE (business_id, id), \n\tCONSTRAINT ck_users_email_normalized CHECK (email = lower(email)), \n\tCONSTRAINT ck_users_version_positive CHECK (version > 0), \n\tCONSTRAINT fk_users_business_id_businesses FOREIGN KEY(business_id) REFERENCES businesses (id)\n)\n\n')
    op.execute('CREATE INDEX ix_users_business_id ON users (business_id)')
    op.execute('\nCREATE TABLE audit_logs (\n\tbusiness_id UUID NOT NULL, \n\tactor_id UUID, \n\taction VARCHAR(100) NOT NULL, \n\tresource_id VARCHAR(100) NOT NULL, \n\trequest_id VARCHAR(36), \n\tid UUID NOT NULL, \n\tcreated_at TIMESTAMP WITH TIME ZONE NOT NULL, \n\tCONSTRAINT pk_audit_logs PRIMARY KEY (id), \n\tCONSTRAINT fk_audit_logs_business_id_users FOREIGN KEY(business_id, actor_id) REFERENCES users (business_id, id), \n\tCONSTRAINT fk_audit_logs_business_id_businesses FOREIGN KEY(business_id) REFERENCES businesses (id)\n)\n\n')
    op.execute('CREATE INDEX ix_audit_business_created ON audit_logs (business_id, created_at)')
    op.execute('\nCREATE TABLE auth_sessions (\n\tbusiness_id UUID NOT NULL, \n\tuser_id UUID NOT NULL, \n\trefresh_hash VARCHAR(64) NOT NULL, \n\texpires_at TIMESTAMP WITH TIME ZONE NOT NULL, \n\trevoked_at TIMESTAMP WITH TIME ZONE, \n\tid UUID NOT NULL, \n\tcreated_at TIMESTAMP WITH TIME ZONE NOT NULL, \n\tCONSTRAINT pk_auth_sessions PRIMARY KEY (id), \n\tCONSTRAINT fk_auth_sessions_business_id_users FOREIGN KEY(business_id, user_id) REFERENCES users (business_id, id), \n\tCONSTRAINT uq_auth_sessions_refresh_hash UNIQUE (refresh_hash)\n)\n\n')
    op.execute('CREATE INDEX ix_auth_sessions_expires_at ON auth_sessions (expires_at)')
    op.execute('CREATE INDEX ix_auth_sessions_user_id ON auth_sessions (user_id)')
    op.execute('\nCREATE TABLE journal_entries (\n\ttransaction_id BIGINT DEFAULT txid_current() NOT NULL, \n\tbusiness_id UUID NOT NULL, \n\tsource_type VARCHAR(60) NOT NULL, \n\tsource_id VARCHAR(100) NOT NULL, \n\tevent VARCHAR(60) NOT NULL, \n\taccounting_date DATE NOT NULL, \n\tcurrency VARCHAR(3) NOT NULL, \n\tactor_id UUID NOT NULL, \n\tid UUID NOT NULL, \n\tcreated_at TIMESTAMP WITH TIME ZONE NOT NULL, \n\tCONSTRAINT pk_journal_entries PRIMARY KEY (id), \n\tCONSTRAINT uq_journal_entries_business_id_source_type_source_id_event UNIQUE (business_id, source_type, source_id, event), \n\tCONSTRAINT uq_journal_entries_business_id_id UNIQUE (business_id, id), \n\tCONSTRAINT fk_journal_entries_business_id_users FOREIGN KEY(business_id, actor_id) REFERENCES users (business_id, id), \n\tCONSTRAINT fk_journal_entries_business_id_businesses FOREIGN KEY(business_id) REFERENCES businesses (id)\n)\n\n')
    op.execute('CREATE INDEX ix_journal_business_date ON journal_entries (business_id, accounting_date)')
    op.execute('\nCREATE TABLE role_permissions (\n\trole_id UUID NOT NULL, \n\tpermission_code VARCHAR(100) NOT NULL, \n\tCONSTRAINT pk_role_permissions PRIMARY KEY (role_id, permission_code), \n\tCONSTRAINT fk_role_permissions_role_id_roles FOREIGN KEY(role_id) REFERENCES roles (id), \n\tCONSTRAINT fk_role_permissions_permission_code_permissions FOREIGN KEY(permission_code) REFERENCES permissions (code)\n)\n\n')
    op.execute('\nCREATE TABLE user_roles (\n\tbusiness_id UUID NOT NULL, \n\tuser_id UUID NOT NULL, \n\trole_id UUID NOT NULL, \n\tCONSTRAINT pk_user_roles PRIMARY KEY (business_id, user_id, role_id), \n\tCONSTRAINT fk_user_roles_business_id_users FOREIGN KEY(business_id, user_id) REFERENCES users (business_id, id), \n\tCONSTRAINT fk_user_roles_business_id_roles FOREIGN KEY(business_id, role_id) REFERENCES roles (business_id, id)\n)\n\n')
    op.execute('CREATE INDEX ix_user_roles_role ON user_roles (business_id, role_id)')
    op.execute('\nCREATE TABLE journal_entry_lines (\n\tbusiness_id UUID NOT NULL, \n\tentry_id UUID NOT NULL, \n\taccount_id UUID NOT NULL, \n\tdebit NUMERIC(20, 6) NOT NULL, \n\tcredit NUMERIC(20, 6) NOT NULL, \n\tid UUID NOT NULL, \n\tcreated_at TIMESTAMP WITH TIME ZONE NOT NULL, \n\tCONSTRAINT pk_journal_entry_lines PRIMARY KEY (id), \n\tCONSTRAINT fk_journal_entry_lines_business_id_journal_entries FOREIGN KEY(business_id, entry_id) REFERENCES journal_entries (business_id, id), \n\tCONSTRAINT fk_journal_entry_lines_business_id_accounts FOREIGN KEY(business_id, account_id) REFERENCES accounts (business_id, id), \n\tCONSTRAINT ck_journal_entry_lines_one_positive_side CHECK ((debit > 0 AND credit = 0) OR (credit > 0 AND debit = 0)), \n\tCONSTRAINT ck_journal_entry_lines_finite_amount CHECK (debit < 100000000000000 AND credit < 100000000000000)\n)\n\n')
    op.execute('CREATE INDEX ix_journal_entry_lines_account_id ON journal_entry_lines (account_id)')
    op.execute('CREATE INDEX ix_journal_entry_lines_entry_id ON journal_entry_lines (entry_id)')
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
