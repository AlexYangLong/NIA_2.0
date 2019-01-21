from flask import request, session
from flask_restful import Resource

from Src.common import status_code
from Src.common.constant import USER_REQUIRED_FIELD
from Src.common.service import get_reset_password
from Src.services.user_service import UserService
from Src.utils import check_utils
from Src.utils import log as logger
from Src.utils.decorator import login_required, write_operate_log


class RegisterController(Resource):

    @staticmethod
    @write_operate_log(action_cn="用户注册", action_en="User register")
    def post():
        data = request.json
        if not (data and isinstance(data, dict)):
            return status_code.JSON_PARAMS_ERROR
        for k, v in USER_REQUIRED_FIELD.items():
            if not data.get(k):
                return {"code": status_code.REQUIRED_PARAM_CODE,
                        "msg_cn": status_code.REQUIRED_PARAM_MSG_CN.format(v),
                        "msg_en": status_code.REQUIRED_PARAM_MSG_EN.format(k)}
        # 正则验证

        account = data.get("account")
        password = data.get("password")
        phone = data.get("phone")
        try:
            user_service = UserService()
            user = user_service.get_user_by_account(account=account)
            if user:
                return status_code.USER_ACCOUNT_EXIST
            user_service.create_user(account=account, password=password, phone=phone)
            return status_code.SUCCESS
        except Exception as ex:
            print(ex)
            logger.error("用户注册失败,{}".format(ex))
            return status_code.FAIL


class LoginController(Resource):

    @staticmethod
    @write_operate_log(action_cn="用户登录", action_en="User login")
    def post():
        data = request.json
        session.clear()
        if not (data and isinstance(data, dict)):
            return status_code.JSON_PARAMS_ERROR
        account = data.get("account")
        password = data.get("password")
        if not account:
            return {"code": status_code.REQUIRED_PARAM_CODE,
                    "msg_cn": status_code.REQUIRED_PARAM_MSG_CN.format("帐号"),
                    "msg_en": status_code.REQUIRED_PARAM_MSG_EN.format("account")}
        if not password:
            return {"code": status_code.REQUIRED_PARAM_CODE,
                    "msg_cn": status_code.REQUIRED_PARAM_MSG_CN.format("密码"),
                    "msg_en": status_code.REQUIRED_PARAM_MSG_EN.format("password")}
        try:
            user_service = UserService()
            user = user_service.get_user_by_account(account=account)
            if not user:
                return status_code.USER_NOT_EXIST
            if not user.get("is_active"):
                return status_code.USER_IS_NOT_ACTIVE
            if not user_service.check_user_password(user_id=user.get("id"), password=password):
                return status_code.PASSWORD_ERROR
            token = user_service.change_user_token(user_id=user.get("id"))
            session["user_id"] = user.get("id")
            session["token"] = token
            result = status_code.SUCCESS
            result["token"] = token
            return result
        except Exception as ex:
            print(ex)
            logger.error("用户登录失败,{}".format(ex))
            return status_code.FAIL


class UserInfoController(Resource):
    @staticmethod
    @write_operate_log(action_cn="获取用户", action_en="Get user or list")
    @login_required
    def get(uid=None):
        if not check_utils.check_param_format(request.path, [r"^/v1/bms/user/([1-9][0-9]*)/$", r"^/v1/bms/user/$"]):
            return status_code.URL_ERROR
        try:
            user_service = UserService()
            if uid:
                user = user_service.get_user_by_id(user_id=uid)
                if not user:
                    return status_code.USER_NOT_EXIST
                result = status_code.SUCCESS
                result["data"] = user
                return result
            else:
                users = user_service.get_users()
                result = status_code.SUCCESS
                result["data"] = users
                return result
        except Exception as ex:
            print(ex)
            logger.error("获取用户失败,{}".format(ex))
            return status_code.FAIL

    @staticmethod
    @write_operate_log(action_cn="创建用户", action_en="Create user")
    @login_required
    def post(uid=None):
        if not check_utils.check_param_format(request.path, [r"^/v1/bms/user/$"]):
            return status_code.URL_ERROR
        data = request.json
        if not (data and isinstance(data, dict)):
            return status_code.JSON_PARAMS_ERROR
        for k, v in USER_REQUIRED_FIELD.items():
            if not data.get(k):
                return {"code": status_code.REQUIRED_PARAM_CODE,
                        "msg_cn": status_code.REQUIRED_PARAM_MSG_CN.format(v),
                        "msg_en": status_code.REQUIRED_PARAM_MSG_EN.format(k)}
        # 正则验证

        try:
            user_service = UserService()
            user = user_service.get_user_by_account(account=data.get("account"))
            if user:
                return status_code.USER_ACCOUNT_EXIST
            user_service.create_user(account=data.get("account"), password=data.get("password"),
                                     phone=data.get("phone"), username=data.get("username"),
                                     gender=data.get("gender"), email=data.get("email"),
                                     birth=data.get("birth"), is_active=data.get("is_active"))
            return status_code.SUCCESS
        except Exception as ex:
            print(ex)
            logger.error("创建用户失败,{}".format(ex))
            return status_code.FAIL

    @staticmethod
    @write_operate_log(action_cn="修改用户基础信息", action_en="Update user basic info")
    @login_required
    def put(uid=None):
        if not check_utils.check_param_format(request.path, [r"^/v1/bms/user/([1-9][0-9]*)/$"]):
            return status_code.URL_ERROR
        data = request.json
        if not (data and isinstance(data, dict)):
            return status_code.JSON_PARAMS_ERROR
        if not data.get("phone"):
            return {"code": status_code.REQUIRED_PARAM_CODE,
                    "msg_cn": status_code.REQUIRED_PARAM_MSG_CN.format("电话号码"),
                    "msg_en": status_code.REQUIRED_PARAM_MSG_EN.format("phone")}
        try:
            user_service = UserService()
            user = user_service.get_user_by_id(user_id=uid)
            if not user:
                return status_code.USER_NOT_EXIST
            user_service.update_user_basic(user_id=uid, phone=data.get("phone"),
                                                  username=data.get("username"), gender=data.get("gender"),
                                                  email=data.get("email"), birth=data.get("birth"))
            return status_code.SUCCESS
        except Exception as ex:
            print(ex)
            logger.error("修改用户基础信息失败,{}".format(ex))
            return status_code.FAIL

    @staticmethod
    @write_operate_log(action_cn="修改用户状态", action_en="Update user active status")
    @login_required
    def patch(uid=None):
        if not check_utils.check_param_format(request.path, [r"^/v1/bms/user/$"]):
            return status_code.URL_ERROR
        data = request.json
        if not (data and isinstance(data, dict)) or not isinstance(data.get("ids"), list):
            return status_code.JSON_PARAMS_ERROR
        if not data.get("ids"):
            return {"code": status_code.REQUIRED_PARAM_CODE,
                    "msg_cn": status_code.REQUIRED_PARAM_MSG_CN.format("用户id"),
                    "msg_en": status_code.REQUIRED_PARAM_MSG_EN.format("user ids")}
        # if data.get("is_active") == None or data.get("is_active") == "":
        #     return {"code": status_code.REQUIRED_PARAM_CODE,
#                     "msg_cn": status_code.REQUIRED_PARAM_MSG_CN.format("激活状态"),
#                     "msg_en": status_code.REQUIRED_PARAM_MSG_EN.format("active status")}
        if not isinstance(data.get("is_active"), bool):
            return status_code.ACTIVE_NOT_BOOL
        try:
            user_service = UserService()
            user_service.change_user_status(is_active=data.get("is_active"), user_id_list=data.get("ids"))
            return status_code.SUCCESS
        except Exception as ex:
            print(ex)
            logger.error("修改用户状态失败,{}".format(ex))
            return status_code.FAIL

    @staticmethod
    @write_operate_log(action_cn="删除用户", action_en="Delete user")
    @login_required
    def delete(uid=None):
        if not check_utils.check_param_format(request.path, [r"^/v1/bms/user/$"]):
            return status_code.URL_ERROR
        data = request.json
        if not (data and isinstance(data, dict)) or not isinstance(data.get("ids"), list):
            return status_code.JSON_PARAMS_ERROR
        if not data.get("ids"):
            return {"code": status_code.REQUIRED_PARAM_CODE,
                    "msg_cn": status_code.REQUIRED_PARAM_MSG_CN.format("用户id"),
                    "msg_en": status_code.REQUIRED_PARAM_MSG_EN.format("user ids")}
        try:
            user_service = UserService()
            user_service.delete_user(user_id_list=data.get("ids"))
            return status_code.SUCCESS
        except Exception as ex:
            print(ex)
            logger.error("删除用户失败,{}".format(ex))
            return status_code.FAIL


class UserPwdController(Resource):
    @staticmethod
    @write_operate_log(action_cn="修改密码", action_en="Update user password")
    @login_required
    def patch():
        if not check_utils.check_param_format(request.path, [r"^/v1/bms/user/password/$"]):
            return status_code.URL_ERROR
        user_id = session.get("user_id")
        data = request.json
        if not (data and isinstance(data, dict)):
            return status_code.JSON_PARAMS_ERROR
        if not data.get("old_password"):
            return {"code": status_code.REQUIRED_PARAM_CODE,
                            "msg_cn": status_code.REQUIRED_PARAM_MSG_CN.format("原密码"),
                            "msg_en": status_code.REQUIRED_PARAM_MSG_EN.format("old password")}
        if not data.get("new_password"):
            return {"code": status_code.REQUIRED_PARAM_CODE,
                            "msg_cn": status_code.REQUIRED_PARAM_MSG_CN.format("新密码"),
                            "msg_en": status_code.REQUIRED_PARAM_MSG_EN.format("new password")}
        try:
            user_service = UserService()
            user = user_service.get_user_by_id(user_id=user_id)
            if not user:
                return status_code.USER_NOT_EXIST
            if not user_service.check_user_password(user_id=user_id, password=data.get("old_password")):
                return status_code.PASSWORD_ERROR
            user_service.update_user_password(user_id=user_id, new_password=data.get("new_password"))
            return status_code.SUCCESS
        except Exception as ex:
            print(ex)
            logger.error("修改用户密码失败,{}".format(ex))
            return status_code.FAIL


class ResetPwdController(Resource):
    @staticmethod
    @write_operate_log(action_cn="重置密码", action_en="Reset user password")
    @login_required
    def patch(uid=None):
        if not check_utils.check_param_format(request.path, [r"^/v1/bms/user/([1-9][0-9]*)/password/$"]):
            return status_code.URL_ERROR
        try:
            user_service = UserService()
            new_password = get_reset_password()
            user_service.update_user_password(user_id=uid, new_password=new_password)
            result = status_code.SUCCESS
            result["new_password"] = new_password
            return result
        except Exception as ex:
            print(ex)
            logger.error("重置用户密码失败,{}".format(ex))
            return status_code.FAIL
