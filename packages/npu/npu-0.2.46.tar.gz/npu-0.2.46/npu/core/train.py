import base64

import dill
import requests

from .Task import Task
from .common import getToken, check_data, add_kwargs_to_params, checkModel, determine_data, check_model_type, \
    check_data_type, get_project, npu_print
from .web.urls import TRAIN_URL


def train(model, train_data, val_data, batch_size, epochs, optimiser, loss, metrics, trained_model_name, asynchronous,
          callback, **kwargs):
    checkModel(model)
    train_data = check_data(train_data)
    val_data = check_data(val_data)
    task_id = model.task_id if isinstance(model, Task) else ""
    task = Task(trainApi(model, train_data, val_data, batch_size, epochs, optimiser, loss, metrics, trained_model_name,
                         task_id, **kwargs).json(), callback)
    if not asynchronous:
        task.wait()
        npu_print("Model finished training")
    return task


def trainApi(model, train_data, val_data, batch_size, epochs, optimiser, loss, metrics, trained_model_name, task_id="",
             **kwargs):
    if not isinstance(trained_model_name, str):
        raise ValueError("Name given is not valid. Please supply a string.")
    train_data, train_name, train_start, train_end = determine_data(train_data)
    val_data, test_name, test_start, test_end = determine_data(val_data)
    if callable(loss):
        npu_print("Using custom loss function... {}".format(loss.__name__ if hasattr(loss, "__name__")
                                                                    else loss.__class__.__name__))
        loss = base64.urlsafe_b64encode(dill.dumps(loss))
    for i, m in enumerate(metrics):
        if callable(m) or mxnet_metric(m):
            npu_print("Serialising custom metric function... {}".format(m.__name__ if hasattr(m, "__name__")
                                                                    else m.__class__.__name__))
            metrics[i] = base64.urlsafe_b64encode(dill.dumps(m))
    params = {"loss": loss,
              "token": getToken(), "batch_size": batch_size, "epochs": epochs, "task_id": task_id,
              "train_start": train_start, "train_end": train_end, "test_start": test_start,
              "test_end": test_end, "train_name": train_name, "test_name": test_name,
              "trained_model_name": trained_model_name, "metrics": metrics, "project": get_project()}
    check_model_type(model, params)
    check_data_type(train_data, "train", params)
    check_data_type(val_data, "test", params)
    params = add_kwargs_to_params(params, **kwargs)
    response = requests.get(TRAIN_URL, params=params, json=optimiser)
    if response.status_code != 200:
        raise ValueError(response.text)
    return response


def mxnet_metric(metric):
    try:
        from mxnet.metric import CustomMetric
        return isinstance(metric, CustomMetric)
    except:
        return False
