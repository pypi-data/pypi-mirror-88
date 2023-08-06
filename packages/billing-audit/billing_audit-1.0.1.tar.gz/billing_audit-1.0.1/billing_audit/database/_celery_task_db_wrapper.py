import logging
import functools


class DatabaseWrapper:
    def __init__(self, databases_mapping):
        self.databases_mapping = databases_mapping

    def __get_task_id(self, task):
        if task.request:
            return task.request.id
        return None

    def _set_sessions(self, task, databases):
        task_id = self.__get_task_id(task)
        if not databases:
            return
        for db_name, session_cls in self.databases_mapping.items():
            if db_name in databases:
                setattr(task, db_name, session_cls())
                logging.info(f"Task: {task_id} - Database {db_name} has been created")

    def _rollback_sessions(self, task, databases):
        task_id = self.__get_task_id(task)
        if not databases:
            return
        for name in databases:
            session = getattr(task, name)
            if session:
                session.rollback()
                logging.info(f"Task: {task_id} - Database {name} has been rolled back")

    def _close_sessions(self, task, databases):
        task_id = self.__get_task_id(task)
        if not databases:
            return
        for name in databases:
            session = getattr(task, name)
            if session:
                session.close()
                session.bind.dispose()
                logging.info(f"Task: {task_id} - Database {name} has been closed")

    def wraps(self, **opts):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(task, *args, **kwargs):
                databases = opts.get("databases")
                if not databases:
                    logging.warning(f"func: {func.__name__} - databases is required")
                    databases = {}
                self._set_sessions(task, databases)
                try:
                    result = func(task, *args, **kwargs)
                except Exception as exc:
                    self._rollback_sessions(task, databases)
                    raise exc
                else:
                    return result
                finally:
                    self._close_sessions(task, databases)
            return wrapper
        return decorator

