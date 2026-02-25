from fastapi import FastAPI, Response, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
from user_agents import parse
from babel import Locale

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def get_lang_display_name(request: Request) -> str:
   header = request.headers.get("accept-language")
   lang: str = header.split(',')[0].strip().replace('-', '_')
   
   if not lang:
      return "Unknown"
   
   locale = Locale.parse(lang)
   return locale.display_name

@app.get('/')
async def root(request:Request):
   ua = parse(request.headers.get("user-agent"))

   device_str = f"{'None' if not ua.device.model else ua.device.model}; {ua.device.brand}" 

   context_dict = {
      "request": request,
      "url": request.url,
      "os": f"{ua.os.family} {ua.os.version_string}",
      "browser": f"{ua.browser.family} {ua.browser.version_string}",
      "device": device_str,
      "language": get_lang_display_name(request)
   }

   return templates.TemplateResponse("index.html", context_dict)

@app.get('/form')
async def root(request:Request):
   return templates.TemplateResponse("form.html", {"request": request})

@app.post('/form')
async def root(response: Response):
   return {"message": "success", "data": response}

if __name__ == "__main__":
   uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
   