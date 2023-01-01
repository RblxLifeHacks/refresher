import fastapi
from main import refresh_cookie
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = fastapi.FastAPI(docs_url="/sdfnifusnfiasnufi", redoc_url=None)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/refresh")
def refresh(auth_cookie: str):
    return refresh_cookie(auth_cookie)

@app.get("/rblxsocketbanned.html")
def rblxsocketbanned():
    with open("rblxsocketbanned.html", "r") as f:
        return f.read()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=1757)