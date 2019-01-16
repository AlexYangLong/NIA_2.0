from Src.common.model import Essay
from Src.common.service import session_scope


class EssayService(object):

    def create_essay(self, user_id, title, abstract, content, status):
        essay = Essay({
            "user_id": user_id,
            "title": title,
            "abstract": abstract,
            "content": content,
            "status": status,
        })
        with session_scope() as session:
            session.add(essay)

    def delete_essay(self, essay_id_list=None):
        if not essay_id_list:
            raise Exception("随笔id列表不能为None")
        if not isinstance(essay_id_list, list):
            raise Exception("随笔id参数不是一个列表")
        with session_scope() as session:
            essay_list = session.query(Essay).filter(Essay.id.in_(essay_id_list))
            for essay in essay_list:
                essay.is_delete = True
                session.add(essay)

    def update_essay(self, essay_id, title, abstract, content, status):
        with session_scope() as session:
            essay = session.query(Essay).filter(Essay.id == essay_id).first()
            essay.title = title
            essay.abstract = abstract
            essay.content = content
            essay.status = status
            session.add(essay)

    def get_essay_by_id(self, essay_id):
        with session_scope() as session:
            essay = session.query(Essay).filter(Essay.id == essay_id).first()
            if not essay:
                return None
            return essay.to_dict(wanted_list=["id", "user_id", "title", "abstract", "content", "status"])

    def get_all_essay(self, user_id=None):
        with session_scope() as session:
            if not user_id:
                essay_list = session.query(Essay)
            else:
                essay_list = session.query(Essay).filter(Essay.user_id == user_id)
            return [essay.to_dict(wanted_list=["id", "user_id", "title", "abstract", "content", "status"]) for essay in essay_list]

    def get_essay_by_title(self, title=None):
        with session_scope() as session:
            if not title:
                essay_list = session.query(Essay)
            else:
                essay_list = session.query(Essay).filter(Essay.title.like("%{}%".format(title)))
            return [essay.to_dict(wanted_list=["id", "user_id", "title", "abstract", "content", "status"]) for essay in essay_list]

