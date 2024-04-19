from datetime import date, datetime
import redis
import json

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.model import pydantic_post, pydantic_comment, sql_models

db = redis.Redis(host="localhost", port=6379, decode_responses=True)


def type_or_none(number: str, type: callable) -> int | None:
    if number.isdigit():
        return type(number)
    return None


class DataBaseConn:
    def __init__(self, db_uri):
        self.engine = create_engine(db_uri, echo=True)
        self.session = Session(self.engine)
        self.conn = self.engine.connect()

    def get_posts(self, page_size=100, page_nr=0) -> list[pydantic_post.Post]:
        ggh = self.session.query(sql_models.Post)
        ggh = ggh.limit(page_size)
        ggh = ggh.offset(page_size * page_nr)

        return [post.to_pydantic() for post in ggh.all()]

    def get_posts_by_date(
        self, start_date: str, end_date: str
    ) -> list[pydantic_post.Post]:
        start_date_datetime = datetime(*map(int, start_date.split("-")))
        end_date_datetime = datetime(*map(int, end_date.split("-")))

        start_epoch = int(start_date_datetime.timestamp())
        end_epoch = int(end_date_datetime.timestamp())
        posts = self.session.query(sql_models.Post).filter(
            sql_models.Post.created_utc.between(start_epoch, end_epoch)
        )
        if len(posts.all()) == 1 and type(posts.all()[0]) is None:
            return []
        return [post.to_pydantic() for post in posts.all()]

    def get_posts_by_keyword(
        self, keywords: list[str]
    ) -> tuple[list[pydantic_post.Post], dict]:
        id = []
        weight = {}
        for word in keywords:
            try:
                keywod_ids = json.loads(db.get(word))
                weight[word] = len(keywod_ids)
                id = id + keywod_ids
            except TypeError:
                pass

        posts = self.session.query(sql_models.Post).filter(sql_models.Post.id.in_(id))
        if len(posts.all()) == 1 and type(posts.all()[0]) == None:
            return []
        return [post.to_pydantic() for post in posts.all()], weight

    def get_post(self, post_id: str) -> pydantic_post.Post:
        # smt = select(sql_models.Post).where(sql_models.Post.id.is_(post_id))
        return (
            self.session.query(sql_models.Post)
            .filter(sql_models.Post.id == post_id)
            .first()
            .to_pydantic()
        )

    def get_comments(self, page_size=100, page_nr=0) -> pydantic_post.Post:
        comments = self.session.query(sql_models.Comment)
        comments = comments.limit(page_size)
        comments = comments.offset(page_size * page_nr)

        return [comment.to_pydantic() for comment in comments.all()]

    def get_comments_by_date(
        self, start_date: str, end_date: str
    ) -> list[pydantic_comment.Comment]:
        start_date_datetime = datetime(*map(int, start_date.split("-")))
        end_date_datetime = datetime(*map(int, end_date.split("-")))

        start_epoch = int(start_date_datetime.timestamp())
        end_epoch = int(end_date_datetime.timestamp())
        comments = self.session.query(sql_models.Comment).filter(
            sql_models.Comment.created_utc.between(start_epoch, end_epoch)
        )
        if len(comments.all()) == 1 and type(comments.all()[0]) is None:
            return []
        return [comment.to_pydantic() for comment in comments.all()]

    def get_comments_by_keyword(
        self, keywords: list[str]
    ) -> list[pydantic_comment.Comment]:
        id = []
        weight = {}
        for word in keywords:
            try:
                keywod_ids = json.loads(db.get(word))
                weight[word] = len(keywod_ids)
                id = id + keywod_ids
            except TypeError:
                pass

        comments = self.session.query(sql_models.Comment).filter(
            sql_models.Comment.id.in_(id)
        )
        if len(comments.all()) == 1 and type(comments.all()[0]) is None:
            return []
        return [comment.to_pydantic() for comment in comments.all()], weight

    def get_comment(self, comment_id: str) -> pydantic_comment.Comment:
        return (
            self.session.query(sql_models.Comment)
            .filter(sql_models.Comment.id == comment_id)
            .first()
            .to_pydantic()
        )

    def get_comments_by_post(
        self, post: pydantic_post.Post
    ) -> list[pydantic_comment.Comment]:
        comments = self.session.query(sql_models.Comment).filter(
            sql_models.Comment.linked_submission_id == post.id
        )

        if len(comments.all()) == 1 and type(comments.all()[0]) is None:
            return []
        return [comment.to_pydantic() for comment in comments.all()]
