import csv
import pydantic


import datetime
import redis

# r = redis.Redis(host='localhost', port=6379, decode_responses=True)

from fastapi import APIRouter, HTTPException, Request
from fastui import AnyComponent, FastUI
from fastui import components as c
from fastui.components.display import DisplayLookup, DisplayMode
from fastui.events import BackEvent, GoToEvent
from pydantic import TypeAdapter

from app.model.pydantic_post import Post
from app.data.service import DataBaseConn


router = APIRouter()


db = DataBaseConn("postgresql://berry_user:S3cret@localhost:5432/berry_db")


@router.get(
    "/api/posts/date/",
    tags=["posts"],
    response_model=FastUI,
    response_model_exclude_none=True,
)
def read_all_date(start_date: str, end_date: str, select_single: str):
    # print(start_date)
    if select_single == "Posts":
        posts = db.get_posts_by_date(start_date, end_date)
        if len(posts) < 1:
            return [
                c.PageTitle(text=f"TEST"),
                c.Navbar(
                    title="BERRY",
                    title_event=GoToEvent(url="/"),
                    start_links=[
                        c.Link(
                            components=[c.Text(text="Date")],
                            on_click=GoToEvent(url="/forms/date"),
                            active="startswith:/forms/date",
                        ),
                        c.Link(
                            components=[c.Text(text="Keyword")],
                            on_click=GoToEvent(url="/forms/keyword"),
                            active="startswith:/forms/keyword",
                        ),
                    ],
                ),
                c.Page(
                    components=[
                        c.Heading(text="Posts", level=2),
                        c.Text(text="no data found"),
                    ]
                ),
            ]
        else:
            return [
                c.PageTitle(text=f"TEST"),
                c.Navbar(
                    title="BERRY",
                    title_event=GoToEvent(url="/"),
                    start_links=[
                        c.Link(
                            components=[c.Text(text="Date")],
                            on_click=GoToEvent(url="/forms/date"),
                            active="startswith:/forms/date",
                        ),
                        c.Link(
                            components=[c.Text(text="Keyword")],
                            on_click=GoToEvent(url="/forms/keyword"),
                            active="startswith:/forms/keyword",
                        ),
                    ],
                ),
                c.Page(
                    components=[
                        c.Heading(text="Posts", level=2),
                        c.Table(
                            data=posts,
                            columns=[
                                DisplayLookup(
                                    field="id",
                                    on_click=GoToEvent(url="/posts/{id}"),
                                    table_width_percent=10,
                                ),
                                DisplayLookup(field="title", table_width_percent=33),
                                DisplayLookup(field="author", table_width_percent=33),
                            ],
                        ),
                    ],
                ),
            ]

    elif select_single == "Comments":
        comments = db.get_comments_by_date(start_date, end_date)
        if len(comments) < 1:
            return [
                c.PageTitle(text=f"Comments Date Search"),
                c.Navbar(
                    title="BERRY",
                    title_event=GoToEvent(url="/"),
                    start_links=[
                        c.Link(
                            components=[c.Text(text="Date")],
                            on_click=GoToEvent(url="/forms/date"),
                            active="startswith:/forms/date",
                        ),
                        c.Link(
                            components=[c.Text(text="Keyword")],
                            on_click=GoToEvent(url="/forms/keyword"),
                            active="startswith:/forms/keyword",
                        ),
                    ],
                ),
                c.Page(
                    components=[
                        c.Heading(text="Comments", level=2),
                        c.Text(text="no data found"),
                    ]
                ),
            ]
        else:
            return [
                c.PageTitle(text=f"TEST"),
                c.Navbar(
                    title="BERRY",
                    title_event=GoToEvent(url="/"),
                    start_links=[
                        c.Link(
                            components=[c.Text(text="Date")],
                            on_click=GoToEvent(url="/forms/date"),
                            active="startswith:/forms/date",
                        ),
                        c.Link(
                            components=[c.Text(text="Keyword")],
                            on_click=GoToEvent(url="/forms/keyword"),
                            active="startswith:/forms/keyword",
                        ),
                    ],
                ),
                c.Page(
                    components=[
                        c.Heading(text="Comments", level=2),
                        c.Table(
                            data=comments,
                            columns=[
                                DisplayLookup(
                                    field="id",
                                    on_click=GoToEvent(url="/comments/{id}"),
                                    table_width_percent=10,
                                ),
                                DisplayLookup(field="title", table_width_percent=33),
                                DisplayLookup(field="author", table_width_percent=33),
                            ],
                        ),
                    ],
                ),
            ]
    elif select_single == "Both":
        elements = []
        posts = db.get_posts_by_date(start_date, end_date)
        # comments = db.get_comments_by_date(start_date, end_date)
        for post in posts:
            elements.append(
                c.Link(
                    components=[c.Text(text=f"{post.id}\n")],
                    on_click=GoToEvent(url=f"/posts/{post.id}"),
                )
            )
            comments = db.get_comments_by_post(post)
            for comment in comments:
                elements.append(
                    c.Link(
                        components=[c.Text(text=f"↳ {comment.id}")],
                        on_click=GoToEvent(url=f"/comments/{comment.id}"),
                    )
                )
            print(f"/posts/{post.id}")

    return [
        c.PageTitle(text=f"Comments & Post Date Search"),
        c.Navbar(
            title="BERRY",
            title_event=GoToEvent(url="/"),
            start_links=[
                c.Link(
                    components=[c.Text(text="Date")],
                    on_click=GoToEvent(url="/forms/date"),
                    active="startswith:/forms/date",
                ),
                c.Link(
                    components=[c.Text(text="Keyword")],
                    on_click=GoToEvent(url="/forms/keyword"),
                    active="startswith:/forms/keyword",
                ),
            ],
        ),
        c.Page(
            components=[
                c.Heading(text="Posts & Comments", level=2),
                c.LinkList(links=elements),
            ]
        ),
    ]


@router.get(
    "/api/posts/keyword/",
    tags=["posts"],
    response_model=FastUI,
    response_model_exclude_none=True,
)
def read_all_keyword(keyword: str, select_single: str):
    if select_single == "Posts":
        posts, weight = db.get_posts_by_keyword(keyword.split())
        hits = ""
        for i in weight.keys():
            hits += f"{i}: {weight[i]}, "
        if len(posts) < 1:
            return [
                c.PageTitle(text=f"TEST"),
                c.Navbar(
                    title="BERRY",
                    title_event=GoToEvent(url="/"),
                    start_links=[
                        c.Link(
                            components=[c.Text(text="Date")],
                            on_click=GoToEvent(url="/forms/date"),
                            active="startswith:/forms/date",
                        ),
                        c.Link(
                            components=[c.Text(text="Keyword")],
                            on_click=GoToEvent(url="/forms/keyword"),
                            active="startswith:/forms/keyword",
                        ),
                    ],
                ),
                c.Page(
                    components=[
                        c.Heading(text="Posts", level=2),
                        c.Text(text="no data found"),
                    ]
                ),
            ]
        else:
            return [
                c.PageTitle(text=f"TEST"),
                c.Navbar(
                    title="BERRY",
                    title_event=GoToEvent(url="/"),
                    start_links=[
                        c.Link(
                            components=[c.Text(text="Date")],
                            on_click=GoToEvent(url="/forms/date"),
                            active="startswith:/forms/date",
                        ),
                        c.Link(
                            components=[c.Text(text="Keyword")],
                            on_click=GoToEvent(url="/forms/keyword"),
                            active="startswith:/forms/keyword",
                        ),
                    ],
                ),
                c.Page(
                    components=[
                        c.Heading(text="Posts", level=2),
                        c.Text(text=hits),
                        c.Table(
                            data=posts,
                            columns=[
                                DisplayLookup(
                                    field="id",
                                    on_click=GoToEvent(url="/posts/{id}"),
                                    table_width_percent=10,
                                ),
                                DisplayLookup(field="title", table_width_percent=33),
                                DisplayLookup(field="author", table_width_percent=33),
                            ],
                        ),
                    ],
                ),
            ]

    elif select_single == "Comments":
        comments, weight = db.get_comments_by_keyword(keyword.split())
        hits = ""
        for i in weight.keys():
            hits += f"{i}: {weight[i]}, "
        if len(comments) < 1:
            return [
                c.PageTitle(text=f"Comments Date Search"),
                c.Navbar(
                    title="BERRY",
                    title_event=GoToEvent(url="/"),
                    start_links=[
                        c.Link(
                            components=[c.Text(text="Date")],
                            on_click=GoToEvent(url="/forms/date"),
                            active="startswith:/forms/date",
                        ),
                        c.Link(
                            components=[c.Text(text="Keyword")],
                            on_click=GoToEvent(url="/forms/keyword"),
                            active="startswith:/forms/keyword",
                        ),
                    ],
                ),
                c.Page(
                    components=[
                        c.Heading(text="Comments", level=2),
                        c.Text(text="no data found"),
                    ]
                ),
            ]
        else:
            return [
                c.PageTitle(text=f"TEST"),
                c.Navbar(
                    title="BERRY",
                    title_event=GoToEvent(url="/"),
                    start_links=[
                        c.Link(
                            components=[c.Text(text="Date")],
                            on_click=GoToEvent(url="/forms/date"),
                            active="startswith:/forms/date",
                        ),
                        c.Link(
                            components=[c.Text(text="Keyword")],
                            on_click=GoToEvent(url="/forms/keyword"),
                            active="startswith:/forms/keyword",
                        ),
                    ],
                ),
                c.Page(
                    components=[
                        c.Heading(text="Comments", level=2),
                        c.Text(text=hits),
                        c.Table(
                            data=comments,
                            columns=[
                                DisplayLookup(
                                    field="id",
                                    on_click=GoToEvent(url="/comments/{id}"),
                                    table_width_percent=10,
                                ),
                                DisplayLookup(field="title", table_width_percent=33),
                                DisplayLookup(field="author", table_width_percent=33),
                            ],
                        ),
                    ],
                ),
            ]

    elif select_single == "Both":
        elements = []
        posts, weight = db.get_posts_by_keyword(keywords=keyword.split())
        # comments = db.get_comments_by_date(start_date, end_date)
        for post in posts:
            elements.append(
                c.Link(
                    components=[c.Text(text=f"{post.id}\n")],
                    on_click=GoToEvent(url=f"/posts/{post.id}"),
                )
            )
            comments = db.get_comments_by_post(post)
            for comment in comments:
                elements.append(
                    c.Link(
                        components=[c.Text(text=f"↳ {comment.id}")],
                        on_click=GoToEvent(url=f"/comments/{comment.id}"),
                    )
                )
            print(f"/posts/{post.id}")

    return [
        c.PageTitle(text=f"Comments & Date Search"),
        c.Navbar(
            title="BERRY",
            title_event=GoToEvent(url="/"),
            start_links=[
                c.Link(
                    components=[c.Text(text="Date")],
                    on_click=GoToEvent(url="/forms/date"),
                    active="startswith:/forms/date",
                ),
                c.Link(
                    components=[c.Text(text="Keyword")],
                    on_click=GoToEvent(url="/forms/keyword"),
                    active="startswith:/forms/keyword",
                ),
            ],
        ),
        c.Page(
            components=[
                c.Heading(text="Posts & Comments", level=2),
                c.LinkList(links=elements),
            ]
        ),
    ]


@router.get(
    "/api/comments/{comment_id}",
    tags=["posts"],
    response_model=FastUI,
    response_model_exclude_none=True,
)
def read_comment_by_id(comment_id: str) -> list[AnyComponent]:
    comment = db.get_comment(comment_id)
    if comment.image_url != "":
        return [
            c.PageTitle(text=f"comment: {comment.id}"),
            c.Page(
                components=[
                    c.Heading(text="Comment"),
                    c.Link(components=[c.Text(text="Back")], on_click=BackEvent()),
                    c.Heading(
                        text=f"Comment ID: {comment.id}, Author: {comment.author}",
                        level=3,
                    ),
                    c.Heading(text=f"Title: {comment.title}", level=3),
                    c.Link(
                        components=[
                            c.Heading(text=f"{comment.linked_submission_id}", level=5)
                        ],
                        on_click=GoToEvent(
                            url=f"/posts/{comment.linked_submission_id}"
                        ),
                    ),
                    c.Image(src=comment.image_url, loading="lazy", width=500),
                    c.Table(
                        data=[comment],
                        columns=[
                            DisplayLookup(field="unnamed0", table_width_percent=15),
                            DisplayLookup(field="unnamed01", table_width_percent=15),
                            DisplayLookup(field="unnamed011", table_width_percent=15),
                            DisplayLookup(field="n2_way_label", table_width_percent=15),
                            DisplayLookup(field="n3_way_label", table_width_percent=15),
                            DisplayLookup(field="n6_way_label", table_width_percent=15),
                        ],
                    ),
                    c.Details(
                        data=comment,
                    ),
                ]
            ),
        ]

    return [
        c.PageTitle(text=f"comment: {comment.id}"),
        c.Page(
            components=[
                c.Heading(text=comment.id),
                c.Link(components=[c.Text(text="Back")], on_click=BackEvent()),
                c.Details(data=comment),
            ]
        ),
    ]


@router.get(
    "/api/posts/{post_id}",
    tags=["posts"],
    response_model=FastUI,
    response_model_exclude_none=True,
)
def read_post_by_id(post_id: str) -> list[AnyComponent]:
    print(post_id)
    try:
        print(post_id)
        post = db.get_post(post_id)

        # post = post.to_pydantic()
    except KeyError:
        print(post_id)
        raise HTTPException(status_code=404, detail="Post not found")

    if post.image_url != "":
        return [
            c.PageTitle(text=f"post: {post.id}"),
            c.Page(
                components=[
                    c.Heading(text=post.id),
                    c.Link(components=[c.Text(text="Back")], on_click=BackEvent()),
                    c.Image(src=post.image_url, loading="lazy"),
                    c.Details(data=post),
                ]
            ),
        ]

    return [
        c.PageTitle(text=f"post: {post.id}"),
        c.Page(
            components=[
                c.Heading(text=post.id),
                c.Link(components=[c.Text(text="Back")], on_click=BackEvent()),
                c.Details(data=post),
            ]
        ),
    ]


@router.get(
    "/api/posts/",
    tags=["posts"],
    response_model=FastUI,
    response_model_exclude_none=True,
)
def read_all_posts(
    request: Request,
    page: int = 0,
    page_size: int = 50,
    form: str | None = None,
    start_date: int | None = None,
    end_date: int | None = None,
    keywords: list[str] | None = None,
) -> list[AnyComponent]:
    print(form)
    if form == "date":
        assert type(start_date) is int
        assert type(end_date) is int
        posts = db.get_posts_by_date(start_date, end_date)
    if form == "keyword":
        assert type(keywords) is list
        assert len(keywords) >= 1
        posts = db.get_posts_by_keyword(keywords)
    else:
        posts = db.get_posts(page_size=page_size, page_nr=page)

    return [
        c.PageTitle(text=f"TEST"),
        c.Page(
            components=[
                c.Heading(text="Posts", level=2),
                c.Table(
                    data=posts,
                    columns=[
                        DisplayLookup(
                            field="id",
                            on_click=GoToEvent(url="./{id}"),
                            table_width_percent=10,
                        ),
                        DisplayLookup(field="title", table_width_percent=33),
                        DisplayLookup(field="author", table_width_percent=33),
                    ],
                ),
            ],
        ),
    ]
