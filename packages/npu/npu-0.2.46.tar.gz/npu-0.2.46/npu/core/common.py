import hashlib
import math
import requests
from bson import ObjectId
from tqdm import tqdm
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
from datetime import datetime

from .Model import Model
from .DataLoader import DataLoader
from .Dataset import Dataset
from .saving.saving import save_data, determine_model, TF_str, mxnet_str, pytorch_str
from .web.urls import TOKEN_URL, HASH_URL, UPLOAD_DATA_URL


VERBOSITY = 1
MIN_VERBOSITY = 1
MID_VERBOSITY = 2
FULL_VERBOSITY = 3

_token = ""
_project = ""

utcnow = datetime.utcnow

# from SO
class bcolors:
    PURPLE = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ORANGE = '\33[38;5;208m'


levels = {"WARNING": bcolors.ORANGE, "INFO": bcolors.PURPLE}

NEURO_AI_STR = f"[{bcolors.OKBLUE}Neuro Ai{bcolors.ENDC}]"


def api(token_, project_name, verbosity):
    global _token
    global  _project
    global VERBOSITY
    _token = token_
    VERBOSITY = verbosity
    if VERBOSITY != MIN_VERBOSITY:
        npu_print(f"Verbosity level set to {VERBOSITY}")
    params = {"token": _token, "project_name": project_name}
    response = requests.get(TOKEN_URL, params=params)
    if response.status_code == 200:
        npu_print("Token successfully authenticated")
        _project = response.json()
        npu_print(f"Using project: {project_name}")
        return response
    else:
        raise ValueError(response.text)
    # "API token not valid"


def getToken():
    return _token


def getVerbosity():
    return VERBOSITY


def get_project():
    return _project


def getResponse(response):
    try:
        return response.json()
    except Exception as e:
        raise ConnectionError("Invalid response received. Error: {}".format(response.text))


# https://stackoverflow.com/questions/5194057/better-way-to-convert-file-sizes-in-python
def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


def add_kwargs_to_params(params, **kwargs):
    params = {**params, **kwargs}
    return params


def read_in_chunks(file_object, chunk_size=1024):
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1k."""
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data


def checkModel(model):
    from .Task import Task
    from .Model import Model
    if not isinstance(model, Task) and not isinstance(model, str) and not isinstance(model, Model):
        raise ValueError("Model is not a valid format. Please make sure you've compiled it first.")


def check_model_type(model, params):
    from .Task import Task
    if isinstance(model, Model):
        params["model_name"] = model.name
        params["model_attr"] = model.attr
    elif isinstance(model, str) and not ObjectId.is_valid(model):
        params["model_name"] = model
    elif model != "" and not isinstance(model, Task):
        params["modelId"] = model


def check_data_type(data, param_name, params):
    from .Task import Task
    if isinstance(data, Dataset):
        params[param_name + "_name"] = data.id
    elif isinstance(data, str) and not ObjectId.is_valid(data):
        params[param_name + "_name"] = data
    elif data != "" and not isinstance(data, Task):
        params[param_name + "Id"] = data


def check_data(data, name=""):
    if not isinstance(name, str):
        raise ValueError("Name given is not valid. Please supply a string.")
    if isinstance(data, (str, dict)):
        return data
    elif isinstance(data, Dataset):
        return data
    elif isinstance(data, DataLoader):
        response = upload_data_loader(data, name)
    else:
        response = upload_data(data, name)
    status_code = response.status_code
    if status_code not in (204, 200, 201):
        raise ConnectionAbortedError("Data upload has not worked: {}".format(response.content))
    if status_code != 204:
        response = getResponse(response)
    if isinstance(response, dict) and status_code == 200:
        message = response.get("message")
        npu_print(message)
        response = response["id"]
    return response


def sliceData(data):
    id = data["id"]
    x = data["indexes"]
    y = None
    if isinstance(x, slice):
        y = x.stop
        x = x.start
    return id, x, y


def gen(dl):
    for data_part in dl.numpy():
        yield save_data(data_part)


def create_callback(encoder):
    encoder_len = encoder.len
    bar = tqdm(desc=f"{NEURO_AI_STR} Uploading", unit="B", unit_scale=True, total=encoder_len, unit_divisor=1024)

    def callback(monitor):
        bar.n = monitor.bytes_read
        bar.refresh()
        if monitor.bytes_read == encoder_len:
            bar.close()
    return callback


def get_progress_bar_uploader(file):
    encoder = create_upload(file)
    callback = create_callback(encoder)
    monitor = MultipartEncoderMonitor(encoder, callback)
    return monitor


def create_upload(file):
    return MultipartEncoder({
        'file': ('file', file, 'application/octet-stream', {'Content-Transfer-Encoding': 'binary'}),
    })


def upload_data_loader(dl, name=""):
    if VERBOSITY >= MID_VERBOSITY:
        npu_print("Hashing data locally...")
    hash, size, length = dl.hash()
    params = {"token": getToken(), "hash": hash, "collection": 1, "chunked": True, "is_last": False, "size": size,
              "given_name": name, "input_shape": dl.shape, "project": get_project()}
    # params = {"token": getToken(), "hash": hash, "collection": 1, "size": size, "given_name": name}
    npu_print("Checking if data is on servers...")
    response = requests.get(HASH_URL, params=params)
    if response.status_code == 200:
        if VERBOSITY >= MID_VERBOSITY:
            npu_print("Data already uploaded. Will not reupload.")
        return response
    npu_print("Data not on servers. Starting to upload. Total size of data is {}".format(convert_size(size)))
    if length == 1:
        return upload_data(next(dl.numpy()), name)
    npu_print("{} chunks to upload...".format(length))
    for i, data_part in enumerate(dl.numpy()):
        if VERBOSITY >= MID_VERBOSITY:
            npu_print("Uploading chunk {} out of {}...".format(i + 1, length))
        if i == length - 1:
            params["is_last"] = True
        file = save_data(data_part)
        monitor = get_progress_bar_uploader(file)
        response = requests.post(UPLOAD_DATA_URL, data=monitor,
                                 headers={'Content-Type': monitor.content_type}, params=params)
    return response


def upload_data(data, name=""):
    if VERBOSITY >= FULL_VERBOSITY:
        npu_print("Saving data locally...")
    if isinstance(data, str):
        file = open(data, "rb")
    else:
        file = save_data(data)
    if VERBOSITY >= FULL_VERBOSITY:
        npu_print("Hashing...")
    hash = hashlib.md5()
    for piece in read_in_chunks(file):
        hash.update(piece)
    size = file.tell()
    hash = hash.hexdigest()
    npu_print("Checking if data is on servers...")
    params = {"token": getToken(), "hash": hash, "collection": 1, "given_name": name, "project": get_project()}
    response = requests.get(HASH_URL, params=params, json=params)
    if response.status_code == 200:
        if VERBOSITY >= MID_VERBOSITY:
            npu_print("Data already on servers. Returning result...")
        file.close()
        return response
    npu_print("Data not found on servers. Total size of data is {}. Uploading now...".format(convert_size(size)))
    file.seek(0)

    monitor = get_progress_bar_uploader(file)
    response = requests.post(UPLOAD_DATA_URL, data=monitor,
                             headers={'Content-Type': monitor.content_type}, params=params, json=params)
    if isinstance(data, str):
        file.close()
    return response


def upload_sample(data, params):
    required = (len(data[0]) if isinstance(data, (tuple, list)) else len(data)) > 10
    if not required:
        return False
    data = [d[:10] for d in data] if isinstance(data, (tuple, list)) else data[:10]


def hashData(data):
    pass


def validate_model(model, data):
    library = determine_model(model)
    if isinstance(data, str):
        return
    # data = convert_to_numpy(data)
    if library == pytorch_str:
        from torch import ones
    elif library == mxnet_str:
        from mxnet import nd
        ones = nd.ones
    elif library == TF_str:
        from numpy import ones
    else:
        return
        # raise ValueError("Cannot validate library: {} .".format(library))
    placeholder_data = ones(data.shape)
    model(placeholder_data)


def determine_data(data):
    start = end = None
    name = ""
    if isinstance(data, dict):
        data, start, end = sliceData(data)
    if isinstance(data, Dataset):
        name = data.id
        data = data
    return data, name, start, end


def npu_print(val, level="INFO"):

    log_str = f"{NEURO_AI_STR} {utcnow_formatted()} - [{levels[level]}{level}{bcolors.ENDC}]: {val}"
    print(f"{log_str}")


def utcnow_formatted():
    return utcnow().strftime("%H:%M:%S")
