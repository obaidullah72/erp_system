#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
ERP_TEST_ROOT=$(mktemp -d "/tmp/erp-foundation.XXXXXX")
ERP_TEST_PORT=${ERP_TEST_PORT:-55439}
cleanup() {
  pg_ctl -D "$ERP_TEST_ROOT/data" -m fast stop >/dev/null 2>&1 || true
  # Retain temporary files/logs for diagnosing failures; OS temp cleanup may remove them.
  echo "Test logs: $ERP_TEST_ROOT"
}
trap cleanup EXIT
initdb -D "$ERP_TEST_ROOT/data" -A trust -U erp_test --no-locale -E UTF8 >"$ERP_TEST_ROOT/init.log"
pg_ctl -D "$ERP_TEST_ROOT/data" -l "$ERP_TEST_ROOT/postgres.log" -o "-p $ERP_TEST_PORT -h 127.0.0.1 -k $ERP_TEST_ROOT" start
createdb -h 127.0.0.1 -p "$ERP_TEST_PORT" -U erp_test erp_test
export ERP_TEST_DATABASE_URL="postgresql+psycopg://erp_test@127.0.0.1:$ERP_TEST_PORT/erp_test"
make test-integration
make test-e2e
