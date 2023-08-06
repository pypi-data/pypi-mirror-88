# AUDIT UTILS

Các function dùng để dùng lại ở số lượng lớn audit repos

## usages
1. DatabaseWrapper: thêm database session cho task celery  
```python
from audit_utils.database import DatabaseWrapper
from somewhere import BillingDatabaseSession
from somewhere import celery_app

databases_mapping = {"billing": BillingDatabaseSession}

db_wrapper = DatabaseWrapper(databases_mapping)

@celery_app.task(bind=True)  # bind=True is required
@db_wrapper.wraps(databases={"billing"})
def task_name(self, *args, **kwargs):
    result = do_something_with_db(self.billing)
    return result
```

#
`from billing.audit import ❤️`
