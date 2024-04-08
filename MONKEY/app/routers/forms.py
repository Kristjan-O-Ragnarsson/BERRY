from fastapi import APIRouter, HTTPException, Form
from fastapi.responses import RedirectResponse
from fastui import AnyComponent, FastUI
from fastui import components as c
from fastui.components.display import DisplayLookup, DisplayMode
from fastui.events import BackEvent, GoToEvent


from app.model.pydantic_search_forms import (
    SearchByDate,
    SearchByKeyword,
    CommentPostEnum,
)
from app.data.service import DataBaseConn

from typing import Annotated
from datetime import date, datetime


db = DataBaseConn("postgresql://berry_user:S3cret@localhost:5432/berry_db")


router = APIRouter()


@router.get(
    "/api/forms/date",
    tags=["forms"],
    response_model=FastUI,
    response_model_exclude_none=True,
)
def search_by_date_form() -> list[AnyComponent]:
    return [
        c.PageTitle(text=f"Search"),
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
                c.ModelForm(
                    model=SearchByDate,
                    display_mode="page",
                    method="GOTO",
                    submit_url="/posts/date/",
                ),
            ]
        ),
    ]


@router.post(
    "/api/forms/date",
    tags=["forms"],
    response_model=FastUI,
)
def search_by_date_response(
    start_date: Annotated[date, Form()],
    end_date: Annotated[date, Form()],
    select_single: Annotated[CommentPostEnum, Form()],
):
    print({end_date, start_date})
    start_date_datetime = datetime(start_date.year, start_date.month, start_date.day)
    end_date_datetime = datetime(end_date.year, end_date.month, end_date.day)

    start_epoch = int(start_date_datetime.timestamp())
    end_epoch = int(end_date_datetime.timestamp())

    assert type(start_epoch) is int
    assert type(end_epoch) is int

    return RedirectResponse(
        url=f"/posts/date/?form=date&start_date={start_epoch}&end_date={end_epoch}"
    )


@router.get(
    "/api/forms/keyword",
    tags=["forms"],
    response_model=FastUI,
    response_model_exclude_none=True,
)
def search_by_keyword_form() -> list[AnyComponent]:
    return [
        c.PageTitle(text=f"Search"),
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
                    active="startswith:/forms/keyword/",
                ),
            ],
        ),
        c.Page(
            components=[
                c.ModelForm(
                    model=SearchByKeyword,
                    display_mode="page",
                    submit_url="/posts/keyword/",
                    method="GOTO",
                ),
            ]
        ),
    ]


@router.post(
    "/api/forms/keyword",
    tags=["forms"],
    response_model=FastUI,
    response_model_exclude_none=True,
)
def search_by_keyword_response(search_keyword: SearchByKeyword):
    pass
