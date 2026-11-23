"""Export implemented contracts using inert settings; does not connect to the database."""
import json
import os
from pathlib import Path
os.environ['ENVIRONMENT'] = 'test'
os.environ['JWT_SECRET_KEY'] = 'schema-export-only-inert-key-not-for-deployment'
os.environ['DATABASE_URL'] = 'postgresql+psycopg://schema@127.0.0.1:1/schema_test'
from app.main import create_app

if __name__ == '__main__':
    destination = Path(__file__).resolve().parents[2] / 'docs' / 'openapi.json'
    destination.write_text(json.dumps(create_app().openapi(), indent=2, sort_keys=True) + '\n')
    print('Wrote docs/openapi.json (implemented routes only).')
