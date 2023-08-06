import requests

from .Dataset import Dataset
from .Task import Task
from .common import getToken, check_data, add_kwargs_to_params, checkModel, determine_data, validate_model, \
    check_model_type, check_data_type, get_project
from .web.urls import PREDICT_URL


def predict(model, data, asynchronous=False, callback=None, **kwargs):
    checkModel(model)
    # if isinstance(model, Task) and model.cache is not None and "model" in model.cache:
    #     cached_model = model.cache["model"]
    #     if not isinstance(data, (str, Dataset, dict)):
    #         validate_model(cached_model, data)
    inference_data = check_data(data)
    task_id = model.task_id if isinstance(model, Task) else ""
    resp = predictApi(model, inference_data, task_id, **kwargs)
    task = Task(resp.json(), callback)
    if not asynchronous:
        task.wait()
    return task


def predictApi(model, data, task_id, **kwargs):
    data, data_name, start, end = determine_data(data)
    params = {"token": getToken(), "task_id": task_id, "data_start": start, "data_end": end,
              "data_name": data_name, "project": get_project()}
    check_model_type(model, params)
    check_data_type(data, "data", params)
    params = add_kwargs_to_params(params, **kwargs)
    response = requests.get(PREDICT_URL, params=params)
    if response.status_code != 200:
        raise ValueError(response.text)
    return response


