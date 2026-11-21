from app.db.model_registry import AuditLog


def audit(db, business_id, actor_id, action, resource_id, request_id=None):
    # Deliberately no free-form request payload: credentials and personal data stay out of audit.
    db.add(AuditLog(business_id=business_id, actor_id=actor_id, action=action,
                    resource_id=str(resource_id), request_id=request_id))
