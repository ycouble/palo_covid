from flask import Flask
app = Flask(__name__)


_DATASETS = {
    "jhu": "Johns Hopkins University",
    "wm": "Worldometers.info",
    "kor": "Korea Centers for Disease Control & Prevention",
    "srk": "SRK",
}
DATASETS = [{"code": code, "name": name} for code, name in _DATASETS.items()]


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/covid')
def covid():
    return 'Covid Overview'


@app.route('/covid/datasets')
def covid_datasets():
    return {"datasets": DATASETS}

