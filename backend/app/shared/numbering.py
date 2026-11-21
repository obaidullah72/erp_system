from sqlalchemy.dialects.postgresql import insert
from app.db.model_registry import DocumentSequence


def next_number(db, business_id, document_type, year):
    """Transactional allocation; rollback may reuse a number. Caller owns commit."""
    row = insert(DocumentSequence).values(business_id=business_id, document_type=document_type, year=year, next_value=2)
    value = db.scalar(row.on_conflict_do_update(
        index_elements=['business_id', 'document_type', 'year'],
        set_={'next_value': DocumentSequence.next_value + 1}).returning(DocumentSequence.next_value))
    return f'{document_type}-{year}-{value - 1:06d}'
