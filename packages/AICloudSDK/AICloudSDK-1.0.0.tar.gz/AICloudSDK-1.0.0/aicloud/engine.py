import zipfile
import time
import os
import tarfile
import uuid

from aicloud.cloudapi import AIPlatform
import json
import sys
import io
#sys.stdout = sys.__stdout__ = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8', line_buffering=True)
#sys.stderr = sys.__stderr__ = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8', line_buffering=True)



class AlgorithmEngine(object):

    def __init__(self):
        self.token = os.environ.get('token')
        self.auth_token = os.environ.get('authToken')
        self.user_id = os.environ.get('userId')
        self.train_id = os.environ.get('trainId')
        self.base_url = os.environ.get('baseUrl')
        self.ai_platform = AIPlatform(base_url=self.base_url, authorization=self.token, auth_token=self.auth_token)
        self.nbid = os.environ.get('nbid')

    def upload_model(self, source_dir, target_dir=None):
        """
        upload model file to cloud storage
        :param source_dir: source directory of model files
        :param target_dir: target directory to zip model files
        :return:
        """
        target_file = target_dir + str(uuid.uuid1()) + ".tar" if target_dir else str(uuid.uuid1()) + ".tar"
        with tarfile.open(target_file, "w:") as tar:
            tar.add(source_dir, arcname=os.path.basename(source_dir))

        file = open(target_file, 'rb')
        code, header, body = self.ai_platform.upload_model_file(user_id=self.user_id,
                                                                train_id=self.train_id,
                                                                nbid=self.nbid,
                                                                model_file=file)
        #msg = 'upload model file successfully' if code == 200 else 'upload model file failed'
        if code is not 200:
            msg = 'upload model file failed'
            return code, msg 
        if json.loads(str(body.content, encoding = "utf-8"))['code'] == '0':
            msg = 'upload model file successfully'
        else:
             msg = json.loads(str(body.content, encoding = "utf-8"))
        # delete tar package
        file.close()
        os.remove(target_file)
        return msg

    def download_model(self, local_model_path):
        """
        download model file from cloud storage
        :param local_model_path: local storage path
        :return:
        """
        code, header, body = self.ai_platform.download_model_file(train_id=self.train_id)
        if code is not 200:
            msg = 'download model file failed'
            return code, msg
        if json.loads(str(body.content, encoding = "utf-8"))['code'] == '0':
            msg = 'download model file successfully'
        else:
             msg = json.loads(str(body.content, encoding = "utf-8"))
        #msg = 'download model file successfully'
        now_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
        file_absolute_path = local_model_path + '/' + now_time + '.tar'
        try:
            with open(file_absolute_path, "wb") as f:
                f.write(body.content)

            tar = tarfile.open(file_absolute_path)
            tar.extractall(local_model_path)
            tar.close()
        except Exception as ex:
            return 500, ex

        if os.path.exists(file_absolute_path):
            os.remove(file_absolute_path)

        return code, msg

    def create_training_task(self, name, log_path, description=None):
        """
        create training task, then can find in training list
        training task include name, description, version, dataset
        version is generated automatically associated with project, project is from env
        dataset is training dataset from env
        :param name: traitr(body.content, encoding = "utf-8")ing task name
        :param description: description of the task
        :return:
        """
        #test_url = self.base_url + '/ai/api/v1/training/training/form'
        code, header, body = self.ai_platform.save_model_info(name, log_path, self.nbid)
        if code is not 200:
            msg = 'create training task failed'
            return code, msg
        if json.loads(str(body.content, encoding = "utf-8"))['code'] == '0':
            msg = 'create training successfully'
            train_id = json.loads(str(body.content, encoding = "utf-8"))['result']['data']['trainingId']
            with open('/workspace/trainid.txt', 'w') as file:
                file.write(str(train_id))
        else:
            msg = json.loads(str(body.content, encoding = "utf-8"))
        return msg
    def create_training_duration(self):
        #url = self.base_url + '/ai/api/v1/training/finish/form/'
        code, header, body = self.ai_platform.training_duration_info()
        if code is not 200:
            msg = 'create training duration failed'
            return code, msg
        if json.loads(str(body.content, encoding = "utf-8"))['code'] == '0':
            msg = 'create training duration successfully'
        else:
             msg = json.loads(str(body.content, encoding = "utf-8"))
        return  msg




