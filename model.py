import json
from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, class_mapper
from werkzeug.security import check_password_hash

from Src.conf.config import DevelopConfig

engine = create_engine(DevelopConfig.SQLALCHEMY_DATABASE_URI, pool_size=100, pool_recycle=30)

Base = declarative_base(bind=engine)


def dict_to_obj(obj, data):
    """
    字典转化为对象的属性
    :param obj: 对象
    :param data: 数据
    :return:
    """

    for key in data:
        value = data.get(key)
        if isinstance(value, (list, dict)):
            value = json.dumps(value)
        setattr(obj, key, value)


def is_json(test_data):
    """
    判断是否能json化
    :param test_data: 测试数据
    :return:
    """
    try:
        json.loads(test_data)
    except Exception as ex:
        return False
    return True


def obj_to_dict(obj, wanted_keys=None, time_format=None):
    """
    转化字典
    :param obj: 对象
    :param wanted_keys: 需要序列化的字段列表 ['id', 'app_id'] 需要和模型中的字段对应好
    :param time_format: 时间格式化字符串
    :return: dict 序列化结果
    """

    res = {}
    model_keys = list(col.name for col in class_mapper(obj.__class__).mapped_table.c)
    for key in model_keys:
        value = getattr(obj, key)
        if isinstance(value, datetime) and time_format:
            value = value.strftime(time_format)
        if is_json(value):
            value = json.loads(value)
        res[key] = value
    for key in wanted_keys:
        if key not in model_keys:
            raise Exception("对象{}中不存在{}属性".format(obj, key))
    if wanted_keys:
        return {key: res[key] for key in wanted_keys}
    return res


class BaseModel(object):
    """
    基础model
    """

    create_time = Column(DateTime, default=datetime.now)  # 创建时间
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)  # 更新时间
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)  # 主键id
    is_delete = Column(Boolean, default=False)  # 是否删除

    def __init__(self, data_dict):
        """
        初始化对象，使用字典形式
        :param data_dict: 字典
        """

        dict_to_obj(self, data_dict)

    def to_dict(self, wanted_list):
        """
        obj转成dict
        :param wanted_list:
        :return:
        """

        return obj_to_dict(self, wanted_keys=wanted_list, time_format="%Y-%m-%d %X")


class UserInfo(BaseModel, Base):
    """
    用户信息
    """

    __tablename__ = "user_info"
    user_name = Column(String(32))  # 用户名
    user_account = Column(String(16), nullable=False)  # 用户账号
    password = Column(String(256), nullable=False)  # 用户密码
    gender = Column(Boolean, default=True)  # 性别
    phone = Column(String(12), nullable=False)  # 电话
    email = Column(String(64))  # 邮箱
    birth = Column(DateTime)  # 出生日期
    is_active = Column(Boolean, default=True)  # 是否激活
    token = Column(String(128))  # 口令

    logs = relationship("LogInfo", backref="user", lazy=True)
    essays = relationship("Essay", backref="user", lazy=True)
    comments = relationship("Comment", backref="user", lazy=True)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class LogInfo(BaseModel, Base):
    """
    日志信息
    """

    __tablename__ = "log_info"
    user_id = Column(Integer, ForeignKey("user_info.id"))  # 外键id
    client_ip = Column(String(16), nullable=False)  # 客户端IP
    action_cn = Column(String(60), nullable=False)  # 操作对象中文
    action_en = Column(String(120), nullable=False)  # 操作对象英文
    result_cn = Column(String(12), nullable=False)  # 结果中文
    result_en = Column(String(12), nullable=False)  # 结果英文
    reason_cn = Column(String(256))  # 失败原因中文
    reason_en = Column(String(256))  # 失败原因英文


class Essay(BaseModel, Base):
    """
    随笔
    """

    __tablename__ = "essay"
    user_id = Column(Integer, ForeignKey("user_info.id"), nullable=False)  # 外键id
    title = Column(String(120), nullable=False)  # 标题
    abstract = Column(Text)  # 摘要
    content = Column(Text, nullable=False)  # 随笔内容
    status = Column(Integer, default=1)  # 状态
    zan_times = Column(Integer, default=0)  # 点赞数


class Comment(BaseModel, Base):
    """
    评论
    """

    __tablename__ = "comment"
    article_id = Column(Integer, nullable=False)  # 其他表外键id
    article_type = Column(String(16), nullable=False)  # 评论的种类
    comment_con = Column(Text, nullable=False)  # 评论内容
    comment_id = Column(Integer)  # 自关联外键id
    comment_user = Column(Integer, ForeignKey("user_info.id"), nullable=False)  # 用户表外键id


Base.metadata.create_all(engine)
