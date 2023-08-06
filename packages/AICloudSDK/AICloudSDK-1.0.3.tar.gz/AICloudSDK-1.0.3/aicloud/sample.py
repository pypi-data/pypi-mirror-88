#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time           : 20-4-28 下午1:07
# @Author         : Shen Bin
# @File           : sample.py
# @Product        : PyCharm
# @Docs           :
# @Source         :

from aicloud.engine import AlgorithmEngine

ae = AlgorithmEngine()
#download model from cloud
#code, msg = ae.download_model('.')

# upload model to cloud
#msg = ae.upload_model('./test.txt')

#print(code,msg)
#create training task
#msg = ae.create_training_task('training_name', '/path/log2')
#print(msg)
#create training duration
msg = ae.create_training_duration()
print( msg)



