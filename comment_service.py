from Src.common.model import Comment
from Src.common.service import session_scope


class CommentService(object):

    def create_comment(self, article_id, article_type, comment_con, comment_user, comment_id=None):
        comment = Comment({
            "article_id": article_id,
            "article_type": article_type,
            "comment_con": comment_con,
            "comment_user": comment_user,
            "comment_id": comment_id
        })
        with session_scope() as session:
            session.add(comment)

    def update_comment(self, comment_id, comment_con):
        with session_scope() as session:
            comment = session.query(Comment).filter(Comment.id == comment_id).first()
            comment.comment_con = comment_con
            session.add(comment)

    def delete_comment(self, comment_id_list=None):
        if not comment_id_list:
            raise Exception("评论id列表不能为None")
        if not isinstance(comment_id_list, list):
            raise Exception("评论id参数不是一个列表")
        with session_scope() as session:
            comment_list = session.query(Comment).filter(Comment.id.in_(comment_id_list))
            for comment in comment_list:
                comment.is_delete = True
                session.add(comment)

    def get_comment_by_article(self, article_id):
        with session_scope() as session:
            comment_list = session.query(Comment).filter(Comment.article_id == article_id)
            if not list(comment_list):
                return None
            return [comment.to_dict(wanted_list=["id", "comment_con", "comment_id", "comment_user", "create_time"]) for comment in comment_list]

    def get_comment_by_id(self, comment_id):
        with session_scope() as session:
            comment = session.query(Comment).filter(Comment.id == comment_id).first()
            if not comment:
                return None
            return comment.to_dict(wanted_list=["id", "comment_con", "comment_id", "comment_user", "create_time"])

    def get_reply_by_comment(self, comment_id):
        with session_scope() as session:
            comment_list = session.query(Comment).filter(Comment.comment_id == comment_id)
            if not list(comment_list):
                return None
            return [comment.to_dict(wanted_list=["id", "comment_con", "comment_id", "comment_user", "create_time"]) for comment in comment_list]
