
# replication of initial sparql query across to wikidata 

import pandas
import pydash
import requests

def value_extract(row, col):

    ''' Extract dictionary values. '''

    return pydash.get(row[col], "value")

def sparql_query(query, service):

    ''' Send sparql request, and formulate results into a dataframe. '''

    r = requests.get(service, params={"format": "json", "query": query})
    data = pydash.get(r.json(), "results.bindings")
    data = pandas.DataFrame.from_dict(data)
    for x in data.columns:
        data[x] = data.apply(value_extract, col=x, axis=1)
    return data

# warnings.simplefilter(action='ignore', category=FutureWarning)

query = """
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
select distinct ?editor
where { 
    wd:Q1346439 wdt:P1040 ?editor . 
} """

#   // send batches to wikidata.
#   return new Promise((resolve) => {
#     setTimeout(() => {
#       let wd_list = "wd:" + y.join(" wd:");
#       let query =
#         `select ?film ?filmLabel ?dirLabel ?year where {
#            values ?film { wd:` +
#         wd_list +
#         ` } .
#          ?film wdt:P57 ?dir .
#          ?film  wdt:P577 ?year .
#          service wikibase:label {bd:serviceParam wikibase:language "en". }}`;
#       let sparql_request = d3.json(
#         `https://query.wikidata.org/sparql?query=${encodeURIComponent(query)}`,
#         { headers: { accept: "application/sparql-results+json" } }
#       );
#       resolve(sparql_request);
#     }, 500);
#   });

dataframe = sparql_query(query, "https://query.wikidata.org/sparql")
print(len(dataframe))
print(dataframe.head())