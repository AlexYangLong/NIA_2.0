from functools import wraps

from flask import jsonify, session

from Src.common import status_code
from Src.common.service import LogService
from Src.services.user_service import UserService
from Src.utils import log as logger


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get("user_id"):
            return jsonify(status_code.NO_LOGIN)

        return func(*args, **kwargs)
    return wrapper

def user_is_active(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            user_service = UserService()
            if not user_service.get_user_active(user_id=session.get("user_id")):
                return jsonify(status_code.USER_IS_NOT_ACTIVE)
        except Exception as ex:
            print(ex)
            return jsonify(status_code.FAIL)

        return func(*args, **kwargs)
    return wrapper


def write_operate_log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        # 在这里写入日志文件
        if result.get("code") == 200:
            # LogService().write_log()
            print("aaa")
        else:
            print("bbb")
        return jsonify(result)

    return wrapper
