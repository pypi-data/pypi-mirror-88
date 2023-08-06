import sklearn, torch
import torch.nn as nn
import numpy as np
import torch.nn.functional as F
from wilds.common.metrics.metric import Metric, ElementwiseMetric, MultiTaskMetric
from wilds.common.metrics.loss import ElementwiseLoss
from wilds.common.utils import avg_over_groups, minimum, maximum
from scipy.stats import pearsonr

def logits_to_score(logits):
    assert logits.dim() in (1,2)
    if logits.dim()==2: #multi-class logits
        assert logits.size(1)==2, "Only binary classification"
        score = F.softmax(logits, dim=1)[:,1]
    else:
        score = logits
    return score

def logits_to_pred(logits):
    assert logits.dim() in (1,2)
    if logits.dim()==2: #multi-class logits
        pred = torch.argmax(logits, 1)
    else:
        pred = (logits>0).long()
    return pred

def logits_to_binary_pred(logits):
    assert logits.dim() in (1,2)
    pred = (logits>0).long()
    return pred


class Accuracy(ElementwiseMetric):
    def __init__(self, prediction_fn=logits_to_pred, name=None):
        self.prediction_fn = prediction_fn
        if name is None:
            name = 'acc'
        super().__init__(name=name)

    def _compute_element_wise(self, y_pred, y_true):
        if self.prediction_fn is not None:
            y_pred = self.prediction_fn(y_pred)
        return (y_pred==y_true).float()

    def worst(self, metrics):
        return minimum(metrics)

class MultiTaskAccuracy(MultiTaskMetric):
    def __init__(self, prediction_fn=logits_to_binary_pred, name=None):
        self.prediction_fn = prediction_fn  # should work on flattened inputs
        if name is None:
            name = 'acc'
        super().__init__(name=name)

    def _compute_flattened(self, flattened_y_pred, flattened_y_true):
        if self.prediction_fn is not None:
            flattened_y_pred = self.prediction_fn(flattened_y_pred)
        return (flattened_y_pred==flattened_y_true).float()

    def worst(self, metrics):
        return minimum(metrics)

class Recall(Metric):
    def __init__(self, prediction_fn=logits_to_pred, name=None, average='binary'):
        self.prediction_fn = prediction_fn
        if name is None:
            name = f'recall'
            if average is not None:
                name+=f'-{average}'
        self.average = average
        super().__init__(name=name)

    def _compute(self, y_pred, y_true):
        if self.prediction_fn is not None:
            y_pred = self.prediction_fn(y_pred)
        return sklearn.metrics.recall_score(y_true, y_pred, average=self.average, labels=torch.unique(y_true))

    def worst(self, metrics):
        return minimum(metrics)

class F1(Metric):
    def __init__(self, prediction_fn=logits_to_pred, name=None, average='binary'):
        self.prediction_fn = prediction_fn
        if name is None:
            name = f'F1'
            if average is not None:
                name+=f'-{average}'
        self.average = average
        super().__init__(name=name)

    def _compute(self, y_pred, y_true):
        if self.prediction_fn is not None:
            y_pred = self.prediction_fn(y_pred)
        return sklearn.metrics.f1_score(y_true, y_pred, average=self.average, labels=torch.unique(y_true))

    def worst(self, metrics):
        return minimum(metrics)

class BinaryAUROC(Metric):
    def __init__(self, score_fn=logits_to_score, name=None):
        self.score_fn = score_fn
        if name is None:
            name = 'auroc'
        super().__init__(name=name)

    def _compute(self, y_pred, y_true):
        if self.score_fn is not None:
            score = self.score_fn(y_pred)

        try:
            return torch.FloatTensor([sklearn.metrics.roc_auc_score(y_true, score)])
        except ValueError:
            print('Warning: AUROC not defined when only one class is present in y_true.')
            return torch.FloatTensor([float('nan')])

    def worst(self, metrics):
        return minimum(metrics)
      
class BinaryAUPRC(Metric):
    def __init__(self, score_fn=logits_to_score, name=None):
        self.score_fn = score_fn
        if name is None:
            name = f'auprc'

        super().__init__(name=name)

    def _compute(self, y_pred, y_true):
        if self.score_fn is not None:
            score = self.score_fn(y_pred)
        try:
            return torch.FloatTensor([sklearn.metrics.average_precision_score(y_true, score)])
        except ValueError:
            print('Warning: AUPRC not defined when only one class is present in y_true.')
            return torch.FloatTensor([float('nan')])

    def worst(self, metrics):
        return minimum(metrics)

class PrecisionAtRecall(Metric):
    """Given a specific model threshold, determine the precision score achieved"""
    def __init__(self, threshold, score_fn=logits_to_score, name=None):
        self.score_fn = score_fn
        self.threshold = threshold
        if name is None:
            name = "precision_at_global_recall_"
        super().__init__(name=name)

    def _compute(self, y_pred, y_true):
        score = self.score_fn(y_pred)
        predictions = (score > self.threshold)
        return torch.FloatTensor([sklearn.metrics.precision_score(y_true, predictions)])

    def worst(self, metrics):
        return minimum(metrics)

class SQCorrelation(Metric):
    def __init__(self, name=None):
        if name is None:
            name = 'r2'
        super().__init__(name=name)

    def _compute(self, y_pred, y_true):
        r2 = pearsonr(y_pred.squeeze().detach().cpu().numpy(), y_true.squeeze().detach().cpu().numpy())[0]**2
        return torch.tensor(r2)

    def worst(self, metrics):
        return minimum(metrics)

def mse_loss(out, targets, reduction='none'):
    losses = (out - targets)**2
    reduce_dims = tuple(list(range(1, len(targets.shape))))
    losses = torch.mean(losses, dim=reduce_dims)

    if reduction == 'mean':
        loss = losses.mean()
    elif reduction == 'sum':
        loss = losses.sum()
    elif reduction == 'none':
        loss = losses
    return loss

class MSE(ElementwiseLoss):
    def __init__(self, name=None):
        if name is None:
            name = 'mse'
        super().__init__(name=name, loss_fn=mse_loss)
