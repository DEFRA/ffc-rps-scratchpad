from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from alb_checker import process, groupchat

app = FastAPI()

# Define the request body model
class TextRequest(BaseModel):
    text: str

# Mount a directory to serve static files like CSS, images, JS (if needed)
app.mount("/static", StaticFiles(directory="static"), name="static")



# User-facing HTML page to get the input text
@app.get("/", response_class=HTMLResponse)
async def read_html():
    # Read the HTML file content and return it
    with open("templates/index.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.post("/alb", response_class=HTMLResponse)
async def alb_checker(text: str = Form(...)):
    # process the text
    response = process(text, groupchat)

    # generate some HTML to return

    html = "<h1>Results</h1><br>"

    for item in response.chat_history:
        if item.get('name', '') == 'admin':
            continue
        name = item.get('name', '')
        content = item.get('content', '')
        #content_paragraphs = '<p>' + content.replace('\n', '</p><p>') + '</p>'
        content_paragraphs = paragraphise(content)

        html += f"\n<h2>{name}</h2><br>{content_paragraphs}<br>"

    summary = paragraphise(response.summary)

    html += f"\n<h2>Summary</h2><br>{summary}"

    return html

def paragraphise(text: str):
    return '<p>' + text.replace('\n', '</p><p>') + '</p>'