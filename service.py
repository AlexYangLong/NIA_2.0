from contextlib import contextmanager

from sqlalchemy.orm import sessionmaker

from Src.common import model

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
