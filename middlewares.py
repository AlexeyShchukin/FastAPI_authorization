from starlette.middleware.cors import CORSMiddleware

from main import app

origins = [
        "http://127.0.0.1:8000",
        "http://localhost:8000"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=['*'],
    allow_headers=['*'],
    allow_credentials=True
)