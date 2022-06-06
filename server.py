from flask import Flask
# from threading import Thread
import _thread
import json
SRC     = "sourse.json"
app = Flask(__name__)

@app.route('/')
def index():
    import pytz
    from datetime import datetime
    TZ = pytz.timezone("Europe/Minsk")
    date = datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S")
    return f'Hello from Flask! {date}'
  
@app.route('/json')
def returnJson():
    with open(SRC, "r") as file:
        text = file.read()
    src = json.loads(text)
    textLi = ""
    for k,v in src.items():
      textLi += f"<li>{k} : <b>{v}</b></li>\n"
    list = f"""\n<ul>\n{textLi}\n</ul>"""
    
    return list
# app.run(host='0.0.0.0', port=81)

def run():
  app.run(host="0.0.0.0",port=8080)

def keep_alive():
#   t = Thread(target=run)
  t = _thread.start_new_thread( run, () )
  print(t)
#   t.start()

