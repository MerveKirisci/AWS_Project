import os
import json
import boto3
import mysql.connector
import time

insert_new_data = "INSERT INTO `flood` (`range`) VALUES (%s);"


def lambda_handler(event, context):
    myrange = str(event['queryStringParameters']['range'])

    cnx = mysql.connector.connect(host=os.environ['RDS_HOSTNAME'], user=os.environ['RDS_USERNAME'],
                                  passwd=os.environ['RDS_PASSWORD'],
                                  database=os.environ['RDS_DB_NAME'], port=os.environ['RDS_PORT'])

    cur = cnx.cursor()
    cur.execute(insert_new_data, (myrange,))
    cnx.commit()
    cnx.close()

    myrange = int(myrange)

    if myrange < 10:

        filename = '/tmp/epoch_time2.txt'

        if os.path.exists(filename):
            with open(filename, 'r') as file:
                epoch_time_str = file.read().strip()
                epoch_time = int(epoch_time_str)
                print(f"Epoch time from existing file '{filename}': {epoch_time}")

                current_epoch_time = int(time.time())
                epoch_diff = current_epoch_time - epoch_time
                print(f"epoch_diff:{epoch_diff}")
                if epoch_diff > 10:
                    with open(filename, 'w') as file2:
                        file2.truncate(0)
                        file2.write(str(current_epoch_time))
                    sns = boto3.client('sns', region_name='eu-north-1')
                    message = 'Nehir seviyesi beklenen degerden yuksek cikmistir. Bolgeyi terk edin yada yuksek bir yere cikin !'

                    response = sns.publish(
                        TopicArn='arn:aws:sns:eu-north-1:112061248042:sus',
                        Message=message
                    )


        else:
            epoch_time = int(time.time())
            epoch_time_str = str(epoch_time)
            with open(filename, 'w') as file:
                file.write(epoch_time_str)
            print(f"Epoch time written to new file '{filename}': {epoch_time}")

    # Okunan verileri JSON formatında döndürün
    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }