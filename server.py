from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    with open(f"./root/index.md", "rt") as f:
        passage_markdown = f.read()
    return render_template("article_template.html")

@app.route("/root")
def root():
    with open(f"./root/index.md", "rt") as f:
        passage_markdown = f.read()
    return render_template("article_template.html")

@app.route("/root/<path:passagepath>")
def template(passagepath):
    with open(f"./root/{passagepath}") as f:
        passage_markdown = f.read()
    return render_template("article_template.html")

@app.route("/markdown/<path:mdpath>")
def markdown(mdpath):
    with open(f"./root/{mdpath}", "rt") as f:
        md = f.read()
    return md

@app.route("/data/directory")
def getDirectory():
    raw = "nothing"
    with open("./directory.json", "rt") as f:
        raw = f.read()
    return raw

if __name__ == "__main__" :
    app.run("0.0.0.0", 8888, debug = True)
