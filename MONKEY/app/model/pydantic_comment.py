from pydantic import BaseModel, Field


class Comment(BaseModel):
    unnamed0: int = Field(title="Unnamed: 0")
    unnamed01: int | None = Field(title="Unnamed: 0.1")
    unnamed011: int | None = Field(title="Unnamed: 0.1.1")
    author: str = Field(title="Author")
    clean_title: str = Field(title="Clean title")
    created_utc: int = Field(title="Created UTC")
    domain: str = Field(title="Domain")
    hasImage: bool = Field(title="has image")
    id: str = Field(title="ID")
    image_url: str = Field(title="image url")
    linked_submission_id: str = Field(title="linked submission id")
    num_comments: int | None = Field(title="Number of comments")
    score: int = Field(title="Score")
    subreddit: str = Field(title="Subreddit")
    title: str = Field(title="Title")
    upvote_ratio: float | None = Field(title="Upvote ratio")
    n2_way_label: int = Field(title="2 way label")
    n3_way_label: int = Field(title="3 way label")
    n6_way_label: int = Field(title="6 way label")
