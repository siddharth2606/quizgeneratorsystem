from fastapi import FastAPI , Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

templates = Jinja2Templates(directory="templates")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.get("/",response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html",{"request":request,"mcq":""})

@app.post("/generate",response_class=HTMLResponse)
async def generate_quiz(request:Request,topic:str=Form(...),num:int=Form(...)):
    
    prompt = f"Generate {num} MCQ Questions on {topic} with answer"

    chat_completion = client.chat.completions.create(
        messages=[{"role":"user","content":prompt}],
        model="llama-3.3-70b-versatile",
    )

    mcq = chat_completion.choices[0].message.content

    return templates.TemplateResponse(
        "index.html",
        {"request":request,"mcq":mcq}
    )