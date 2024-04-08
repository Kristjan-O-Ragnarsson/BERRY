from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.model import pydantic_post, pydantic_comment

import datetime


class Base(DeclarativeBase):
    pass


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    author: Mapped[str]
    clean_title: Mapped[str]
    domain: Mapped[str]
    has_image: Mapped[bool]
    created_utc: Mapped[float]
    img_url: Mapped[str]
    score: Mapped[int]
    subreddit: Mapped[str]
    title: Mapped[str]
    upvote_ratio: Mapped[Optional[float]]
    nr_of_comments: Mapped[Optional[int]]
    unnamed_0: Mapped[Optional[int]]
    unnamed_0_1: Mapped[Optional[int]]
    unnamed_0_1_1: Mapped[Optional[int]]
    n2_way_lable: Mapped[Optional[int]]
    n3_way_lable: Mapped[Optional[int]]
    n6_way_lable: Mapped[Optional[int]]
    linked_submission_id: Mapped[str]
    # comments: Mapped[set["Comment"]] = relationship(back_populates="posts")

    def to_pydantic(self) -> pydantic_post.Post:
        return pydantic_post.Post(
            unnamed0=self.unnamed_0,
            unnamed01=self.unnamed_0_1,
            unnamed011=self.unnamed_0_1_1,
            author=self.author,
            clean_title=self.clean_title,
            created_utc=self.created_utc,
            domain=self.domain,
            hasImage=self.has_image,
            id=self.id,
            image_url=self.img_url,
            linked_submission_id=self.linked_submission_id,
            num_comments=self.nr_of_comments,
            score=self.score,
            subreddit=self.subreddit,
            title=self.title,
            upvote_ratio=self.upvote_ratio,
            n2_way_label=self.n2_way_lable,
            n3_way_label=self.n3_way_lable,
            n6_way_label=self.n6_way_lable,
        )


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    author: Mapped[str]
    clean_title: Mapped[str]
    domain: Mapped[str]
    has_image: Mapped[bool]
    created_utc: Mapped[float]
    img_url: Mapped[str]
    score: Mapped[int]
    subreddit: Mapped[str]
    title: Mapped[str]
    upvote_ratio: Mapped[Optional[float]]
    nr_of_comments: Mapped[Optional[int]]
    unnamed_0: Mapped[Optional[int]]
    unnamed_0_1: Mapped[Optional[int]]
    unnamed_0_1_1: Mapped[Optional[int]]
    n2_way_lable: Mapped[Optional[int]]
    n3_way_lable: Mapped[Optional[int]]
    n6_way_lable: Mapped[Optional[int]]
    linked_submission_id: Mapped[str]

    def to_pydantic(self) -> pydantic_comment.Comment:
        return pydantic_comment.Comment(
            unnamed0=self.unnamed_0,
            unnamed01=self.unnamed_0_1,
            unnamed011=self.unnamed_0_1_1,
            author=self.author,
            clean_title=self.clean_title,
            created_utc=self.created_utc,
            domain=self.domain,
            hasImage=self.has_image,
            id=self.id,
            image_url=self.img_url,
            linked_submission_id=self.linked_submission_id,
            num_comments=self.nr_of_comments,
            score=self.score,
            subreddit=self.subreddit,
            title=self.title,
            upvote_ratio=self.upvote_ratio,
            n2_way_label=self.n2_way_lable,
            n3_way_label=self.n3_way_lable,
            n6_way_label=self.n6_way_lable,
        )
