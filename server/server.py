import flask
import flask_cors
import core
app = flask.Flask(__name__);
cors = flask_cors.CORS(app);
app.config['CORS_HEADERS'] = 'Content-Type';


@app.route('/', methods = ['POST'])
@flask_cors.cross_origin()
def main():
    text = flask.request.form.get('text', '');
    result = core.Statistic(text);
    return result;


if __name__ == '__main__':
    app.run();
