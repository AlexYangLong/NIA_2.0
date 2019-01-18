import uuid

from werkzeug.security import generate_password_hash

from Src.common.model import UserInfo
from Src.common.service import session_scope


class UserService(object):

    def create_user(self, account, password, phone, username=None, gender=True, email=None, birth=None, is_active=True):
        token = uuid.uuid1().hex
        password = generate_password_hash(password)
        user = UserInfo({
            "user_name": username,
            "user_account": account,
            "password": password,
            "gender": gender,
            "phone": phone,
            "email": email,
            "birth": birth,
            "token": token,
            "is_active": is_active
        })
        with session_scope() as session:
            session.add(user)

    def delete_user(self, user_id_list=None):
        if not user_id_list:
            raise Exception("用户id列表不能为None")
        if not isinstance(user_id_list, list):
            raise Exception("用户id参数不是一个列表")
        with session_scope() as session:
            user_list = session.query(UserInfo).filter(UserInfo.id.in_(user_id_list))
            for user in user_list:
                user.is_delete = True
                session.add(user)

    def update_user_basic(self, user_id, phone, username=None, gender=True, email=None, birth=None):
        with session_scope() as session:
            user = session.query(UserInfo).filter(UserInfo.id == user_id).first()
            user.phone = phone
            user.user_name = username
            user.gender = gender
            user.email = email
            user.birth = birth
            session.add(user)

    def update_user_password(self, user_id, new_password):
        password = generate_password_hash(new_password)
        with session_scope() as session:
            user = session.query(UserInfo).filter(UserInfo.id == user_id).first()
            user.password = password
            session.add(user)

    def change_user_status(self, is_active, user_id_list=None):
        if not user_id_list:
            raise Exception("用户id列表不能为None")
        if not isinstance(user_id_list, list):
            raise Exception("用户id参数不是一个列表")
        if not isinstance(is_active, bool):
            raise Exception("用户激活参数不是一个布尔值")
        with session_scope() as session:
            user_list = session.query(UserInfo).filter(UserInfo.id.in_(user_id_list))
            for user in user_list:
                user.is_active = is_active
                session.add(user)

    def change_user_token(self, user_id):
        new_token = uuid.uuid1().hex
        with session_scope() as session:
            user = session.query(UserInfo).filter(UserInfo.id == user_id).first()
            user.token = new_token
            return new_token

    def get_user_by_id(self, user_id):
        with session_scope() as session:
            user = session.query(UserInfo).filter(UserInfo.id == user_id).first()
            if not user:
                 return None
            return user.to_dict(wanted_list=["id", "user_name", "user_account", "gender", "phone", "email", "birth", "is_active", "token"])

    def get_user_by_token(self, token):
        with session_scope() as session:
            user = session.query(UserInfo).filter(UserInfo.token == token).first()
            if not user:
                 return None
            return user.to_dict(wanted_list=["id", "user_name", "user_account", "gender", "phone", "email", "birth", "is_active", "token"])

    def get_user_by_account(self, account):
        with session_scope() as session:
            user = session.query(UserInfo).filter(UserInfo.user_account == account).first()
            if not user:
                 return None
            return user.to_dict(wanted_list=["id", "user_name", "user_account", "gender", "phone", "email", "birth", "is_active", "token"])

    def get_users(self):
        with session_scope() as session:
            users = session.query(UserInfo).all()
            return [user.to_dict(wanted_list=["id", "user_name", "user_account", "gender", "phone", "email", "birth", "is_active", "token"]) for user in users]

    def check_user_password(self, user_id, password):
        with session_scope() as session:
            user = session.query(UserInfo).filter(UserInfo.id == user_id).first()
            return user.check_password(password=password)

    def get_user_active(self, user_id):
        with session_scope() as session:
            user = session.query(UserInfo).filter(UserInfo.id == user_id).first()
            return user.is_active
