from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from prompt_to_ts import prompt_to_ts

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def name(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/submit-form")
async def submit_form(request: Request, doc: str = Form(...), schema: str = Form(...)):
    answer = prompt_to_ts(text=doc, schema=schema)
    return templates.TemplateResponse(
        "result.html", {"request": request, "answer": answer}
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
