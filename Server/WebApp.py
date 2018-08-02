from flask import Flask, render_template
from bokeh.embed import server_document
from tornado.ioloop import IOLoop
import sys
sys.path.append("..")
app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template("main.html")


@app.route('/main.html', methods=['GET'])
def main():
    return render_template("main.html")


@app.route('/kmeans.html', methods=['GET'])
def kmeans():
    return render_template("kmeans.html")


@app.route('/about.html', methods=['GET'])
def about():
    return render_template("about.html")


@app.route('/neural.html', methods=['GET'])
def neural():
    return render_template("neural.html")


@app.route('/karpuzkavun.html', methods=['GET'])
def karpuzkavun():
    return render_template("karpuzkavun.html")


@app.route('/gameOfThrones.html', methods=['GET'])
def got():
    return render_template("gameOfThrones.html")


@app.route('/charts.html', methods=['GET'])
def charts():
    return render_template("charts.html")


@app.route('/agac', methods=['GET'])
def tree():
    script = server_document("http://localhost:5006/bokeh-decision-tree")
    return render_template("index.html", script=script)


if __name__ == '__main__':
    app.run(port=8000)
