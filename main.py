from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.templating import Jinja2Templates
import uvicorn
from wiki import Wikipedia


app = FastAPI()
templates = Jinja2Templates(directory="src/templates")


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/{title}")
def contact_details(title: str):
    return Wikipedia(title).request()


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
