from flask import Flask, render_template, request
from threading import Thread

from bokeh.embed import server_document
from bokeh.server.server import Server
from tornado.ioloop import IOLoop
import sys
sys.path.append("..")
from Bokeh.Decision_Tree.Plot.plot_decision_tree import create_figure
from Bokeh.K_Means.kmeans_cluestering import create_figure as create_figure_k_means
from bokeh.embed import components
app = Flask(__name__)


def modify_doc(doc):
    plot = create_figure()
    doc.add_root(plot)


def modify_doc2(doc):
    plot = create_figure_k_means()
    doc.add_root(plot)


@app.route('/q', methods=['GET'])
def shut():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.route('/', methods=['GET'])
def bkapp_page():
    script = server_document('http://localhost:5006/bkapp')
    return render_template("index.html", script=script, template="Flask")


@app.route('/k_means', methods=['GET'])
def bkapp_page2():
    script = server_document('http://localhost:5006/bkapp2')
    return render_template("index2.html", script=script, template="Flask")


@app.route('/karpuzkavun')
def karpuz():
    return render_template("karpuzkavun.html", template="Flask")


def bk_worker():
    # Can't pass num_procs > 1 in this configuration. If you need to run multiple
    # processes, see e.g. flask_gunicorn_embed.py
    server = Server({'/bkapp': modify_doc, '/bkapp2': modify_doc2}, io_loop=IOLoop(), allow_websocket_origin=["localhost:8000"])
    server.start()
    server.io_loop.start()


Thread(target=bk_worker).start()

if __name__ == '__main__':
    print('Opening single process Flask app with embedded Bokeh application on http://localhost:8000/')
    print()
    print('Multiple connections may block the Bokeh app in this configuration!')
    print('See "flask_gunicorn_embed.py" for one way to run multi-process')
    app.run(port=8000)
