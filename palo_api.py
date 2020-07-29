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
    Covid data brief
    ---
    responses:
        200:
            description: various stats about the data
    """
    df = ei.get_aggregated()
    return jsonify(df.describe().to_dict())


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


@app.route("/covid/countries/<country>")
def covid_get_latest_for_country(country):
    return covid_get_by_date_and_country("latest", country)


@app.route("/covid/countries/<country>/<day>")
def covid_get_by_date_and_country(day, country):
    """
    Get datapoint by Country and date, or latest for the given country
    Use day = 'latest' to retrieve latest stats for the given country
    ---
    examples:
        /covid/countries/France/2020-02-21 will return stats for Feb 21st 2020 for France
        /covid/countries/France/latest will return latest stats for France
    """
    df = ei.get_aggregated()
    if day == "latest":
        by_c = df[df["Country"] == country]
        result = [
            res for res in by_c[by_c["Date"] == by_c["Date"].max()]
            .to_dict(orient='index')
            .values()
        ]
    else:
        result = [
            res for res in df[(df['Country'] == country) & (df['Date'] == day)]
            .to_dict(orient='index')
            .values()
        ]
    return jsonify(result)


@app.route("/covid/world")
def covid_get_latest_for_world():
    return covid_get_world_by_date("latest")


@app.route("/covid/world/<day>")
def covid_get_world_by_date(day):
    """
    Get datapoint for the world for the given date
    Use day = 'latest' to retrieve latest stats for the given country
    ---
    examples:
        /covid/world/2020-02-21 will return stats for Feb 21st 2020 for World
        /covid/world/latest will return latest stats for World
    """
    df = ei.get_world()
    if day == "latest":
        result = [
            res for res in df[df["Date"] == df["Date"].max()]
            .to_dict(orient='index')
            .values()
        ]
    else:
        result = [
            res for res in df[df['Date'] == day]
            .to_dict(orient='index')
            .values()
        ]
    return jsonify(result)

