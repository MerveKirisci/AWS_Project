import os
import json
import boto3
import mysql.connector
import datetime
import time

insert_new_data = "select `range` as r, timestamp time from flood order by id ASC;"


def lambda_handler(event, context):
    cnx = mysql.connector.connect(host=os.environ['RDS_HOSTNAME'], user=os.environ['RDS_USERNAME'],
                                  passwd=os.environ['RDS_PASSWORD'],
                                  database=os.environ['RDS_DB_NAME'], port=os.environ['RDS_PORT'])

    cur = cnx.cursor()
    cur.execute(insert_new_data)
    res = cur.fetchall()
    cnx.close()
    ret = []
    for row in res:
        dt_obj = row[1]
        timestamp_ms = int(time.mktime(dt_obj.timetuple()) * 1000)
        ret.append([timestamp_ms, row[0]])

    return {"statusCode": 200,
            "headers": {"content-type": "application/json"},
            "body": json.dumps(ret, indent=0, sort_keys=True, default=str)}