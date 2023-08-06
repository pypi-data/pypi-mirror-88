import os
import base64
import time
import sys
import traceback
import logging
import json
import requests
from aicloud.utils import RedisClient
import io
import importlib
import aicloud.settings as settings

# root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
root = os.path.abspath(os.path.dirname(os.getcwd()))
sys.path.append(root)
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
                    datefmt="%Y-%M-%d %H:%M:%S")


def __insert_redis(param_path, src_redis):
    images_path = os.listdir(param_path)
    images_dict = {}
    count = 0
    # 10 images are default
    for image_path in images_path:
        try:
            if count < 10:
                absolute_image_path = os.path.join(param_path, image_path)
                logging.info(
                    "__insert_redis image path:{0} count:{1} ".format(absolute_image_path, count))
                with open(absolute_image_path, 'rb') as f:
                    images_dict[image_path] = f.read()
                count += 1
        except Exception:
            logging.error(traceback.format_exc())
    now_time_key = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    src_batch_id = now_time_key + "_debug_image"
    src_redis.hmset(src_batch_id, images_dict)
    return src_batch_id


def simple_inference(infer_rlt_redis_dict=settings.DEBUG_INFER_RLT_REDIS,
                     is_debug=True, module_path=None, images_path=None):
    logging.info(
        'simple_inference input0 infer_rlt_redis_dict: {0} is_debug: {1} module_path: {2} images_path: {3}'.format(
            infer_rlt_redis_dict, is_debug, module_path, images_path))
    # defaults
    debug_src_redis_dict = settings.DEBUG_SRC_REDIS_DICT
    engine_class_name = settings.ENGINE_CLASS_NAME
    load_model_method_name = settings.LOAD_MODEL_METHOD_NAME
    inference_method_name = settings.INFERENCE_METHOD_NAME
    release_method_name = settings.RELEASE_GPU_RES_METHOD_NAME

    if is_debug:
        if images_path:
            # debug algorithm in notebook
            src_redis = RedisClient(debug_src_redis_dict["redis_host"], debug_src_redis_dict["password"],
                                    debug_src_redis_dict["db"])
            src_batch_id = __insert_redis(images_path, src_redis)
            result_key = src_batch_id + '_result_key'
            progress_key = src_batch_id + '_progress_key'
            result_redis = RedisClient(infer_rlt_redis_dict["redis_host"], infer_rlt_redis_dict["password"],
                                       infer_rlt_redis_dict["db"])
        else:
            logging.error('there is no images_path in debug mode')
            return
    else:
        src_batch_id = settings.SRC_BATCH_ID
        result_key = settings.RESULT_KEY
        progress_key = settings.PROGRESS_KEY
        src_redis = RedisClient(settings.SRC_REDIS_HOSTS, settings.SRC_REDIS_PASSWORD, settings.SRC_REDIS_DB)
        result_redis = RedisClient(settings.DST_REDIS_HOSTS, settings.DST_REDIS_PASSWORD, settings.DST_REDIS_DB)

    if not module_path:
        logging.error("no module_path")
        return
    else:
        alg_module = importlib.import_module(module_path)

    infer_engine = getattr(alg_module, engine_class_name)()
    logging.info('__init__ method  executed')
    load_model_func = getattr(infer_engine, load_model_method_name)
    load_model_func()
    logging.info('load_model method executed')

    count = 0
    if is_debug or settings.INFERENCE_TYPE == '1':
        # recoder progress count
        key = src_redis.hkeys(src_batch_id)
        if len(key) == 0:
            logging.error('no source data found')
        now_time_str = time.strftime("%Y%m%d_%H%M%S", time.localtime())
        for i in range(len(key)):
            logging.info('batch inference start count is:' + str(count))
            # read image from redis and encode
            data = src_redis.hget(src_batch_id, key[i])
            base64_data = base64.b64encode(data).decode()
            result_json = __one_pic_inference__(infer_engine, inference_method_name, base64_data)
            # store inference result and progress in redis
            # we will not process exception about the redis in order to restart automatically
            count = count + 1
            result_redis.hset(result_key, str(key[i], encoding="utf-8"), json.dumps(result_json))
            result_redis.set(progress_key, count)
            if is_debug:
                # write debug result
                result_file_full_name = os.getcwd() + "/" + now_time_str + "_debug_result"
                with open(result_file_full_name, 'a+') as f:
                    f.write(json.dumps(result_json) + "\n\n")
                logging.info('your debug result has been written to' + result_file_full_name)
    elif settings.INFERENCE_TYPE == '0':
        # single pic inference
        logging.info('batch inference single pic start ')
        base64_data = src_redis.get(src_batch_id)
        result_json = __one_pic_inference__(infer_engine, inference_method_name, base64_data)
        result_redis.set(result_key, json.dumps(result_json))
        count = count + 1

    # post process
    if is_debug:
        src_redis.delete(src_batch_id)
        result_redis.expire(result_key, 3600)
    else:
        # release GPU quotas
        try:
            release_func = getattr(infer_engine, release_method_name)
            release_func()
            tmpUrl = os.getenv("releaseQuotaUrl")
            url = tmpUrl + str(count)
            logging.info('releaseQuotaUrl url:{}'.format(url))
            r = requests.get(url)
            msg = 'ai successfully' if r.status_code == 200 else 'ai failed'
            logging.info(msg)
        except:
            logging.error(traceback.format_exc())


def __one_pic_inference__(infer_engine, inference_method_name, base64_data):
    result_json = {}
    try:
        t1 = time.time()
        infer_func = getattr(infer_engine, inference_method_name)
        result = infer_func(base64_data)
        t2 = time.time()
        infer_time = t2 - t1
        result_json = json.loads(result)
        # add inference time
        result_json['infer_time'] = infer_time
    except:
        logging.error(traceback.format_exc())
        result_json['msg'] = traceback.format_exc()
    return result_json


if __name__ == '__main__':
    simple_inference(is_debug=False, module_path=settings.ENGINE_MODULE_PATH)