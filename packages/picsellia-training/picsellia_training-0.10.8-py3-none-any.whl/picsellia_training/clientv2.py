import json
import os
import sys
import io
import requests
from PIL import Image, ImageDraw, ExifTags
from multiprocessing.pool import ThreadPool
from multiprocessing import Pool, Value
import picsellia_training.pxl_multithreading as mlt
import time
import zipfile
import picsellia_training.pxl_exceptions as exceptions
from uuid import UUID, uuid4
from picsellia_training.pxl_utils import is_uuid
import picsellia_training.pxl_utils as utils
from picsellia_training.pxl_urls_v2 import Urls as urls
from pathlib import Path

class Client:



    def __init__(self, api_token, host="https://app.picsellia.com/sdk/", interactive=True):
        """[summary]

        Args:
            api_token ([token]): [Your api token accessible in Profile Page]
            host (str, optional): [description]. Defaults to "http://127.0.0.1:8000/sdk/v2/".
            interactive (bool, optional): [set verbose mode]. Defaults to True.

        Raises:
            exceptions.NetworkError: [If Platform Not responding]
        """

        self.supported_img_types = ("png", "jpg", "jpeg", "JPG", "JPEG", "PNG")
        self.auth = {"Authorization": "Token " + api_token}
        self.host = host

        try:
            r = requests.get(self.host + 'ping', headers=self.auth)
        except Exception:
            raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")  

        # User Variables 
        self.username = r.json()["username"]

        # Project Variables
        self.project_name_list = None
        self.project_token = None
        self.project_id = None
        self.project_infos = None
        self.project_name = None
        self.project_type = None

        # Dataset Variables 

        # Network Variables
        self.network_names = None
        self.network_id = None
        self.network_name = None
        

        # Directory Variables
        self.png_dir = None
        self.base_dir = None
        self.metrics_dir = None
        self.checkpoint_dir = None
        self.record_dir = None
        self.config_dir = None
        self.results_dir = None
        self.exported_model_dir = None

        # Experiment Variables
        self.experiment_id = None
        self.exp_name = None
        self.exp_description = None 
        self.exp_status = None 
        self.exp_parameters = None
        self.line_nb = 0
        self.training_id = None
        self.annotation_type = None
        self.dict_annotations = {}
        self.train_list_id = None
        self.eval_list_id = None
        self.train_list = None
        self.eval_list = None
        self.index_url = None
        self.checkpoint_index = None
        self.checkpoint_data = None
        self.config_file = None
        self.model_selected = None
        self.label_path = None
        self.label_map = None
        self.urls = urls(self.host, self.auth)
        self.dataset = self.Dataset(self.host, self.auth)
        self.experiment = self.Experiment(self.host, api_token)
        self.network = self.Network(self.host, self.auth)
        self.project = self.Project(self.host, self.auth)
        self.interactive = interactive
        print(f"Hi {self.username}, welcome back.")

    class Experiment:

        def __init__(self, api_token=None, host="https://app.picsellia.com/sdk/", project_token=None, id=None, name=None, interactive=True):
            self.host = host
            self.auth = {"Authorization": "Token " + api_token}
            self.id = id
            self.experiment_name = name
            self.urls = urls(self.host, self.auth)
            self.interactive = interactive
            self.project_token = project_token

        def checkout(self, id=None, name=None, project_token=None, tree=False, with_file=False, with_data=False):
            identifier = None
            if self.id != None:
                identifier = self.id
            if id != None:
                identifier = id
            if self.project_token != None:
                if name != None:
                    identifier = name
            if project_token != None:
                self.project_token = project_token
                if name != None:
                    identifier = name
            if identifier == None:
                raise Exception('No corresponding experiment found, please enter a correct experiment id or a correct experiment name + project token')
            experiment = self.get(identifier, with_file=with_file, with_data=with_data)
            self.files = experiment["files"]
            self.data = experiment["data"]
            self.id = experiment["id"]
            self.experiment_name = experiment["name"]
            if tree:
                self.setup_dirs()
                if with_file:
                    for f in self.files:
                        object_name = f["object_name"]
                        name = f["name"]
                        filename = f["object_name"].split('/')[-1]
                        if f["large"]:
                            if name == 'checkpoint-data-latest':
                                self.dl_large_file(object_name, os.path.join(self.checkpoint_dir, filename))
                            elif name == 'model-latest':
                                self.dl_large_file(object_name, os.path.join(self.exported_model_dir, filename))
                            else:
                                self.dl_large_file(object_name, os.path.join(self.base_dir, filename))
                        else:
                            if name == 'config':
                                self.dl_file(object_name, os.path.join(self.config_dir, filename))
                            elif name == 'checkpoint-index-latest':
                                self.dl_file(object_name, os.path.join(self.checkpoint_dir, filename))
                            else:
                                self.dl_file(object_name, os.path.join(self.base_dir, filename))
            else:
                if with_file:
                    self.base_dir = self.experiment_name
                    self._create_dir(self.base_dir)
                    for f in self.files:
                        object_name = f["object_name"]
                        filename = f["object_name"].split('/')[-1]
                        if f["large"]:
                            self.dl_large_file(object_name, os.path.join(self.base_dir, filename))
                        else:
                            self.dl_file(object_name, os.path.join(self.base_dir, filename))
            return experiment


        def list(self, project_token=None):
            """[summary]

            Raises:
                exceptions.NetworkError: [description]
                exceptions.AuthenticationError: [description]

            Returns:
                [type]: [description]
            """
            assert project_token != None or self.project_token != None, "Please checkout a project or enter your project token on initialization"
            if self.project_token != None:
                token = self.project_token
            elif project_token != None:
                token = project_token
            try:
                r = requests.get(self.host + 'experiment/{}'.format(token), headers=self.auth)
            except Exception:
                raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
            
            if r.status_code != 200:
                raise exceptions.AuthenticationError(r.json()["error"])
            return r.json()["experiments"]

        def get(self, identifier, with_file=False, with_data=False):
            """[summary]

            Args:
                identifier ([type]): can be dataset_name (str) or uuid
            Raises:
                exceptions.NetworkError: [description]
                exceptions.AuthenticationError: [description]

            Returns:
                [type]: [description]
            """
            assert self.project_token != None, "Please checkout a project or enter your project token on initialization"
            data = {
                'with_file': with_file,
                'with_data': with_data
            }
            try:
                if is_uuid(identifier):
                    r = requests.get(self.host + 'experiment/{}/{}'.format(self.project_token, identifier), data,  headers=self.auth)
                else:
                    r = requests.get(self.host + 'experiment/{}/by_name/{}'.format(self.project_token, identifier), data, headers=self.auth)
            except Exception:
                raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
            
            if r.status_code != 200:
                raise exceptions.ResourceNotFoundError(r.json()["error"])

            return r.json()["experiment"][0]

        def create(self, name=None, description='', id=None, source=None):
            """[summary]

            Args:
                dataset_name ([str]): [description]
                description (str, optional): [description]. Defaults to "".
                private (bool, optional): [description]. Defaults to True.

            Raises:
                exceptions.NetworkError: [description]
                exceptions.ResourceNotFoundError: [description]

            Returns:
                [type]: [description]
            """
            data = json.dumps({
                "name": name,
                "description": description,
                "id": id,
                "source": source
            })
            try:
                r = requests.post(self.host + 'experiment/{}'.format(self.project_token), data=data, headers=self.auth)
            except Exception:
                raise exceptions.NetworkError(r.json()["error"])
            
            if r.status_code != 201:
                raise exceptions.ResourceNotFoundError(r.json()["error"])
            
            return r.json()

        def update(self, identifier, **kwargs):
            """[summary]

            Args:
                dataset_name ([str]): [description]
                description (str, optional): [description]. Defaults to "".
                private (bool, optional): [description]. Defaults to True.

            Raises:
                exceptions.NetworkError: [description]
                exceptions.ResourceNotFoundError: [description]

            Returns:
                [type]: [description]
            """
            data = json.dumps(kwargs)
            try:
                if is_uuid(identifier):
                    r = requests.patch(self.host + 'experiment/{}/{}'.format(self.project_token, identifier), data=data, headers=self.auth)
                else:
                    r = requests.patch(self.host + 'experiment/{}/by_name/{}'.format(self.project_token, identifier), data=data, headers=self.auth)
            except Exception:
                raise exceptions.NetworkError(r.json()["error"])
            
            if r.status_code != 201:
                raise exceptions.ResourceNotFoundError(r.json()["error"])
            
            return r.json()

        def delete(self, identifier):
            """[summary]

            Args:
                identifier ([type]): can be dataset_name (str) or uuid
            Raises:
                exceptions.NetworkError: [description]
                exceptions.AuthenticationError: [description]

            Returns:
                [type]: [description]
            """
            assert self.project_token != None, "Please checkout a project or enter your project token on initialization"
            try:
                if is_uuid(identifier):
                    r = requests.delete(self.host + 'experiment/{}/{}'.format(self.project_token, identifier), headers=self.auth)
                else:
                    r = requests.delete(self.host + 'experiment/{}/by_name/{}'.format(self.project_token, identifier), headers=self.auth)
            except Exception:
                raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
            
            if r.status_code != 200:
                raise exceptions.ResourceNotFoundError(r.json()["error"])

            return True

        def delete_all(self, project_token):
            """[summary]

            Raises:
                exceptions.NetworkError: [description]
                exceptions.AuthenticationError: [description]

            Returns:
                [type]: [description]
            """
            assert self.project_token != None, "Please checkout a project or enter your project token on initialization"
            try:
                r = requests.delete(self.host + 'experiment/{}'.format(self.project_token), headers=self.auth)
            except Exception:
                raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
            
            if r.status_code != 200:
                raise exceptions.AuthenticationError(r.json()["error"])
            return True
        
        def list_files(self, id=None):
            """[summary]

            Raises:
                exceptions.NetworkError: [description]
                exceptions.AuthenticationError: [description]

            Returns:
                [type]: [description]
            """
            assert self.id != None or id != None, "Please checkout an experiment or enter the desired experiment id"
            if self.id != None:
                id = self.id
            try:
                r = requests.get(self.host + 'experiment/{}/file'.format(id), headers=self.auth)
            except Exception:
                raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
            
            if r.status_code != 200:
                raise exceptions.AuthenticationError(r.json()["error"])
            return r.json()["files"]
        
        def delete_all_files(self, id=None):
            """[summary]

            Raises:
                exceptions.NetworkError: [description]
                exceptions.AuthenticationError: [description]

            Returns:
                [type]: [description]
            """
            assert self.id != None or id != None, "Please checkout an experiment or enter the desired experiment id"
            if self.id != None:
                id = self.id
            try:
                r = requests.delete(self.host + 'experiment/{}/file'.format(id), headers=self.auth)
            except Exception:
                raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
            
            if r.status_code != 200:
                raise exceptions.AuthenticationError(r.json()["error"])
            return True
        
        def create_file(self, id=None, name="", object_name="", large=False):
            """[summary]

            Args:
                dataset_name ([str]): [description]
                description (str, optional): [description]. Defaults to "".
                private (bool, optional): [description]. Defaults to True.

            Raises:
                exceptions.NetworkError: [description]
                exceptions.ResourceNotFoundError: [description]

            Returns:
                [type]: [description]
            """
            assert self.id != None or id != None, "Please checkout an experiment or enter the desired experiment id"
            if self.id != None:
                id = self.id
            data = json.dumps({ '0': {
                'name': name,
                'object_name': object_name,
                'large': large
            }
            })
            try:
                r = requests.put(self.host + 'experiment/{}/file'.format(id), data=data, headers=self.auth)
            except Exception:
                raise exceptions.NetworkError(r.json()["error"])
            
            if r.status_code != 201:
                raise exceptions.ResourceNotFoundError(r.json()["error"])
            
            return r.json()
        
        def get_file(self, id=None, name=None):
            """[summary]

            Raises:
                exceptions.NetworkError: [description]
                exceptions.AuthenticationError: [description]

            Returns:
                [type]: [description]
            """
            assert self.id != None or id != None, "Please checkout an experiment or enter the desired experiment id"
            if self.id != None:
                id = self.id
            assert name != None, "Please enter a valid file name"
            try:
                r = requests.get(self.host + 'experiment/{}/file/{}'.format(id, name), headers=self.auth)
            except Exception:
                raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
            
            if r.status_code != 200:
                raise exceptions.AuthenticationError(r.json()["error"])
            return r.json()["file"]

        def delete_file(self, id=None, name=None):
            """[summary]

            Raises:
                exceptions.NetworkError: [description]
                exceptions.AuthenticationError: [description]

            Returns:
                [type]: [description]
            """
            assert self.id != None or id != None, "Please checkout an experiment or enter the desired experiment id"
            if self.id != None:
                id = self.id
            assert name != None, "Please enter a valid file name"
            try:
                r = requests.delete(self.host + 'experiment/{}/file/{}'.format(id, name), headers=self.auth)
            except Exception:
                raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
            
            if r.status_code != 200:
                raise exceptions.AuthenticationError(r.json()["error"])
            return True
        
        def update_file(self, file_name=None, id=None, **kwargs):
            """[summary]

            Args:
                dataset_name ([str]): [description]
                description (str, optional): [description]. Defaults to "".
                private (bool, optional): [description]. Defaults to True.

            Raises:
                exceptions.NetworkError: [description]
                exceptions.ResourceNotFoundError: [description]

            Returns:
                [type]: [description]
            """
            assert self.id != None or id != None, "Please checkout an experiment or enter the desired experiment id"
            if self.id != None:
                id = self.id
            assert file_name != None, "Please enter a valid file name"
            data = json.dumps(kwargs)
            try:
                r = requests.patch(self.host + 'experiment/{}/file/{}'.format(id, file_name), data=data, headers=self.auth)
            except Exception:
                raise exceptions.NetworkError(r.json()["error"])
            
            if r.status_code != 201:
                raise exceptions.ResourceNotFoundError(r.json()["error"])
            
            return r.json()
        
        def list_data(self, id=None):
            """[summary]

            Raises:
                exceptions.NetworkError: [description]
                exceptions.AuthenticationError: [description]

            Returns:
                [type]: [description]
            """
            assert self.id != None or id != None, "Please checkout an experiment or enter the desired experiment id"
            if self.id != None:
                id = self.id
            try:
                r = requests.get(self.host + 'experiment/{}/data'.format(id), headers=self.auth)
            except Exception:
                raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
            
            if r.status_code != 200:
                raise exceptions.AuthenticationError(r.json()["error"])
            return r.json()["data_assets"]
        
        def delete_all_data(self, id=None):
            """[summary]

            Raises:
                exceptions.NetworkError: [description]
                exceptions.AuthenticationError: [description]

            Returns:
                [type]: [description]
            """
            assert self.id != None or id != None, "Please checkout an experiment or enter the desired experiment id"
            if self.id != None:
                id = self.id
            try:
                r = requests.delete(self.host + 'experiment/{}/data'.format(id), headers=self.auth)
            except Exception:
                raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
            
            if r.status_code != 200:
                raise exceptions.AuthenticationError(r.json()["error"])
            return True
        
        def create_data(self, id=None, name="", data={}):
            """[summary]

            Args:
                dataset_name ([str]): [description]
                description (str, optional): [description]. Defaults to "".
                private (bool, optional): [description]. Defaults to True.

            Raises:
                exceptions.NetworkError: [description]
                exceptions.ResourceNotFoundError: [description]

            Returns:
                [type]: [description]
            """
            assert self.id != None or id != None, "Please checkout an experiment or enter the desired experiment id"
            if self.id != None:
                id = self.id
            data = json.dumps({ '0': {
                'name': name,
                'data': data,
            }
            })
            try:
                r = requests.put(self.host + 'experiment/{}/data'.format(id), data=data, headers=self.auth)
            except Exception:
                raise exceptions.NetworkError(r.json()["error"])
            
            if r.status_code != 201:
                raise exceptions.ResourceNotFoundError(r.json()["error"])
            
            return r.json()
        
        def get_data(self, id=None, name=None):
            """[summary]

            Raises:
                exceptions.NetworkError: [description]
                exceptions.AuthenticationError: [description]

            Returns:
                [type]: [description]
            """
            assert self.id != None or id != None, "Please checkout an experiment or enter the desired experiment id"
            if self.id != None:
                id = self.id
            assert name != None, "Please enter a valid data asset name"
            try:
                r = requests.get(self.host + 'experiment/{}/data/{}'.format(id, name), headers=self.auth)
            except Exception:
                raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
            
            if r.status_code != 200:
                raise exceptions.AuthenticationError(r.json()["error"])
            return r.json()["data_asset"]

        def delete_data(self, id=None, name=None):
            """[summary]

            Raises:
                exceptions.NetworkError: [description]
                exceptions.AuthenticationError: [description]

            Returns:
                [type]: [description]
            """
            assert self.id != None or id != None, "Please checkout an experiment or enter the desired experiment id"
            if self.id != None:
                id = self.id
            assert name != None, "Please enter a valid data asset name"
            try:
                r = requests.delete(self.host + 'experiment/{}/data/{}'.format(id, name), headers=self.auth)
            except Exception:
                raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
            
            if r.status_code != 200:
                raise exceptions.AuthenticationError(r.json()["error"])
            return True
        
        def update_data(self, data_name=None, id=None, **kwargs):
            """[summary]

            Args:
                dataset_name ([str]): [description]
                description (str, optional): [description]. Defaults to "".
                private (bool, optional): [description]. Defaults to True.

            Raises:
                exceptions.NetworkError: [description]
                exceptions.ResourceNotFoundError: [description]

            Returns:
                [type]: [description]
            """
            assert self.id != None or id != None, "Please checkout an experiment or enter the desired experiment id"
            if self.id != None:
                id = self.id
            assert data_name != None, "Please enter a valid data asset name"
            data = json.dumps(kwargs)
            try:
                r = requests.patch(self.host + 'experiment/{}/data/{}'.format(id, data_name), data=data, headers=self.auth)
            except Exception:
                raise exceptions.NetworkError(r.json()["error"])
            
            if r.status_code != 201:
                raise exceptions.ResourceNotFoundError(r.json()["error"])
            
            return r.json()

        def _send_large_file(self, path=None, name=None, object_name=None, network_id=None, id=None):
            error_message = "Please checkout an experiment/network or enter the desired experiment id/network_id"
            assert self.id != None or id != None or network_id != None, error_message
            if self.id != None:
                id = self.id
            self.urls._init_multipart(object_name)
            parts = self.urls._upload_part(path, object_name)

            if self.urls._complete_part_upload(parts, object_name, None):
                self._create_or_update_file(name, path, id, object_name=object_name, large=True)

        def _send_file(self, path=None, name=None, object_name=None, network_id=None, id=None):
            error_message = "Please checkout an experiment/network or enter the desired experiment id/network_id"
            assert self.id != None or self.id != None or id != None or network_id != None, error_message
            if self.id != None:
                id = self.id
            response = self.urls._get_presigned_url(method='post', object_name=object_name, bucket_model=True)
            try:
                with open(path, 'rb') as f:
                    files = {'file': (path, f)}
                    http_response = requests.post(response['url'], data=response['fields'], files=files)
                if http_response.status_code == 204:
                    self._create_or_update_file(name, path, id, object_name=object_name, large=False)
            except Exception as e:
                raise exceptions.NetworkError(str(e))

        def log(self, name="", data={}, id=None):
            assert self.id != None or id != None, "Please checkout an experiment or enter the desired experiment id"
            if self.id != None:
                id = self.id
            stored = self.get_data(id, name)
            if stored == []:
                self.create_data(id, name, data)
            else:
                asset = stored[0]
                self.update_data(name, id, data=data)
            
        def _create_or_update_file(self, file_name="", path="", id=None, **kwargs):
            assert self.id != None or id != None, "Please checkout an experiment or enter the desired experiment id"
            if self.id != None:
                id = self.id
            stored = self.get_file(id, file_name)
            if stored == []:
                self.create_file(id, file_name, object_name, large)
            else:
                asset = stored[0]
                self.update_file(file_name=file_name, id=id, **kwargs)

        def store(self, name="", path=None, id=None, zip=False):
            assert self.id != None or id != None, "Please checkout an experiment or enter the desired experiment id"
            if self.id != None:
                id = self.id
            if path != None:
                filesize = Path(path).stat().st_size
                if filesize < 5*1024*1024:
                    filename = path.split('/')[-1]
                    object_name = os.path.join(id, filename)
                    self._send_file(path, name, object_name, None, id)
                else:
                    self._send_large_file(path, name, object_name, None, id)
            else:
                
                if name == 'config':
                    if not os.path.isfile(os.path.join(self.config_dir, "pipeline.config")):
                        raise FileNotFoundError("No config file found")
                    path = os.path.join(self.config_dir, "pipeline.config")
                    object_name = os.path.join(id, "pipeline.config")
                    self._send_file(path, name, object_name, None, id)
                elif name == 'checkpoint-data-latest':
                    file_list = os.listdir(self.checkpoint_dir)
                    ckpt_id = max([int(p.split('-')[1].split('.')[0]) for p in file_list if 'index' in p])
                    ckpt_data_file = None
                    for f in file_list:
                        if "{}.data".format(ckpt_id) in f:
                            ckpt_data_file = f
                    if ckpt_data_file is None:
                        raise exceptions.ResourceNotFoundError("Could not find matching data file with index")
                    path = os.path.join(self.checkpoint_dir, ckpt_data_file)
                    object_name = os.path.join(id, ckpt_data_file)
                    self._send_large_file(path, name, object_name, None, id)
                elif name == 'checkpoint-index-latest':
                    file_list = os.listdir(self.checkpoint_dir)
                    ckpt_id = max([int(p.split('-')[1].split('.')[0]) for p in file_list if 'index' in p])
                    ckpt_index = "model.ckpt-{}.index".format(ckpt_id)
                    path = os.path.join(self.checkpoint_dir, ckpt_index)
                    object_name = os.path.join(id, ckpt_index)
                    self._send_file(path, name, object_name, None, id)
                elif name == 'model-latest':
                    file_path = self.exported_model_dir
                    path = utils.zipdir(file_path)
                    object_name = os.path.join(id, 'saved_model.zip')
                    self._send_large_file(path, name, object_name, None, id)
            return object_name

        def dl_large_file(self, object_name, path):
            url = self.urls._get_presigned_url('get', object_name, bucket_model=True)
            with open(path, 'wb') as handler:
                filename = url.split('/')[-1]
                print("Downloading {}".format(filename))
                print('-----')    
                response = requests.get(url, stream=True)
                total_length = response.headers.get('content-length')
                if total_length is None:  # no content length header
                    print("Couldn't download {} file".format(filename))
                else:
                    dl = 0
                    count = 0
                    total_length = int(total_length)
                    for data in response.iter_content(chunk_size=4096):
                        dl += len(data)
                        handler.write(data)
                        done = int(50 * dl / total_length)
                        if self.interactive:
                            sys.stdout.write(f"\r[{'=' * done}{' ' * (50 - done)}]")
                            sys.stdout.flush()
                        else:
                            if count%500==0:
                                print('['+'='* done+' ' * (50 - done)+']')
                        count += 1
            print('--*--')
        
        def dl_file(self, object_name, path):
            url = self.urls._get_presigned_url('get', object_name, bucket_model=True)
            with open(path, 'wb') as handler:
                filename = url.split('/')[-1]
                response = requests.get(url, stream=True)
                total_length = response.headers.get('content-length')
                if total_length is None:  # no content length header
                    print("Couldn't download {} file".format(filename))
                else:
                    print("Downloading {}".format(filename))
                    for data in response.iter_content(chunk_size=1024):
                        handler.write(data)

        def setup_dirs(self):
            self.base_dir = self.experiment_name
            self.metrics_dir = os.path.join(self.base_dir, 'metrics')
            self.png_dir = os.path.join(self.base_dir, 'images')
            self.checkpoint_dir = os.path.join(self.base_dir, 'checkpoint')
            self.record_dir = os.path.join(self.base_dir, 'records')
            self.config_dir = os.path.join(self.base_dir, 'config')
            self.results_dir = os.path.join(self.base_dir, 'results')
            self.exported_model_dir = os.path.join(self.base_dir, 'exported_model')

            if not os.path.isdir(self.experiment_name):
                print("No directory for this project has been found, creating directory and sub-directories...")
                os.mkdir(self.experiment_name)

            self._create_dir(self.base_dir)
            self._create_dir(self.png_dir)
            self._create_dir(self.checkpoint_dir)
            self._create_dir(self.metrics_dir)
            self._create_dir(self.record_dir)
            self._create_dir(self.config_dir)
            self._create_dir(self.results_dir)
            self._create_dir(self.exported_model_dir)

        def _create_dir(self, dir_name):
            if not os.path.isdir(dir_name):
                os.mkdir(dir_name)

        def dl_annotations(self, option="all"):
            """ Download all the annotations made on Picsell.ia Platform for your project.
            Called when checking out a network
            Args:
                option (str): Define what type of annotation to export (accepted or all)

            Raises:
                NetworkError: If Picsell.ia server is not responding or host is incorrect.
                ResourceNotFoundError: If we can't find any annotations for that project.
            """

            print("Downloading annotations ...")

            try:
                to_send = {"project_token": self.project_token, "type": option}
                r = requests.get(self.host + 'download_annotations', data=json.dumps(to_send), headers=self.auth)
            except Exception:
                raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
            if r.status_code != 200:
                raise exceptions.ResourceNotFoundError("No annotations were found for this project")

            self.dict_annotations = r.json()

            if len(self.dict_annotations.keys()) == 0:
                raise exceptions.ResourceNotFoundError("You don't have any annotations")

        def dl_pictures(self):
            """Download your training set on the machine (Use it to dl images to Google Colab etc.)
            Save it to /project_id/images/*
            Perform train_test_split & send the repartition to Picsell.ia Platform

            Raises:
                ResourceNotFoundError : If no annotations in the Picsell.ia Client yet or images can't be downloaded"""

            if not hasattr(self, "dict_annotations"):
                raise exceptions.ResourceNotFoundError("Please dl_annotations model with dl_annotations()")

            if "images" not in self.dict_annotations.keys():
                raise exceptions.ResourceNotFoundError("Please run dl_annotations function first")

            print("Downloading images ...")

            if not os.path.isdir(self.png_dir):
                os.makedirs(self.png_dir)

            lst = []
            for info in self.dict_annotations["images"]:
                lst.append(info["external_picture_url"])
            t = len(set(lst))
            print('-----')
            nb_threads = 20
            infos_split = list(mlt.chunks(self.dict_annotations["images"], nb_threads))
            counter = Value('i', 0)
            p = Pool(nb_threads, initializer=mlt.pool_init, 
                initargs=(t, self.png_dir, counter,self.interactive,))
            p.map(mlt.dl_list, infos_split)
            print('--*--')
            print("Images downloaded")

        def generate_labelmap(self):
            """THIS FUNCTION IS MAINTAINED FOR TENSORFLOW 1.X
            ----------------------------------------------------------
            Genrate the labelmap.pbtxt file needed for Tensorflow training at:
                - project_id/
                    network_id/
                        training_id/
                            label_map.pbtxt
            Raises:
                ResourceNotFoundError : If no annotations in the Picsell.ia Client yet or images can't be downloaded
                                        If no directories have been created first."""

            print("Generating labelmap ...")
            if not hasattr(self, "dict_annotations") or not hasattr(self, "base_dir"):
                raise exceptions.ResourceNotFoundError("Please run create_network() or checkout_network() then dl_annotations()")

            self.label_path = os.path.join(self.base_dir, "label_map.pbtxt")

            if "categories" not in self.dict_annotations.keys():
                raise exceptions.ResourceNotFoundError("Please run dl_annotations() first")

            categories = self.dict_annotations["categories"]
            labels_Network = {}
            try:
                with open(self.label_path, "w+") as labelmap_file:
                    for k, category in enumerate(categories):
                        name = category["name"]
                        labelmap_file.write("item {\n\tname: \"" + name + "\"" + "\n\tid: " + str(k + 1) + "\n}\n")
                        # if self.project_type == 'classification':
                        #     labels_Network[str(k)] = name
                        # else:
                        labels_Network[str(k + 1)] = name
                    labelmap_file.close()
                print(f"Label_map.pbtxt created @ {self.label_path}")

            except Exception:
                raise exceptions.ResourceNotFoundError("No directory found, please call checkout_network() or create_network() function first")

            self.label_map = labels_Network

        def train_test_split(self, prop=0.8):

            if not hasattr(self, "dict_annotations"):
                raise exceptions.ResourceNotFoundError("Please download annotations first")

            if "images" not in self.dict_annotations.keys():
                raise exceptions.ResourceNotFoundError("Please download annotations first")

            self.train_list = []
            self.eval_list = []
            self.train_list_id = []
            self.eval_list_id = []
            self.index_url = utils.train_valid_split_obj_simple(self.dict_annotations, prop)

            total_length = len(self.dict_annotations["images"])
            for info, idx in zip(self.dict_annotations["images"], self.index_url):
                pic_name = os.path.join(self.png_dir, info['external_picture_url'])
                if idx == 1:
                    self.train_list.append(pic_name)
                    self.train_list_id.append(info["internal_picture_id"])
                else:
                    self.eval_list.append(pic_name)
                    self.eval_list_id.append(info["internal_picture_id"])

            print(f"{len(self.train_list_id)} images used for training and {len(self.eval_list_id)} images used for validation")

            label_train, label_test, cate = utils.get_labels_repartition_obj_detection(self.dict_annotations, self.index_url)

            # to_send = {"project_token": self.project_token,
            #         "train": {"train_list_id": self.train_list_id, "label_repartition": label_train, "labels": cate},
            #         "eval": {"eval_list_id": self.eval_list_id, "label_repartition": label_test, "labels": cate},
            #         "network_id": self.network_id, "training_id": self.training_id}

            # try:
            #     r = requests.post(self.host + 'post_repartition', data=json.dumps(to_send), headers=self.auth)
            #     if r.status_code != 201:
            #         raise exceptions.NetworkError('Can not send repartition to Picsell.ia Backend')
            #     print("Repartition sent ..")
            # except Exception:
            #     raise exceptions.NetworkError('Can not send repartition to Picsell.ia Backend')

    class Dataset:

        def __init__(self, host, auth, dataset_id=None):
            """[summary]

            Args:
                host ([type]): [description]
                auth ([type]): [description]
                dataset_id ([type], optional): [description]. Defaults to None.
            """
            self.host = host
            self.auth = auth 
            self.dataset_id = dataset_id
            # self.urls = urls(self.host, self.auth)

        ###########################################
        ###### DATASET ( LIST, GET, CREATE, DELETE)
        ###########################################

        def list(self):
            """[summary]
            List all your Datasets

            Raises:
                exceptions.NetworkError: [Server Not responding]
                exceptions.AuthenticationError: [Token Invalid]

            Returns:
                [dict]: [datasets infos]
            """
            try:
                r = requests.get(self.host + 'dataset', headers=self.auth)
            except Exception:
                raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
            
            if r.status_code != 200:
                raise exceptions.AuthenticationError('The project_token provided does not match any of the known project_token for your profile.')

            return r.json()

        def get(self, identifier=None):
            """[summary]

            Args:
                identifier ([type]): can be dataset_name (str) or uuid
            Raises:
                exceptions.NetworkError: [description]
                exceptions.AuthenticationError: [description]

            Returns:
                [type]: [description]
            """
            
            try:
                if is_uuid(identifier):
                    if self.dataset_id is not None:
                        r = requests.get(self.host + 'dataset/' + self.dataset_id, headers=self.auth)
                    else:
                        r = requests.get(self.host + 'dataset/' + identifier, headers=self.auth)
                else:
                    r = requests.get(self.host + 'dataset/by_name/' + identifier, headers=self.auth)
            except Exception:
                raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
            
            if r.status_code != 200:
                raise exceptions.ResourceNotFoundError(r.text)

            return r.json()

        def create(self, dataset_name: str, description="", private=True):
            """[summary]

            Args:
                dataset_name ([str]): [description]
                description (str, optional): [description]. Defaults to "".
                private (bool, optional): [description]. Defaults to True.

            Raises:
                exceptions.NetworkError: [description]
                exceptions.ResourceNotFoundError: [description]

            Returns:
                [type]: [description]
            """
            data = json.dumps({ "0": {
                'dataset_name': dataset_name,
                'description': description,
                'private': private
            }
            })
            try:
                r = requests.put(self.host + 'dataset', data=data, headers=self.auth)
            except Exception:
                raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
            
            if r.status_code != 201:
                raise exceptions.ResourceNotFoundError(r.text)
            
            print(f"Dataset {dataset_name} created.\nYou can attach Picture to it.")
            return r.json()

        def delete(self, identifier):

            try:
                if is_uuid(identifier):
                    r = requests.delete(self.host + 'dataset/' + identifier, headers=self.auth)
                else:
                    r = requests.delete(self.host + 'dataset/by_name/' + identifier, headers=self.auth)
            except Exception:
                raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
            
            if r.status_code != 200:
                raise exceptions.ResourceNotFoundError(r.text)

            return r.json()

        def update(self, identifier, **kwargs):
            try:
                if is_uuid(identifier):
                    r = requests.patch(self.host + 'dataset/' + identifier, data=json.dumps(kwargs), headers=self.auth)
                else:
                    r = requests.patch(self.host + 'dataset/by_name/' + identifier, data=json.dumps(kwargs),headers=self.auth)
            except Exception:
                raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
            
            if r.status_code != 201:
                raise exceptions.ResourceNotFoundError(r.text)
            
            print(f"Dataset {identifier} updated.")
            return r.json()


        #############################################
        ################# PICTURE ( ADD, DELETE )
        ##############################################
        def add_picture(self, identifier, **kwargs):
            try:
                if is_uuid(identifier):
                    r = requests.put(self.host + 'picture/' + identifier, data=json.dumps(kwargs), headers=self.auth)
                else:
                    r = requests.put(self.host + 'picture/by_name/' + identifier, data=json.dumps(kwargs),headers=self.auth)
            except Exception:
                raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
            
            if r.status_code != 201:
                raise exceptions.ResourceNotFoundError(r.text)
            
            # if self.interactive:
            #     print("Picture Uploaded")

            return r.json()
        
        ##########################################
        ########## ANNOTATION ( LIST, ADD, DELETE)
        ##########################################
        def list_annotation(self, project_id):
            try:
                if is_uuid(project_id):
                    r = requests.get(self.host + 'annotation/' + project_id, headers=self.auth)
                else:
                    print("Please provide a valid uuid")
                    return
            except Exception:
                raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
            
            if r.status_code != 200:
                raise exceptions.ResourceNotFoundError(r.text)
            
            return r.json()
            

        def add_annotation(self, project_id, picture_id, **kwargs):
            """[summary]

            Args:
                project_id ([type]): [description]
                picture_id ([type]): [description]
                annotation

            Raises:
                exceptions.NetworkError: [description]
                exceptions.ResourceNotFoundError: [description]

            Returns:
                [type]: [description]
            """
            try:
                if is_uuid(project_id) and is_uuid(picture_id):
                    r = requests.put(self.host + 'annotation/' + project_id + '/' + picture_id, data=json.dumps(kwargs), headers=self.auth)
                else:
                    print("Please provide a valid uuid")
                    return
            except Exception:
                raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
            
            if r.status_code != 201:
                raise exceptions.ResourceNotFoundError(r.text)
            
            return r.json()
        
        def delete_annotation(self, project_id, picture_id):
            """[summary]

            Args:
                project_id ([type]): [description]
                picture_id ([type]): [description]
                annotation

            Raises:
                exceptions.NetworkError: [description]
                exceptions.ResourceNotFoundError: [description]

            Returns:
                [type]: [description]
            """
            try:
                if is_uuid(project_id) and is_uuid(picture_id):
                    r = requests.delete(self.host + 'annotation/' + project_id + '/' + picture_id, headers=self.auth)
                else:
                    print("Please provide a valid uuid")
                    return
            except Exception:
                raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
            
            if r.status_code != 200:
                raise exceptions.ResourceNotFoundError(r.text)
            
            return r.json()

        def create_and_upload(self, dataset_name, img_dir, description="", private=True):

            ## Dataset creation ## 

            urls_utils = urls(self.host, self.auth)
            response = self.create(dataset_name=dataset_name, description=description, private=private)
            dataset_id = response["pk"]
            print(dataset_id)
            ## Upload Pictures ## 

            for i,imgpath in enumerate(os.listdir(img_dir)):
                try:
                    if i == 0:
                        files = {'file': open(os.path.join(img_dir, imgpath), 'rb')}
                        r = requests.put(url=self.host + "dataset/add_thumb/" + dataset_id, files=files, headers=self.auth)
                        if r.status_code != 202:
                            raise Exception(r.text)
                    internal_key = os.path.join(dataset_id, str(uuid4()))+ '.' + imgpath.split('.')[-1]
                    external_url = imgpath.split('/')[-1]    
                    width, height = Image.open(os.path.join(img_dir, imgpath)).size
                    response = urls_utils._get_presigned_url("post", object_name=internal_key)
                    with open(os.path.join(img_dir, imgpath), 'rb') as f:
                        r = requests.post(response["url"], data=response["fields"], files = {'file': (internal_key, f)})
                        print(r.status_code)
                        if r.status_code == 204:
                            self.add_picture(identifier=dataset_id, internal_key=internal_key, external_url=external_url, width=width, height=height)
                        else:
                            print(r.text)
                except Exception as e:
                    print("{} was not uploaded : {}".format(imgpath, str(e)))
                    continue

            


    class Network:

        def __init__(self, host, auth, network_id=None):
            """[summary]

            Args:
                host ([type]): [description]
                auth ([type]): [description]
                dataset_id ([type], optional): [description]. Defaults to None.
            """
            self.host = host
            self.auth = auth 
            self.network_id = network_id

        def list(self):
            """[summary]
            List all your Datasets

            Raises:
                exceptions.NetworkError: [Server Not responding]
                exceptions.AuthenticationError: [Token Invalid]

            Returns:
                [dict]: [datasets infos]
            """
            try:
                r = requests.get(self.host + 'network', headers=self.auth)
            except Exception:
                raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
            
            if r.status_code != 200:
                raise exceptions.AuthenticationError('The project_token provided does not match any of the known project_token for your profile.')

            return r.json()

        def get(self, identifier=None):
            """[summary]

            Args:
                identifier ([type]): can be dataset_name (str) or uuid
            Raises:
                exceptions.NetworkError: [description]
                exceptions.AuthenticationError: [description]

            Returns:
                [type]: [description]
            """
            
            try:
                if is_uuid(identifier):
                    if self.network_id is not None:
                        r = requests.get(self.host + 'network/' + self.network_id, headers=self.auth)
                    else:
                        r = requests.get(self.host + 'network/' + identifier, headers=self.auth)
                else:
                    r = requests.get(self.host + 'network/by_name/' + identifier, headers=self.auth)
            except Exception:
                raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
            
            if r.status_code != 200:
                raise exceptions.ResourceNotFoundError(r.text)

            return r.json()

        def create(self, **kwargs):
            """[summary]

            Args:
                dataset_name ([str]): [description]
                description (str, optional): [description]. Defaults to "".
                private (bool, optional): [description]. Defaults to True.

            Raises:
                exceptions.NetworkError: [description]
                exceptions.ResourceNotFoundError: [description]

            Returns:
                [type]: [description]
            """
            
            try:
                r = requests.put(self.host + 'dataset', data=json.dumps(kwargs), headers=self.auth)
            except Exception:
                raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
            
            if r.status_code != 201:
                raise exceptions.ResourceNotFoundError(r.text)
            
            print(f"Network created.\nYou can attach I to your experiment.")
            return r.json()

        def delete(self, identifier):

            try:
                if is_uuid(identifier):
                    if self.network_id is not None:
                        r = requests.delete(self.host + 'network/' + self.network_id, headers=self.auth)
                    else:
                        r = requests.delete(self.host + 'network/' + identifier, headers=self.auth)
                else:
                    r = requests.delete(self.host + 'network/by_name/' + identifier, headers=self.auth)
            except Exception:
                raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
            
            if r.status_code != 200:
                raise exceptions.ResourceNotFoundError(r.text)

            return r.json()

        def update(self, identifier, **kwargs):
            try:
                if is_uuid(identifier):
                    if self.network_id is not None:   
                        r = requests.patch(self.host + 'network/' + self.network_id, data=json.dumps(kwargs), headers=self.auth)
                    else:
                        r = requests.patch(self.host + 'network/' + identifier, data=json.dumps(kwargs), headers=self.auth)
                else:
                    r = requests.patch(self.host + 'network/by_name/' + identifier, data=json.dumps(kwargs),headers=self.auth)
            except Exception:
                raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
            
            if r.status_code != 201:
                raise exceptions.ResourceNotFoundError(r.text)
            
            print(f"Network {identifier} updated.")
            return r.json()

    class Project:

        def __init__(self, host, auth, project_id=None):
            """[summary]

            Args:
                host ([type]): [description]
                auth ([type]): [description]
                dataset_id ([type], optional): [description]. Defaults to None.
            """
            self.host = host
            self.auth = auth 
            self.project_id = project_id
            self.worker = self.Worker(host=self.host, auth= self.auth, project_id=self.project_id)

        def list(self):
            """[summary]
            List all your Datasets

            Raises:
                exceptions.NetworkError: [Server Not responding]
                exceptions.AuthenticationError: [Token Invalid]

            Returns:
                [dict]: [datasets infos]
            """
            try:
                r = requests.get(self.host + 'project', headers=self.auth)
            except Exception:
                raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
            
            if r.status_code != 200:
                raise exceptions.AuthenticationError('The project_token provided does not match any of the known project_token for your profile.')

            return r.json()

        def delete(self):
            try:
                r = requests.delete(self.host + 'project', headers=self.auth)
            except Exception:
                raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
            
            if r.status_code != 200:
                raise exceptions.AuthenticationError('The project_token provided does not match any of the known project_token for your profile.')

            return r.json()

        def create(self, **kwargs):
            try:
                r = requests.put(self.host + 'project', data=json.dumps(kwargs), headers=self.auth)
            except Exception:
                raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
            
            if r.status_code != 201:
                raise Exception(r.text)

            return r.json()

        def update(self, identifier, **kwargs):
            try:
                if is_uuid(identifier):
                    if self.project_id is not None:   
                        r = requests.patch(self.host + 'project/' + self.project_id, data=json.dumps(kwargs), headers=self.auth)
                    else:
                        r = requests.patch(self.host + 'project/' + identifier, data=json.dumps(kwargs), headers=self.auth)
                else:
                    r = requests.patch(self.host + 'project/by_name/' + identifier, data=json.dumps(kwargs),headers=self.auth)
            except Exception:
                raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
            
            if r.status_code != 201:
                raise exceptions.ResourceNotFoundError(r.text)
            
            print(f"Project {identifier} updated.")
            return r.json()

        class Worker:

            def __init__(self, host, auth, project_id=None):
                """[summary]

                Args:
                    host ([type]): [description]
                    auth ([type]): [description]
                    dataset_id ([type], optional): [description]. Defaults to None.
                """
                self.host = host
                self.auth = auth 
                self.project_id = project_id

            def list(self, identifier):
                try:
                    if is_uuid(identifier):
                        if self.project_id is not None:   
                            r = requests.get(self.host + 'worker/' + self.project_id,  headers=self.auth)
                        else:
                            r = requests.get(self.host + 'worker/' + identifier,  headers=self.auth)
                    else:
                        r = requests.get(self.host + 'worker/by_project_name/' + identifier, headers=self.auth)
                except Exception:
                    raise exceptions.NetworkError("Server is not responding, please check your host or Picsell.ia server status on twitter")
            
                if r.status_code != 200:
                    raise exceptions.ResourceNotFoundError(r.text)
    
                return r.json()

            

if __name__ == '__main__':

    clt = Client(api_token="41c608cc6868a575ef6d6255b2e632f7b052e4df")
    image_id = "29100e71-b121-40b6-8121-b2d9610a91fd"
    project_id = "d9d569c6-3c7d-4e86-9d54-13b5044674aa"
    network_name = "ds5ddde"
    network_id = "df4266c1-92ac-480a-8f5a-80f7f69c360a"
    # print(clt.dataset.add_picture("blablabla", external_key="coucosu", internal_key="salsut", height=100, width=200))
    # print(clt.dataset.create(dataset_name="helslo", description="coucou", private=False))
    # print(clt.dataset.delete('9af58e19-04c1-4c93-a3b0-2a323a57e6aa'))
    # print(clt.dataset.list_annotation('d9d569c6-3c7d-4e86-9d54-13b5044674aa'))
    # ann = [
    #     {"qa": [], "type": "rectangle", "label": "addd", "rectangle": {"top": 47.44248485353728, "left": 111.66851948740212, "width": 60.61529933481154, "height": 99.5288248337029}}
    # ]

    
    # clt.dataset.delete_annotation(project_id, image_id)
    # print(clt.project.worker.create(identifier="d9d569c6-3c7d-4e86-9d54-13b5044674aa", is_active=True, role="manager", username="tibl"))

    clt.dataset.create_and_upload(dataset_name="testUpload", img_dir="/home/tibz/Pictures/TO_SEND", description="test it all")