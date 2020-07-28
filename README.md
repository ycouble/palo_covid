# Sources for a technical test
Objective: build a few webservices based on a rest API to provide data from online covid datasets

# Status
- 28/07/2020:
  - flask REST API prototype working on several endpoints
  - prototype for API doc using flasgger
  - get datapoint by date and country: OK, but needs to be optimized since it performs the group by
    at each call
  - Limitations: 
    - used only srk dataset `covid_19_data.csv`
    - some hardcoded values
    - does not use online data, but local csv
