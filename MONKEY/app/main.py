# import pandas as pd

from time import sleep

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastui import FastUI, AnyComponent, prebuilt_html, components as c
from fastui.events import GoToEvent

from app.routers import posts, forms

from app.data.service import DataBaseConn


app = FastAPI()

app.include_router(posts.router)
app.include_router(forms.router)


@app.on_event("startup")
async def startup():
    sleep(1)
    app.state.db = DataBaseConn(
        "postgresql://berry_user:S3cret@localhost:5432/berry_db"
    )


@app.get("/api/", response_model=FastUI, response_model_exclude_none=True)
def fron_page() -> list[AnyComponent]:
    return [
        c.PageTitle(text="BERRY"),
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
    ]


@app.get("/{path:path}")
async def html_landing() -> HTMLResponse:
    """Simple HTML page which serves the React app, comes last as it matches all paths."""
    return HTMLResponse(prebuilt_html(title="FastUI Demo"))
