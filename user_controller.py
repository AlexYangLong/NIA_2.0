from flask import request, jsonify, session
from flask_restful import Resource

from Src.common import status_code
from Src.common.constant import USER_REQUIRED_FIELD
from Src.common.service import get_reset_password
from Src.services.user_service import UserService
from Src.utils import check_utils
from Src.utils.decorator import login_required, user_is_active


class RegisterController(Resource):

    @staticmethod
    def post():
        data = request.json
        if not (data and isinstance(data, dict)):
            return jsonify(status_code.JSON_PARAMS_ERROR)
        for k, v in USER_REQUIRED_FIELD.items():
            if not data.get(k):
                return jsonify({"code": status_code.REQUIRED_PARAM_CODE,
                                "msg_cn": status_code.REQUIRED_PARAM_MSG_CN.format(v),
                                "msg_en": status_code.REQUIRED_PARAM_MSG_EN.format(k)})
        # 正则验证

        account = data.get("account")
        password = data.get("password")
        phone = data.get("phone")
        try:
            user_service = UserService()
            user = user_service.get_user_by_account(account=account)
            if user:
                return jsonify(status_code.USER_ACCOUNT_EXIST)
            user_service.create_user(account=account, password=password, phone=phone)
            return jsonify(status_code.SUCCESS)
        except Exception as ex:
            print(ex)
            return jsonify(status_code.FAIL)


class LoginController(Resource):

    @staticmethod
    def post():
        data = request.json
        if not (data and isinstance(data, dict)):
            return jsonify(status_code.JSON_PARAMS_ERROR)
        account = data.get("account")
        password = data.get("password")
        if not account:
            return jsonify({"code": status_code.REQUIRED_PARAM_CODE,
                            "msg_cn": status_code.REQUIRED_PARAM_MSG_CN.format("帐号"),
                            "msg_en": status_code.REQUIRED_PARAM_MSG_EN.format("account")})
        if not password:
            return jsonify({"code": status_code.REQUIRED_PARAM_CODE,
                            "msg_cn": status_code.REQUIRED_PARAM_MSG_CN.format("密码"),
                            "msg_en": status_code.REQUIRED_PARAM_MSG_EN.format("password")})
        try:
            user_service = UserService()
            user = user_service.get_user_by_account(account=account)
            if not user:
                return jsonify(status_code.USER_NOT_EXIST)
            if not user.get("is_active"):
                return jsonify(status_code.USER_IS_NOT_ACTIVE)
            if not user_service.check_user_password(user_id=user.get("id"), password=password):
                return jsonify(status_code.PASSWORD_ERROR)
            token = user_service.change_user_token(user_id=user.get("id"))
            session["user_id"] = user.get("id")
            result = status_code.SUCCESS
            result["token"] = token
            return jsonify(result)
        except Exception as ex:
            print(ex)
            return jsonify(status_code.FAIL)


class UserInfoController(Resource):
    @staticmethod
    @login_required
    @user_is_active
    def get(uid=None):
        if not check_utils.check_param_format(request.path, [r"^/v1/bms/user/([1-9][0-9]*)/$", r"^/v1/bms/user/$"]):
            return jsonify(status_code.URL_ERROR)
        try:
            user_service = UserService()
            if uid:
                user = user_service.get_user_by_id(user_id=uid)
                if not user:
                    return jsonify(status_code.USER_NOT_EXIST)
                result = status_code.SUCCESS
                result["data"] = user
                return jsonify(result)
            else:
                users = user_service.get_users()
                result = status_code.SUCCESS
                result["data"] = users
                return jsonify(result)
        except Exception as ex:
            print(ex)
            return jsonify(status_code.FAIL)

    @staticmethod
    @login_required
    @user_is_active
    def post(uid=None):
        if not check_utils.check_param_format(request.path, [r"^/v1/bms/user/$"]):
            return jsonify(status_code.URL_ERROR)
        data = request.json
        if not (data and isinstance(data, dict)):
            return jsonify(status_code.JSON_PARAMS_ERROR)
        for k, v in USER_REQUIRED_FIELD.items():
            if not data.get(k):
                return jsonify({"code": status_code.REQUIRED_PARAM_CODE,
                                "msg_cn": status_code.REQUIRED_PARAM_MSG_CN.format(v),
                                "msg_en": status_code.REQUIRED_PARAM_MSG_EN.format(k)})
        # 正则验证

        try:
            user_service = UserService()
            user = user_service.get_user_by_account(account=data.get("account"))
            if user:
                return jsonify(status_code.USER_ACCOUNT_EXIST)
            user_service.create_user(account=data.get("account"), password=data.get("password"),
                                     phone=data.get("phone"), username=data.get("username"),
                                     gender=data.get("gender"), email=data.get("email"),
                                     birth=data.get("birth"), is_active=data.get("is_active"))
            return jsonify(status_code.SUCCESS)
        except Exception as ex:
            print(ex)
            return jsonify(status_code.FAIL)

    @staticmethod
    @login_required
    @user_is_active
    def put(uid=None):
        if not check_utils.check_param_format(request.path, [r"^/v1/bms/user/([1-9][0-9]*)/$"]):
            return jsonify(status_code.URL_ERROR)
        data = request.json
        if not (data and isinstance(data, dict)):
            return jsonify(status_code.JSON_PARAMS_ERROR)
        if not data.get("phone"):
            return jsonify({"code": status_code.REQUIRED_PARAM_CODE,
                            "msg_cn": status_code.REQUIRED_PARAM_MSG_CN.format("电话号码"),
                            "msg_en": status_code.REQUIRED_PARAM_MSG_EN.format("phone")})
        try:
            user_service = UserService()
            user = user_service.get_user_by_id(user_id=uid)
            if not user:
                return jsonify(status_code.USER_NOT_EXIST)
            user_service.update_user_basic(user_id=uid, phone=data.get("phone"),
                                                  username=data.get("username"), gender=data.get("gender"),
                                                  email=data.get("email"), birth=data.get("birth"))
            return jsonify(status_code.SUCCESS)
        except Exception as ex:
            print(ex)
            return jsonify(status_code.FAIL)

    @staticmethod
    @login_required
    @user_is_active
    def patch(uid=None):
        if not check_utils.check_param_format(request.path, [r"^/v1/bms/user/$"]):
            return jsonify(status_code.URL_ERROR)
        data = request.json
        if not (data and isinstance(data, dict)) or not isinstance(data.get("ids"), list):
            return jsonify(status_code.JSON_PARAMS_ERROR)
        if not data.get("ids"):
            return jsonify({"code": status_code.REQUIRED_PARAM_CODE,
                            "msg_cn": status_code.REQUIRED_PARAM_MSG_CN.format("用户id"),
                            "msg_en": status_code.REQUIRED_PARAM_MSG_EN.format("user ids")})
        # if data.get("is_active") == None or data.get("is_active") == "":
        #     return jsonify({"code": status_code.REQUIRED_PARAM_CODE,
        #                     "msg_cn": status_code.REQUIRED_PARAM_MSG_CN.format("激活状态"),
        #                     "msg_en": status_code.REQUIRED_PARAM_MSG_EN.format("active status")})
        if not isinstance(data.get("is_active"), bool):
            return jsonify({"code": status_code.FAIL_CODE,
                            "msg_cn": "激活状态参数不是一个布尔值",
                            "msg_en": "The activation state parameter is not a Boolean value."})
        try:
            user_service = UserService()
            user_service.change_user_status(is_active=data.get("is_active"), user_id_list=data.get("ids"))
            return jsonify(status_code.SUCCESS)
        except Exception as ex:
            print(ex)
            return jsonify(status_code.FAIL)

    @staticmethod
    @login_required
    @user_is_active
    def delete(uid=None):
        if not check_utils.check_param_format(request.path, [r"^/v1/bms/user/$"]):
            return jsonify(status_code.URL_ERROR)
        data = request.json
        if not (data and isinstance(data, dict)) or not isinstance(data.get("ids"), list):
            return jsonify(status_code.JSON_PARAMS_ERROR)
        if not data.get("ids"):
            return jsonify({"code": status_code.REQUIRED_PARAM_CODE,
                            "msg_cn": status_code.REQUIRED_PARAM_MSG_CN.format("用户id"),
                            "msg_en": status_code.REQUIRED_PARAM_MSG_EN.format("user ids")})
        try:
            user_service = UserService()
            user_service.delete_user(user_id_list=data.get("ids"))
            return jsonify(status_code.SUCCESS)
        except Exception as ex:
            print(ex)
            return jsonify(status_code.FAIL)


class UserPwdController(Resource):
    @staticmethod
    @login_required
    @user_is_active
    def patch():
        if not check_utils.check_param_format(request.path, [r"^/v1/bms/user/password/$"]):
            return jsonify(status_code.URL_ERROR)
        user_id = session.get("user_id")
        data = request.json
        if not (data and isinstance(data, dict)):
            return jsonify(status_code.JSON_PARAMS_ERROR)
        if not data.get("old_password"):
            return jsonify({"code": status_code.REQUIRED_PARAM_CODE,
                            "msg_cn": status_code.REQUIRED_PARAM_MSG_CN.format("原密码"),
                            "msg_en": status_code.REQUIRED_PARAM_MSG_EN.format("old password")})
        if not data.get("new_password"):
            return jsonify({"code": status_code.REQUIRED_PARAM_CODE,
                            "msg_cn": status_code.REQUIRED_PARAM_MSG_CN.format("新密码"),
                            "msg_en": status_code.REQUIRED_PARAM_MSG_EN.format("new password")})
        try:
            user_service = UserService()
            user = user_service.get_user_by_id(user_id=user_id)
            if not user:
                return jsonify(status_code.USER_NOT_EXIST)
            if not user_service.check_user_password(user_id=user_id, password=data.get("old_password")):
                return jsonify(status_code.PASSWORD_ERROR)
            user_service.update_user_password(user_id=user_id, new_password=data.get("new_password"))
            return jsonify(status_code.SUCCESS)
        except Exception as ex:
            print(ex)
            return jsonify(status_code.FAIL)


class ResetPwdController(Resource):
    @staticmethod
    @login_required
    @user_is_active
    def patch(uid=None):
        if not check_utils.check_param_format(request.path, [r"^/v1/bms/user/([1-9][0-9]*)/password/$"]):
            return jsonify(status_code.URL_ERROR)
        try:
            user_service = UserService()
            new_password = get_reset_password()
            user_service.update_user_password(user_id=uid, new_password=new_password)
            result = status_code.SUCCESS
            result["new_password"] = new_password
            return jsonify(result)
        except Exception as ex:
            print(ex)
            return jsonify(status_code.FAIL)
