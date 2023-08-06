import sys
import socket
import requests
from visualone import utils
import random
import string
import json
import glob
import time


__version__ = '0.0.14'

samples_s3_folder = 'pypi_samples'
inference_samples_s3_folder = 'pypi_toinfer'

'''
Instructions to upload to PyPi: https://packaging.python.org/tutorials/packaging-projects/

python3 setup.py sdist bdist_wheel

python3 -m twine upload dist/*

'''

class client():
        
    def __init__(self, public_key, private_key):
        self.public_key = public_key
        self.private_key = private_key
        self.object_id = ''
                        
    @property
    def object_id(self):
        return self._object_id

    @object_id.setter
    def object_id(self, oid):
        clients = utils.get_client(self.public_key)
        if len(clients) == 0: raise Exception("Invalid api_public_key!")
        if len(clients) > 1: raise Exception("Invalid client. Contact Visual One team at contact@visualone.tech")  
        if not clients[0]['private_key'] == self.private_key: raise Exception("Invalid api_private_key!")
        self._object_id = clients[0]['objectId']    
                       
        
        
    def train(self, positive_samples, negative_samples, n_pos = -1, n_neg = -1):
        
        confidence_threshold = 0
        
        config = utils.get_config('pypi')[0]
        event_manager_endpoint = config['event_manager_endpoint']
        aws_access_key = config['aws_access_key']
        aws_secret_key = config['aws_secret_key']
           
        task_id = 'PP_' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))

        if isinstance(positive_samples, str):
            # Upload the positive samples into s3
            positive_samples = glob.glob(positive_samples + "/*.jpg") + glob.glob(positive_samples + "/*.png") + glob.glob(positive_samples + "/*.JPG") + glob.glob(positive_samples + "/*.PNG") + glob.glob(positive_samples + "/*.JPEG") + glob.glob(positive_samples + "/*.jpeg") + glob.glob(positive_samples + "/*.BMP") + glob.glob(positive_samples + "/*.bmp")
        elif not isinstance(positive_samples, list):
            raise Exception("Invalid first argument. positive_samples must be the path to the positive samples or a list of postive samples file names.")
        
        if n_pos > 0 and n_pos < len(positive_samples):
            positive_samples = positive_samples[:n_pos]
                
        print("Positive samples:")
        n_positive = 0
        for positive_sample in positive_samples:
            n_positive += 1
            utils.upload_to_s3(positive_sample,
                               samples_s3_folder, 
                               "{}_positive_{}.jpg".format(task_id, str(n_positive)),
                               aws_access_key,
                               aws_secret_key) 
            print("#{}: {}".format(str(n_positive), positive_sample))
        
        print("Found {} positive samples.\n".format(str(n_positive)))
        
        if isinstance(negative_samples, str):
            # Upload the negative samples into s3
            negative_samples = glob.glob(negative_samples + "/*.jpg") + glob.glob(negative_samples + "/*.png") + glob.glob(negative_samples + "/*.JPG") + glob.glob(negative_samples + "/*.PNG") + glob.glob(negative_samples + "/*.JPEG") + glob.glob(negative_samples + "/*.jpeg") + glob.glob(negative_samples + "/*.BMP") + glob.glob(negative_samples + "/*.bmp")
        elif not isinstance(negative_samples, list):
            raise Exception("Invalid first argument. negative_samples must be the path to the negative samples or a list of negative samples file names.")
        
        if n_neg > 0 and n_neg < len(negative_samples):
            negative_samples = negative_samples[:n_neg]
        
        print("Negative samples:")
        n_negative = 0
        for negative_sample in negative_samples:
            n_negative += 1
            utils.upload_to_s3(negative_sample, 
                               samples_s3_folder, 
                               "{}_negative_{}.jpg".format(task_id, str(n_negative)),
                               aws_access_key,
                               aws_secret_key)
            print("#{}: {}".format(str(n_negative), negative_sample))
        
        print("Found {} negative samples.\n".format(str(n_negative)))
        
        print("Creating a task... task_id = {}\n".format(task_id)) 
        
        print("Training a model...\n")
        
        payload = {
            "event_id": task_id,
            "camera_id": 'nil',
            "event_name": 'nil',
            "conf_threshold": confidence_threshold,
            "n_positive": n_positive,
            "n_negative": n_negative,
            "client_id": self.object_id,
            "samples_s3_bucket": 'vo-fsl-demo2',
            "samples_s3_folder": samples_s3_folder
        }
                
        # Create the event 
        resp = requests.post(event_manager_endpoint + '/event', json = payload)
        
        resp_json = json.loads(resp.content)
        
        result = {}
        result['task_id'] = resp_json['event_id'] 
        result['message'] = resp_json['message']
        result['success'] = resp_json['success']
        result['n_positive_samples'] = n_positive
        result['n_negative_samples'] = n_negative
        
        return result
    
        
    def predict(self, task_id, image_file):
        
        config = utils.get_config('pypi')[0]
        event_predictor_endpoint =  config['event_predictor_endpoint']
        aws_access_key = config['aws_access_key']
        aws_secret_key = config['aws_secret_key']
        
#         events = utils.get_event(event_id)
#         conf_threshold = 0
#         if len(events) == 0:
#             return 'The event_id is invalid.'
#         elif len(events) > 1:
#             return 'Duplicate events in DB. Please contact VisualOne.'
#         else: 
#             conf_threshold = events[0]['conf_threshold']
            
        utils.upload_to_s3(image_file, 
                           inference_samples_s3_folder, 
                           "{}.jpg".format(task_id),
                           aws_access_key,
                           aws_secret_key)
        
        payload = {
            "event_id": task_id,
            "event_name": 'nil',
            "image_name": "{}.jpg".format(task_id),
            "timestamp": round(time.time()*1000),
            "update_model": False,
            "force_late_infer": True,
            "inference_samples_s3_bucket": 'vo-fsl-demo2',
            "inference_samples_s3_folder": inference_samples_s3_folder
        }
                
        resp_json = {}
        try:
            resp = requests.post(event_predictor_endpoint, json = payload)
        
            resp_json = json.loads(resp.content)
            
        except:
            return 'An error occured.'
        
        result = {}
        result['prediction'] = resp_json['prediction'] 
        result['confidence'] = resp_json['confidence']
        result['task_id'] = resp_json['event_id']
        result['latency'] = resp_json['latency']
        
        return result
            
        
            
            


