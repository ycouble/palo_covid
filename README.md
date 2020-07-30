# Sources for a technical test
Objective: build a few webservices based on a rest API to provide data from online covid datasets

# Usage
Create a virtual environment, pip install all requirements
```
(.venv) $ pip install -r requirements.txt
```

## Update data (or reset DB)
```
(.venv) $ ./update_data.py
```

## Start server in dev mode (only local access)
```
(.venv) $ ./start_server.sh
```
A server will be listening on port 5000: http://localhost:5000.

To see available endpoints, see http://localhost:5000/apidocs

## Predict future data
```
(.venv) $ ./predict "US UK France"
```
Uses implementation describes in https://www.kaggle.com/eswarchandt/covid-19-forecasting-xgboost/comments

# Status
- 28/07/2020 (4h):
  - flask REST API prototype working on several endpoints
  - prototype for API doc using flasgger
  - get datapoint by date and country: OK, but needs to be optimized since it performs the group by
    at each call
  - Limitations: 
    - used only srk dataset `covid_19_data.csv`
    - some hardcoded values
    - does not use online data, but local csv
- 29/07/2020 (4h):
  - difficulty: generification for multiple sources, lost a lot of time...
  - split data extraction/uniformization and api responses which are now only data queries
  - enriched /covid/countries/<country> endpoint with a special keyword latest to get latests stats for the country
  - set up automatic tests (basic availability of endpoints for now)
  - Added Post method on countries endpoint + test
- 30/07/2020 (5h):
  - difficulty (4h): parametrizing xgboost to try (unsuccessfully) to extrapolate future datapoints. Given implementation seems to be overfitting the training set
  - implemented notebook from kaggle, adapted for a routine job, and for our data
  - writing predictions to DB (csv)
- Wished to do, but no time:
  - storage of data in a DB
  - deploy online on public IP
  - online retrieving of data
  - prediction of future data from parameter, e.g. predict the next 10 days.
  - API endpoints to trigger data refresh, prediction etc.
  - more detailed tests, behavior driven tests (behave)
  - add sources
  - package

