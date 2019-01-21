from contextlib import contextmanager
import random

from sqlalchemy.orm import sessionmaker

from Src.common import model
from Src.common.constant import RANDOM_CHAR
from Src.common.model import LogInfo, UserInfo

Session = sessionmaker(bind=model.engine)


def get_session():
    return Session()


@contextmanager
def session_scope():
    session = get_session()
    try:
        yield session
        session.commit()
    except Exception as ex:
        session.rollback()
        raise Exception(ex)
    finally:
        session.close()


class LogService(object):
    @staticmethod
    def write_log(client_ip, action_cn, action_en, result_cn, result_en, reason_cn=None, reason_en=None, user_id=None):
        log = LogInfo({
            "client_ip": client_ip,
            "action_cn": action_cn,
            "action_en": action_en,
            "result_cn": result_cn,
            "result_en": result_en,
            "reason_cn": reason_cn,
            "reason_en": reason_en,
            "user_id": user_id
        })
        with session_scope() as session:
            session.add(log)


def get_reset_password():
    return "".join(random.choices(RANDOM_CHAR, k=8))


# class Message(object):
#     def __init__(self, code, msg_cn, msg_en):
#         self.code = code
#         self.msg_cn = msg_cn
#         self.msg_en = msg_en
#
#     def to_dict(self):
#         return {
#             "code": self.code,
#             "msg_cn": self.msg_cn,
#             "msg_en": self.msg_en
#         }
