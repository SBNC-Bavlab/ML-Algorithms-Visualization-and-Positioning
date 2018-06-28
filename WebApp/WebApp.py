from flask import Flask, render_template, request
from WebApp.bokeh.decision_tree import create_figure
from bokeh.embed import components
app = Flask(__name__)


# Index page
@app.route('/')
def index():


    # Create the plot
    plot = create_figure()

    # Embed plot into HTML via Flask Render
    script, div = components(plot)
    return render_template("index.html", script=script, div=div,
                           feature_names=[], current_feature_name="")

@app.route('/q', methods=['GET'])
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'

# With debug=True, Flask server will auto-reload
# when there are code changes
if __name__ == '__main__':
    app.run(port=5000, debug=True)
