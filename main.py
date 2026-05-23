from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
 
app = FastAPI()
 
# Allow the frontend to call this API from the browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
 
@app.get("/strings")
def get_strings():
    return ["apple", "banana", "cherry", "date", "elderberry"]
 
 
# Run with: uvicorn main:app --reload