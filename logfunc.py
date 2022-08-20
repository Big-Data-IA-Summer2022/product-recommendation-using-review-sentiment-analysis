from google.cloud import bigquery
from dotenv import load_dotenv
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS']='./key.json'

def logfunc(username:str, issue:str, endpoint:str, response_code: int):
    client = bigquery.Client()
    max=client.query(f"""select max(logid)+1, string(current_timestamp()) as tstamp FROM `defect-detection-356414.for_logs.logs`""").result()
    for i in max:
        var= i[0]
        tstamp=i[1]
    print('log id',var,'has been populated')
    rows_to_insert =[{"logid":var, "logtime":tstamp ,"issue":issue, "endpoint": endpoint, "response_code": response_code}]
    errors = client.insert_rows_json('defect-detection-356414.for_logs.logs', rows_to_insert)  # Make an API request.
    if errors == []:
        print("New rows have been added.")
    else:
        print("Encountered errors while inserting rows: {}".format(errors))