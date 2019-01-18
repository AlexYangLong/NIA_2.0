from flask import request, jsonify, session
from flask_restful import Resource

from Src.common import status_code
from Src.common.constant import ESSAY_REQUIRED_FIELD
from Src.services.essay_service import EssayService
from Src.utils import check_utils
from Src.utils.decorator import login_required, user_is_active


class EssayController(Resource):
    @staticmethod
    def get(eid=None):
        if not check_utils.check_param_format(request.path, [r"^/v1/bms/essay/([1-9][0-9]*)/$", r"^/v1/bms/essay/$"]):
            return jsonify(status_code.URL_ERROR)
        try:
            essay_service = EssayService()
            if eid:
                essay = essay_service.get_essay_by_id(essay_id=eid)
                if not essay:
                    return jsonify(status_code.ESSAY_NOT_EXIST)
                result = status_code.SUCCESS
                result["data"] = essay
                return jsonify(result)
            else:
                data = request.args
                if not data:
                    essay_list = essay_service.get_all_essay()
                    result = status_code.SUCCESS
                    result["data"] = essay_list
                    return jsonify(result)
                elif isinstance(data, dict) and data.get("title"):
                    essay_list = essay_service.get_essay_by_title(title=data.get("title"))
                    result = status_code.SUCCESS
                    result["data"] = essay_list
                    return jsonify(result)
                else:
                    return jsonify(status_code.ARGS_PARAMS_ERROR)
        except Exception as ex:
            print(ex)
            return jsonify(status_code.FAIL)

    @staticmethod
    @login_required
    @user_is_active
    def post(eid=None):
        if not check_utils.check_param_format(request.path, [r"^/v1/bms/essay/$"]):
            return jsonify(status_code.URL_ERROR)
        user_id = session.get("user_id")
        data = request.json
        if not (data and isinstance(data, dict)):
            return jsonify(status_code.JSON_PARAMS_ERROR)
        for k, v in ESSAY_REQUIRED_FIELD.items():
            if not data.get(k):
                return jsonify({"code": status_code.REQUIRED_PARAM_CODE,
                                "msg_cn": status_code.REQUIRED_PARAM_MSG_CN.format(v),
                                "msg_en": status_code.REQUIRED_PARAM_MSG_EN.format(k)})
        # 正则验证

        try:
            essay_service = EssayService()
            essay_service.create_essay(user_id=user_id, title=data.get("title"),
                                       abstract=data.get("abstract"), content=data.get("content"),
                                       status=data.get("status"))
            return jsonify(status_code.SUCCESS)
        except Exception as ex:
            print(ex)
            return jsonify(status_code.FAIL)

    @staticmethod
    @login_required
    @user_is_active
    def put(eid=None):
        if not check_utils.check_param_format(request.path, [r"^/v1/bms/essay/([1-9][0-9]*)/$"]):
            return jsonify(status_code.URL_ERROR)
        data = request.json
        if not (data and isinstance(data, dict)):
            return jsonify(status_code.JSON_PARAMS_ERROR)
        for k, v in ESSAY_REQUIRED_FIELD.items():
            if not data.get(k):
                return jsonify({"code": status_code.REQUIRED_PARAM_CODE,
                                "msg_cn": status_code.REQUIRED_PARAM_MSG_CN.format(v),
                                "msg_en": status_code.REQUIRED_PARAM_MSG_EN.format(k)})
        try:
            essay_service = EssayService()
            essay = essay_service.get_essay_by_id(essay_id=eid)
            if not essay:
                return jsonify(status_code.ESSAY_NOT_EXIST)
            essay_service.update_essay(essay_id=eid, title=data.get("title"),
                                       abstract=data.get("abstract"), content=data.get("content"),
                                       status=data.get("status"))
            return jsonify(status_code.SUCCESS)
        except Exception as ex:
            print(ex)
            return jsonify(status_code.FAIL)

    @staticmethod
    @login_required
    @user_is_active
    def delete(eid=None):
        if not check_utils.check_param_format(request.path, [r"^/v1/bms/essay/$"]):
            return jsonify(status_code.URL_ERROR)
        data = request.json
        if not (data and isinstance(data, dict)) or not isinstance(data.get("ids"), list):
            return jsonify(status_code.JSON_PARAMS_ERROR)
        if not data.get("ids"):
            return jsonify({"code": status_code.REQUIRED_PARAM_CODE,
                            "msg_cn": status_code.REQUIRED_PARAM_MSG_CN.format("随笔id"),
                            "msg_en": status_code.REQUIRED_PARAM_MSG_EN.format("essay ids")})
        try:
            essay_service = EssayService()
            essay_service.delete_essay(essay_id_list=data.get("ids"))
            return jsonify(status_code.SUCCESS)
        except Exception as ex:
            print(ex)
            return jsonify(status_code.FAIL)
