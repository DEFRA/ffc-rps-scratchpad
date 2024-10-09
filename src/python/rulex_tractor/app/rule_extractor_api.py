from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from rule_extractor import client, get_prompt, extract_structured_rules, promptfile

app = FastAPI()

system_prompt = get_prompt(promptfile)

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

@app.post("/xtractor", response_class=HTMLResponse)
async def xtractor(text: str = Form(...)):
    # process the text
    result = extract_structured_rules(text, system_prompt, client)

    html = "<h1>Results</h1><br>"
    html += f"<pre><code>{result}</code></pre>"

    return html