import datetime

import pandas as pd
from flask import Flask, request, jsonify
from flasgger import Swagger, swag_from

import etl.integration as ei

app = Flask(__name__)
swagger = Swagger(app)


DATASETS = [
    {"code":     "jhu", "name": "Johns Hopkins University", "integrated": False},
    {"code": "wm", "name": "Worldometers.info", "integrated": False},
    {"code":"kor",
        "name": "Korea Centers for Disease Control & Prevention",
        "integrated": False,
    },
    {"code":"srk", "name": "SRK", "integrated": True},
]


@app.route("/")
def hello_world():
    return jsonify("Hello, World!")


@app.route("/covid")
def covid():
    """
    Covid base entry point
    ---
    responses:
        200:
            description: no useful results returned
    """
    return jsonify("Covid Overview")


@app.route("/covid/datasets")
def covid_datasets():
    """
    Covid base entry point
    ---
    responses:
        200:
            description: The list of datasets
            schema: 
                datasets: [{code: name}]
    """
    return jsonify({"datasets": DATASETS})


@app.route("/covid/<day>/<country>")
def covid_get_by_date_and_country(day, country):
    aggregated = ei.get_aggregated() 
    if (country, day) in aggregated.index:
        return jsonify(aggregated.loc[country, day].to_dict())
    else:
        return jsonify(
            {
                "Confirmed": float("nan"),
                "Deaths": float("nan"),
                "Recovered": float("nan"),
                "EntryCount": 0,
            }
        )
