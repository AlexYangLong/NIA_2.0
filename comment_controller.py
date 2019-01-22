from flask import request, session
from flask_restful import Resource

from Src.common import status_code
from Src.common.constant import COMMENT_REQUIRED_FIELD
from Src.services.comment_service import CommentService
from Src.utils import check_utils
from Src.utils import log as logger
from Src.utils.decorator import write_operate_log, login_required


class CommentController(Resource):
    @staticmethod
    @write_operate_log(action_cn="获取评论", action_en="Get comment or list")
    @login_required
    def get(cid=None):
        if not check_utils.check_param_format(request.path, [r"^/v1/bms/comment/$", r"^/v1/bms/comment/([1-9][0-9]*)/$"]):
            return status_code.URL_ERROR
        data = request.json
        if not (data and isinstance(data, dict)):
            return status_code.JSON_PARAMS_ERROR
        if not data.get("article_id"):
            return {"code": status_code.REQUIRED_PARAM_CODE,
                    "msg_cn": status_code.REQUIRED_PARAM_MSG_CN.format("评论文章"),
                    "msg_en": status_code.REQUIRED_PARAM_MSG_EN.format("comment article")}
        try:
            comment_service = CommentService()
            result = []
            comment_list = comment_service.get_comment_by_article(article_id=data.get("article_id"))
            for comment in comment_list:
                sub_comment_list = comment_service.get_reply_by_comment(comment_id=comment.get("id"))
                result.append(comment)
        except Exception as ex:
            print(ex)
            logger.error("获取评论失败,{}".format(ex))
            return status_code.FAIL


    @staticmethod
    @write_operate_log(action_cn="创建评论", action_en="Create comment")
    @login_required
    def post(cid=None):
        if not check_utils.check_param_format(request.path, [r"^/v1/bms/comment/$"]):
            return status_code.URL_ERROR
        user_id = session.get("user_id")
        data = request.json
        if not (data and isinstance(data, dict)):
            return status_code.JSON_PARAMS_ERROR
        for k, v in COMMENT_REQUIRED_FIELD.items():
            if not data.get(k):
                return {"code": status_code.REQUIRED_PARAM_CODE,
                        "msg_cn": status_code.REQUIRED_PARAM_MSG_CN.format(v),
                        "msg_en": status_code.REQUIRED_PARAM_MSG_EN.format(k)}
        try:
            comment_service = CommentService()
            comment_service.create_comment(article_id=data.get("article_id"), article_type=data.get("article_type"),
                                           comment_con=data.get("comment_con"), comment_user=user_id,
                                           comment_id=data.get("comment_id"))
            return status_code.SUCCESS
        except Exception as ex:
            print(ex)
            logger.error("创建评论失败,{}".format(ex))
            return status_code.FAIL

    @staticmethod
    @write_operate_log(action_cn="修改评论", action_en="Update comment")
    @login_required
    def patch(cid=None):
        if not check_utils.check_param_format(request.path, [r"^/v1/bms/comment/([1-9][0-9]*)/$"]):
            return status_code.URL_ERROR
        user_id = session.get("user_id")
        data = request.json
        if not (data and isinstance(data, dict)):
            return status_code.JSON_PARAMS_ERROR
        if not data.get("comment_con"):
            return {"code": status_code.REQUIRED_PARAM_CODE,
                    "msg_cn": status_code.REQUIRED_PARAM_MSG_CN.format("评论内容"),
                    "msg_en": status_code.REQUIRED_PARAM_MSG_EN.format("comment content")}
        try:
             comment_service = CommentService()
             comment = comment_service.get_comment_by_id(comment_id=cid)
             if user_id != comment.get("comment_user"):
                 return status_code.COMMENT_NOT_BELONG_USER
             comment_service.update_comment(comment_id=cid, comment_con=data.get("comment_con"))
             return status_code.SUCCESS
        except Exception as ex:
            print(ex)
            logger.error("修改评论失败,{}".format(ex))
            return status_code.FAIL


    @staticmethod
    @write_operate_log(action_cn="删除评论", action_en="Delete comment")
    @login_required
    def delete(cid=None):
        if not check_utils.check_param_format(request.path, [r"^/v1/bms/comment/([1-9][0-9]*)/$"]):
            return status_code.URL_ERROR
        user_id = session.get("user_id")
        try:
             comment_service = CommentService()
             comment = comment_service.get_comment_by_id(comment_id=cid)
             if user_id != comment.get("comment_user"):
                 return status_code.COMMENT_NOT_BELONG_USER
             comment_service.delete_comment(comment_id_list=[cid])
             return status_code.SUCCESS
        except Exception as ex:
            print(ex)
            logger.error("修改评论失败,{}".format(ex))
            return status_code.FAIL
