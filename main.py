from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://faradumatin.github.io"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/strings")
def get_strings():
    return ["apple", "banana", "cherry", "date", "elderberry"]