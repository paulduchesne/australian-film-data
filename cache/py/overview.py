
# replication of initial sparql query to wikidata.

import json
import pandas
import pathlib
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

wd_list = requests.get('https://raw.githubusercontent.com/paulduchesne/australian-filmography/main/entities.json')
wd_list = [x['wikidata'] for x in json.loads(wd_list.text)['entities']]

dataframe = pandas.DataFrame()

for x in range(int(len(wd_list)/100)+1):

    wd_chunk = wd_list[(x*100):((x+1)*100)]
    wd_chunk = 'wd:'+' wd:'.join([x for x in wd_chunk])

    query = """
        select ?film ?filmLabel ?dirLabel ?year where {
            values ?film { """+wd_chunk+""" } .
            ?film wdt:P57 ?dir .
            ?film  wdt:P577 ?year .
            service wikibase:label {bd:serviceParam wikibase:language "en". }}
            """

    dataframe = pandas.concat([dataframe, sparql_query(query, "https://query.wikidata.org/sparql")])

with open(pathlib.Path.cwd().parents[0] / 'json' / 'overview.json', 'w') as export:
    json.dump(dataframe.to_dict('records'), export, indent=4)

print(len(dataframe))
print(dataframe.head())