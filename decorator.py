from functools import wraps

from flask import jsonify, session, request

from Src.common import status_code
from Src.common.service import LogService
from Src.services.user_service import UserService
from Src.utils import log as logger


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not (session and session.get("user_id") and session.get("token")):
            return status_code.USER_NO_LOGIN
        try:
            user_service = UserService()
            user = user_service.get_user_by_id(session.get("user_id"))
            if not user:
                return status_code.USER_NOT_EXIST
            if not user.get("is_active"):
                return status_code.USER_IS_NOT_ACTIVE
            if user.get("token") != session.get("token"):
                return status_code.PLEASE_LOGIN
        except Exception as ex:
            print(ex)
            logger.error("认证失败,{}".format(ex))
            return status_code.FAIL

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


def write_operate_log(action_cn="", action_en=""):
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            ip = request.remote_addr

            result = func(*args, **kwargs)

            if session and session.get("user_id"):
                user_id = session.get("user_id")
            else:
                user_id = None

            if result.get("code") == status_code.SUCCESS_CODE:
                result_cn = "成功"
                result_en = "SUCCESS"
            else:
                result_cn = "失败"
                result_en = "FAIL"
            # 在这里写操作日志
            try:
                LogService().write_log(client_ip=ip, action_cn=action_cn, action_en=action_en,
                                       result_cn=result_cn, result_en=result_en,
                                       reason_cn=result.get("msg_cn"), reason_en=result.get("msg_en"),
                                       user_id=user_id)
            except Exception as ex:
                print(ex)
                logger.error("写操作日志失败,{}".format(ex))
            return jsonify(result)

        return inner
    return wrapper
