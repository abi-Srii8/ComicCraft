from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .config import settings
from .routes import router


BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI(
    title=settings.app_name,
   debug=True)

# Static files
app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)

# HTML templates
templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)

# Store templates inside app state
app.state.templates = templates

# Routes
app.include_router(router)