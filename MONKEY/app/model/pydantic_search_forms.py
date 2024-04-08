import enum
from pydantic import BaseModel, Field
from datetime import date


class CommentPostEnum(str, enum.Enum):
    comment = "Comments"
    post = "Posts"
    both = "Both"


class SearchByDate(BaseModel):
    start_date: date = Field(title="Start date")
    end_date: date = Field(title="End date")
    select_single: CommentPostEnum = Field(title="Search posts and/or comments")


class SearchByKeyword(BaseModel):
    keyword: str = Field(title="Keywords")
    select_single: CommentPostEnum = Field(title="Search posts and/or comments")
