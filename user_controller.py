from contextlib import closing

from flask import request, jsonify
from flask_restful import Resource

from Src.common import status_code
from Src.common.constant import USER_REQUIRED_FIELD
from Src.services.user_service import UserService


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
        account = data.get("account")
        password = data.get("password")
        phone = data.get("phone")
        try:
            user_service = UserService()
            user_service.create_user(account=account, password=password, phone=phone)
            return jsonify({"code": status_code.SUCCESS_CODE,
                            "msg_cn": status_code.SUCCESS_MSG_CN,
                            "msg_en": status_code.SUCCESS_MSG_EN})
        except Exception as ex:
            print(ex)
            return jsonify({"code": status_code.FAIL_CODE,
                            "msg_cn": status_code.FAIL_MSG_CN,
                            "msg_en": status_code.FAIL_MSG_EN})


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
            user= user_service.get_user_by_account(account=account)
            if not user:
                return jsonify(status_code.USER_ERROR)
            if not user_service.check_user_password(user_id=user.get("id"), password=password):
                return jsonify(status_code.USER_ERROR)
            token = user_service.change_user_token(user_id=user.get("id"))
            return jsonify({"code": status_code.SUCCESS_CODE,
                            "msg_cn": status_code.SUCCESS_MSG_CN,
                            "msg_en": status_code.SUCCESS_MSG_EN,
                            "token": token})
        except Exception as ex:
            print(ex)
            return jsonify({"code": status_code.FAIL_CODE,
                            "msg_cn": status_code.FAIL_MSG_CN,
                            "msg_en": status_code.FAIL_MSG_EN})
