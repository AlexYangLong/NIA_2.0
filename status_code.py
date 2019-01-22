# 公共
SUCCESS = {"code": 601, "msg_cn": "操作成功", "msg_en": "Operate successful."}
SUCCESS_CODE = 601

FAIL = {"code": 602, "msg_cn": "操作失败,请重试", "msg_en": "Operate failed."}
FAIL_CODE = 602

REQUIRED_PARAM_CODE = 603
REQUIRED_PARAM_MSG_CN = "请求参数{}不能为空"
REQUIRED_PARAM_MSG_EN = "Request parameter {} can not be empty."

URL_ERROR = {"code": 604, "msg_cn": "请求路径或方式错误", "msg_en": "Request path or method error."}

JSON_PARAMS_ERROR = {"code": 605, "msg_cn": "JSON请求参数错误", "msg_en": "JSON request parameter error."}
ARGS_PARAMS_ERROR = {"code": 606, "msg_cn": "ARGS请求参数错误", "msg_en": "ARGS request parameter error."}

USER_NO_LOGIN = {"code": 607, "msg_cn": "用户未登录", "msg_en": "Users are not logged in."}
PLEASE_LOGIN = {"code": 608, "msg_cn": "请先登录", "msg_en": "Please login first."}

# 用户相关
USER_ERROR = {"code": 1001, "msg_cn": "帐号或密码错误", "msg_en": "Account or password error."}
USER_NOT_EXIST = {"code": 1002, "msg_cn": "用户不存在", "msg_en": "User is not existed."}
USER_ACCOUNT_EXIST = {"code": 1003, "msg_cn": "帐户名已存在", "msg_en": "User account is already existed."}
PASSWORD_ERROR = {"code": 1004, "msg_cn": "密码错误", "msg_en": "Password error."}
USER_IS_NOT_ACTIVE = {"code": 1005, "msg_cn": "用户未激活,请联系管理员", "msg_en": "User is not active."}
ACTIVE_NOT_BOOL = {"code": 1006, "msg_cn": "激活状态参数不是一个布尔值", "msg_en": "The activation state parameter is not a Boolean value."}

# 随笔相关
ESSAY_NOT_EXIST = {"code": 1101, "msg_cn": "随笔不存在", "msg_en": "Essay is not existed."}
ESSAY_STATUS_NOT_INT = {"code": 1102, "msg_cn": "随笔状态值不是整数", "msg_en": "Essay status is not integer."}
ESSAY_STATUS_OUT_RANGE = {"code": 1103, "msg_cn": "随笔状态值超出范围", "msg_en": "Essay status is out of range."}

# 评论相关
COMMENT_NOT_BELONG_USER = {"code": 1201, "msg_cn": "评论不属于该用户", "msg_en": "Comment don't belong this user."}

