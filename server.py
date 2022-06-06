from flask import Flask, render_template
# from threading import Thread
import threading
# import _thread
import json
SRC     = "sourse.json"
app = Flask(__name__)

@app.route('/')
def index():
    import pytz
    from datetime import datetime
    TZ = pytz.timezone("Europe/Minsk")
    date = datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S")
    # return f'Hello from Flask! {date}'



    SRC = json.load(open("sourse.json"))

    return render_template('index.html',date=date,SRC=SRC)
  
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

@app.route("/log")
def log():
    with open("/home/valentin13/Desktop/Programming/Python/Code/VisaItaly/log.log", "r") as file:
        text = file.read()
    arr = text.splitlines()


    for i in range(len(arr)):
        date  = arr[i] [:17]
        level = arr[i] [18:26]
        func  = arr[i] [27:44]
        msg   = arr[i] [45:]
        new_s = "<div class='box'>"f'<strong>{date}</strong> <span style="color:#00994d">{level}</span> <span style="color:#9933ff">{func}</span> <i>{msg}</i>' + "</div>"
        # print(new_s)
        arr[i] = new_s
    text = "\n\n".join(arr)


    s1 = """
        <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Logs</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css">
    </head>
    <body>
    <section class="section">
        <div class="box">
        <h1 class="title">
            Hello User
        </h1>
        <h2 class="subtitle">
        This is the page with <strong>logs</strong>!
        </p>
        </div>
    </section>
    <section class="section">
        <div class="box">
        """
    s2 = """
        </div>
    </section>
    </body>
    </html>
        """
    html = s1 + f"""{text}""" + s2

    with open("templates/log.html", "w") as file:
        file.write(html)
    #     <div class="box">
    #     {{text}}
    # </div>


    return render_template('log.html')

# app.run(host='0.0.0.0', port=81)

def run():
  print("server started",threading.current_thread())
  app.run(host="0.0.0.0",port=8080)
  print("Server was running. Complited")

def keep_alive():
#   t = Thread(target=run)
#   t = _thread.start_new_thread( run, () )
#   print(t)
    threading.Thread(target=run).start()
    print("Thread started in keep_alive server.py")
#   t.start()

