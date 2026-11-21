import json
import logging
from app.core.logging import JsonFormatter
from app.workers.celery_app import ping


def test_structured_logs_do_not_capture_credentials(client, caplog):
    caplog.set_level(logging.INFO)
    response=client.post('/api/v1/auth/login?secret=never-log-query', json={
        'business':'demo','email':'admin@example.com','password':'never-log-password'},
        headers={'Authorization':'Bearer never-log-token'})
    assert response.status_code == 401
    client.get('/api/v1/not-a-route/never-log-path')
    records=[r for r in caplog.records if r.name=='app.core.middleware']
    assert records
    encoded='\n'.join(JsonFormatter().format(r) for r in records)
    for secret in ('never-log-query','never-log-password','never-log-token','never-log-path','admin@example.com'):
        assert secret not in encoded
    for line in encoded.splitlines():
        entry=json.loads(line)
        assert entry['request_id'] and entry['status'] and 'duration_ms' in entry


def test_worker_diagnostic_has_no_business_side_effects():
    assert ping.apply().get() == 'pong'
