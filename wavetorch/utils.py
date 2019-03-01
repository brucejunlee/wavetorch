import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

from sklearn.metrics import confusion_matrix

import torch

import time
import os
import socket

SAVEDIR = "./trained/"

def save_model(model, name=None, history=None, args=None):
    str_hostname = socket.gethostname()
    if name is None:
        name = time.strftime("%Y_%m_%d-%H_%M_%S")

    str_filename = 'model_' + str_hostname + '_' + name +  '.pt'
    if not os.path.exists(SAVEDIR):
        os.makedirs(SAVEDIR)
    str_savepath = SAVEDIR + str_filename
    dsave = {"model": model,
             "history": history,
             "args": args}
    print("Saving model to %s" % str_savepath)
    torch.save(dsave, str_savepath)


def load_model(str_filename):
    print("Loading model from %s" % str_filename)
    dload = torch.load(str_filename)
    return dload["model"], dload["history"], dload["args"]


def accuracy(out, yb):
    preds = torch.argmax(out, dim=1)
    return (preds == yb).float().mean().item()


def calc_cm(model, dataloader, verbose=True):
    with torch.no_grad():
        list_yb_pred = []
        list_yb = []
        i = 1
        for xb, yb in dataloader:
            yb_pred = model(xb)
            list_yb_pred.append(yb_pred)
            list_yb.append(yb)
            if verbose: print("cm: processing batch %d" % i)
            i += 1

        y_pred = torch.cat(list_yb_pred, dim=0)
        y_truth = torch.cat(list_yb, dim=0)

    return confusion_matrix(y_truth.argmax(dim=1).numpy(), y_pred.argmax(dim=1).numpy())

