__author__ = 'Milo Utsch and Cecilia Assis'
__version__ = '0.1.0'

import typing as tp

import pandas as pd
import numpy as np

from .intent import Intent

DF = pd.DataFrame


class KnowledgeBase:
    """KnowledgeBase

    Wraps methods for calculating insights regarding the quality of the Knowledge Base.

    Also grants access to intent level insights.

    Attributes
    ----------
    analysed : str
        Analysed base file dataframe.
    labels: list of str
        List of unique intent labels in the knowledge base.
    y_true: list of str
        List of true intent labels in the knowledge base.
    y_pred: list of str
        List of predicted intent labels in the knowledge base.
    intents: dict of Intent
        Dictionary of all intents in the knowledge base.
    all_vs_all_confusion_matrix: pandas.DataFrame
        All vs ALL confusion matrix of the knowledge base.

    Methods
    -------
    get_intent(intent)
        Provides a intent.
    get_best_intent(metric)
        Provides best intent based on a metric.
    get_worst_intent(metric)
        Provides worst intent based on a metric.
    """

    def __init__(self, analysed_base: DF, intent_col: str, predict_col: str) -> None:
        """
        Parameters
        ----------
        analysed_base: pandas.DataFrame
            Analysed base file dataframe.
        intent_col : str
            Column containing the original intents in your knowledge base.
        predict_col : str
            Column containing the predicted intents in your knowledge base.
        """
        self.analysed = analysed_base

        self.labels = analysed_base[intent_col].unique()

        self.y_true = analysed_base[intent_col]
        self.y_pred = analysed_base[predict_col]

        self.intents = {}

        self.__calculate_all_vs_all_confusion_matrix()

    def __create_empty_all_vs_all_matrix(self) -> DF:
        """
        Initializes a ALL vs ALL (multilabel) confusion matrix filled with zeros.

        Returns
        -------
        matrix : pandas.DataFrame:
            Zero filled 2d dataframe with the size of the label count.
        """
        label_count = self.labels.size

        return pd.DataFrame(data=np.zeros((label_count, label_count)),
                            index=self.labels,
                            columns=self.labels)

    def __calculate_all_vs_all_confusion_matrix(self) -> None:
        """Calculates the confusion matrix for this knowledge base.
        """
        confusion_matrix = self.__create_empty_all_vs_all_matrix()

        for i in range(len(self.y_true)):
            confusion_matrix[self.y_true[i]][self.y_pred[i]] += 1.

        self.all_vs_all_confusion_matrix = confusion_matrix

    def get_intent(self, intent) -> Intent:
        """
        Provides intent.

        Parameters
        ----------
        intent : str
            Label of the intent to be retrieved.

        Returns
        -------
        intent : Intent
            Requested intent.

        Raises
        ------
        ZeroDivisionError
            If during intent's metrics calculation the denominator evaluates to zero.
        """
        if intent not in self.intents:
            self.intents[intent] = Intent(label=intent,
                                          all_vs_all_confusion_matrix=self.all_vs_all_confusion_matrix)

        return self.intents[intent]

    def get_best_intent(self, metric: str) -> tp.Tuple[str, float]:
        """Provides best intent based on a metric.

        Parameters
        ----------
        metric : str
            Metric for which the value will be retrived.
            Can be either of "accuracy", "precision", "recall" or "f1".

        Returns
        -------
        intent : tuple of str and float
            Tuple containing intent name and metric value.

        Raises
        ------
        KeyError
            If `metric` is any of the expected ones.
        """
        return self.__sort_metrics(metric)[-1]

    def get_worst_intent(self, metric: str) -> tp.Tuple[str, float]:
        """Provides worst intent based on a metric.

        Parameters
        ----------
        metric : str
            Metric for which the value will be retrived.
            Can be either of "accuracy", "precision", "recall" or "f1".

        Returns
        -------
        intent : tuple of str and float
            Tuple containing intent name and metric value.

        Raises
        ------
        KeyError
            If `metric` is any of the expected ones.
        """
        return self.__sort_metrics(metric)[0]

    def __sort_metrics(self, metric: str) -> tp.List[tp.Tuple]:
        """Sorts in ascending order a list of intents and its values based on a metric.

        Parameters
        ----------
        metric : str
            Metric for which the value will be retrived.
            Can be either of "accuracy", "precision", "recall" or "f1".

        Returns
        -------
        metrics : list of tuple.
            Sorted list

        Raises
        ------
        KeyError
            If `metric` is any of the expected ones.
        """
        metrics = {}

        for label in self.labels:
            intent = self.get_intent(label)
            metrics[intent.label] = intent.get_metric(metric)

        sorted_metrics = sorted(metrics.items(), key=lambda item: item[1])

        return sorted_metrics
