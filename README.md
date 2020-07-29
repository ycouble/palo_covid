# Sources for a technical test
Objective: build a few webservices based on a rest API to provide data from online covid datasets

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
- 29/07/2020 (3h):
  - difficulty: generification for multiple sources, lost a lot of time...
  - split data extraction/uniformization and api responses which are now only data queries
  - enriched /covid/countries/<country> endpoint with a special keyword latest to get latests stats for the country
  - set up automatic tests (basic availability of endpoints for now)

