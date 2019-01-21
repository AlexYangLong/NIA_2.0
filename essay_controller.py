from flask import request, session
from flask_restful import Resource

from Src.common import status_code
from Src.common.constant import ESSAY_REQUIRED_FIELD, ESSAY_STATUS
from Src.services.essay_service import EssayService
from Src.utils import check_utils
from Src.utils import log as logger
from Src.utils.decorator import login_required, write_operate_log


class EssayController(Resource):
    @staticmethod
    @write_operate_log(action_cn="获取随笔", action_en="Get essay or list")
    def get(eid=None):
        if not check_utils.check_param_format(request.path, [r"^/v1/bms/essay/([1-9][0-9]*)/$", r"^/v1/bms/essay/$"]):
            return status_code.URL_ERROR
        try:
            essay_service = EssayService()
            if eid:
                essay = essay_service.get_essay_by_id(essay_id=eid)
                if not essay:
                    return status_code.ESSAY_NOT_EXIST
                result = status_code.SUCCESS
                result["data"] = essay
                return result
            else:
                data = request.args
                if not data:
                    essay_list = essay_service.get_all_essay()
                    result = status_code.SUCCESS
                    result["data"] = essay_list
                    return result
                elif isinstance(data, dict) and data.get("title"):
                    essay_list = essay_service.get_essay_by_title(title=data.get("title"))
                    result = status_code.SUCCESS
                    result["data"] = essay_list
                    return result
                else:
                    return status_code.ARGS_PARAMS_ERROR
        except Exception as ex:
            print(ex)
            logger.error("获取随笔失败,{}".format(ex))
            return status_code.FAIL

    @staticmethod
    @write_operate_log(action_cn="创建随笔", action_en="Create essay")
    @login_required
    def post(eid=None):
        if not check_utils.check_param_format(request.path, [r"^/v1/bms/essay/$"]):
            return status_code.URL_ERROR
        user_id = session.get("user_id")
        data = request.json
        if not (data and isinstance(data, dict)):
            return status_code.JSON_PARAMS_ERROR
        for k, v in ESSAY_REQUIRED_FIELD.items():
            if not data.get(k):
                return {"code": status_code.REQUIRED_PARAM_CODE,
                        "msg_cn": status_code.REQUIRED_PARAM_MSG_CN.format(v),
                        "msg_en": status_code.REQUIRED_PARAM_MSG_EN.format(k)}
        if not isinstance(data.get("status"), int):
            return status_code.ESSAY_STATUS_NOT_INT
        if data.get("status") not in ESSAY_STATUS.values():
            return status_code.ESSAY_STATUS_OUT_RANGE
        # 正则验证

        try:
            essay_service = EssayService()
            essay_service.create_essay(user_id=user_id, title=data.get("title"),
                                       abstract=data.get("abstract"), content=data.get("content"),
                                       status=data.get("status"))
            return status_code.SUCCESS
        except Exception as ex:
            print(ex)
            logger.error("创建随笔失败,{}".format(ex))
            return status_code.FAIL

    @staticmethod
    @write_operate_log(action_cn="修改随笔", action_en="Update essay")
    @login_required
    def put(eid=None):
        if not check_utils.check_param_format(request.path, [r"^/v1/bms/essay/([1-9][0-9]*)/$"]):
            return status_code.URL_ERROR
        data = request.json
        if not (data and isinstance(data, dict)):
            return status_code.JSON_PARAMS_ERROR
        for k, v in ESSAY_REQUIRED_FIELD.items():
            if not data.get(k):
                return {"code": status_code.REQUIRED_PARAM_CODE,
                        "msg_cn": status_code.REQUIRED_PARAM_MSG_CN.format(v),
                        "msg_en": status_code.REQUIRED_PARAM_MSG_EN.format(k)}
        try:
            essay_service = EssayService()
            essay = essay_service.get_essay_by_id(essay_id=eid)
            if not essay:
                return status_code.ESSAY_NOT_EXIST
            essay_service.update_essay(essay_id=eid, title=data.get("title"),
                                       abstract=data.get("abstract"), content=data.get("content"),
                                       status=data.get("status"))
            return status_code.SUCCESS
        except Exception as ex:
            print(ex)
            logger.error("修改随笔失败,{}".format(ex))
            return status_code.FAIL

    @staticmethod
    @write_operate_log(action_cn="删除随笔", action_en="Delete essay")
    @login_required
    def delete(eid=None):
        if not check_utils.check_param_format(request.path, [r"^/v1/bms/essay/$"]):
            return status_code.URL_ERROR
        data = request.json
        if not (data and isinstance(data, dict)) or not isinstance(data.get("ids"), list):
            return status_code.JSON_PARAMS_ERROR
        if not data.get("ids"):
            return {"code": status_code.REQUIRED_PARAM_CODE,
                    "msg_cn": status_code.REQUIRED_PARAM_MSG_CN.format("随笔id"),
                    "msg_en": status_code.REQUIRED_PARAM_MSG_EN.format("essay ids")}
        try:
            essay_service = EssayService()
            essay_service.delete_essay(essay_id_list=data.get("ids"))
            return status_code.SUCCESS
        except Exception as ex:
            print(ex)
            logger.error("删除随笔失败,{}".format(ex))
            return status_code.FAIL
