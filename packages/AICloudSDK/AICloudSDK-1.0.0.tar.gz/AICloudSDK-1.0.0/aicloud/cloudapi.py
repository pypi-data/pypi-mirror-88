#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time           : 20-4-27 下午4:05
# @Author         : Shen Bin
# @File           : cloudapi.py
# @Product        : PyCharm
# @Docs           :
# @Source         :
from aicloud.rest import get, post, put
import json
import os

class AIPlatform(object):

    model_upload_path = '/model/file'
    model_download_path = '/model/download/modelfile'
    create_training_task = '/training/training/form'
    create_training_duration = '/training/finish/form/'    
    def __init__(self, base_url, version='v1', authorization=None, auth_token=None):
        self.authorization = authorization
        self.auth_token = auth_token
        self.url = base_url.rstrip('/') + '/ai/api/' + version
        self.train_id_file = '/workspace/trainid.txt'
    def _make_token_headers(self, content_type=None):
        headers = {
            'Authorization': self.authorization,
            'auth-token': self.auth_token
        }
        if content_type:
            headers['Content-Type'] = content_type

        return headers

    def upload_model_file(self, user_id, train_id, nbid, model_file):
        """
        upload model file to cloud storage
        :param user_id: user id
        :param train_id: training id
        :param model_file: model file by training
        :return:
        """
        if os.path.exists(self.train_id_file):
            with open(self.train_id_file) as f:
                train_id = f.readline()

        url = self.url + self.model_upload_path
        file = {'multipartFile': model_file}
     
        data = {
            'trainingId': train_id,
            'userId': user_id,
            'nbid': nbid
        }

        return post(url, headers=self._make_token_headers(), data=data, files=file)

    def download_model_file(self, train_id):
        """
        download model file from cloud storage
        :param train_id: training id
        :return:
        """
        url = self.url + self.model_download_path
        params = {'trainingId': train_id}

        return get(url, headers=self._make_token_headers(), params=params)
    def save_model_info(self, training_name, log_path,  nbid):
        """
        :param training_name:
        :param nbid:
        :param task_url:
        :return:
        """
        url = self.url + self.create_training_task
        data = {
            'trainingName': training_name,
            'notebookId': nbid,
            'logAddr': log_path
        }

        return post(url, headers=self._make_token_headers(content_type='application/json'), data=json.dumps(data))
    
    def training_duration_info(self):
        if os.path.exists(self.train_id_file):
            with open(self.train_id_file) as f:
                train_id = f.readline()
                url = self.url + self.create_training_duration + str(train_id)
        return put(url, headers=self._make_token_headers())     


class StorageEngine(object):
    pass
