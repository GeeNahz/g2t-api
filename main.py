import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from routes import jobpost, post, user, contact, faq


app = FastAPI(
    title="G2G API"
)

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "GET", "PUT", "DELETE"],
    allow_headers=["*"],
)

script_dir = os.path.dirname(__file__)
static_path = os.path.join(script_dir, "static/")

app.mount("/static", StaticFiles(directory=static_path), name="static")


@app.get('/')
async def root():
    return RedirectResponse('/redoc')


app.include_router(post.router)
app.include_router(jobpost.router)
app.include_router(contact.router)
app.include_router(faq.router)
app.include_router(user.router)
