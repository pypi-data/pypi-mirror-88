import boto3
import time
import json
import http.client
import urllib
from PIL import Image
import os
import os.path

parseServer = 'ec2-44-235-188-114.us-west-2.compute.amazonaws.com'
parseServerPort = 80
parseApplicationId = "myappID"

s3_bucket = 'vo-fsl-demo2'


def upload_to_s3(local_file_name, s3_folder, s3_file_name, aws_access_key, aws_secret_key, image_size = 500):
           
    try:
        file_name_split = os.path.splitext(local_file_name)    
        resized_image_file = file_name_split[0] + '_rsd' + file_name_split[1]
        img = Image.open(local_file_name).resize((image_size, image_size))
        if img.mode != 'RGB':
            img = img.convert('RGB')
        img.save(resized_image_file)
    except:
        resized_image_file = local_file_name
    
    s3 = boto3.client('s3', aws_access_key_id = aws_access_key , aws_secret_access_key = aws_secret_key)
    try:
        s3.upload_file(resized_image_file, s3_bucket, s3_folder + '/' + s3_file_name)
        os.remove(resized_image_file)
        return True
    except:
        os.remove(resized_image_file)
        return False
    
    
def create_user(username, accesscode):
    connection = http.client.HTTPConnection(parseServer, parseServerPort)
    connection.connect()
    connection.request('POST', '/parse/classes/_User', json.dumps({
        "username": username,
        "accesscode": accesscode,
        "client_id": "pypi"
    }), {
        "X-Parse-Application-Id": parseApplicationId,
        "Content-Type": "application/json"
    })
    return json.loads(connection.getresponse().read())



def get_client(public_key):
    connection = http.client.HTTPConnection(parseServer, parseServerPort)
    connection.connect()
    params = urllib.parse.urlencode({"where": json.dumps({
        "public_key": public_key
    })})
    connection.request('GET', '/parse/classes/Client?%s' % params, '', {
        "X-Parse-Application-Id": parseApplicationId
    })
    return json.loads(connection.getresponse().read())["results"]


def get_event(event_id):
    connection = http.client.HTTPConnection(parseServer, parseServerPort)
    connection.connect()
    params = urllib.parse.urlencode({"where": json.dumps({
        "event_id": event_id
    })})
    connection.request('GET', '/parse/classes/Event?%s' % params, '', {
        "X-Parse-Application-Id": parseApplicationId
    })
    return json.loads(connection.getresponse().read())["results"]


def get_config(client_type):
    connection = http.client.HTTPConnection(parseServer, parseServerPort)
    connection.connect()
    params = urllib.parse.urlencode({"where": json.dumps({
        "client_type": client_type
    })})
    connection.request('GET', '/parse/classes/Config?%s' % params, '', {
        "X-Parse-Application-Id": parseApplicationId
    })
    return json.loads(connection.getresponse().read())["results"]





