from starlette.middleware.cors import CORSMiddleware

from main import app

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8000",
        "http://localhost:8000"
    ],
)