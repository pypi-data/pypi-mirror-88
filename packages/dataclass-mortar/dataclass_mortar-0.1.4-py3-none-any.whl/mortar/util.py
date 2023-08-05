from dataclasses import asdict

import datetime
from functools import wraps

from sqlalchemy import MetaData
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import FlushError
from sqlalchemy.orm.session import sessionmaker, Session

Datetime = datetime.datetime


class _Empty: ...

_Session = sessionmaker()
def operation(func):
    @wraps(func)
    def wrapper(instance: MetaData, item, session=None):
        instance.ensure_table_exists(item)

        commit = session is None
        session: Session = session or Session(bind=instance.bind)
        ret = func(instance, item, session)
        if commit:
            try:
                session.commit()
            except (IntegrityError) as ex:
                session.rollback()
                v = session.query(type(item)).get(item.item_id)
                if v != item:
                    diff = asdict(item).items() ^ asdict(v).items()
                    if v.run_date == item.run_date:
                        print(f"Update suppressed: {v.id} {diff}")
                        return
                    raise NotImplementedError(f"Update needed {diff}")
            except FlushError as ex:
                session.rollback()
                session.merge(item)
                session.commit()
            finally:
                session.close()
        if ret == _Empty:
            return None
        return ret or instance

    return wrapper
